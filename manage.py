#!/usr/bin/env python3
"""Install the personal collection. Python 3.10+, standard library only."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
NAMES = ('architecture', 'code-quality', 'refactoring', 'review', 'testing')
CLIENTS = ('claude', 'codex', 'opencode')
LEGACY = ('clean-architecture', 'clean-code', 'code-review-mastery',
          'refactoring-patterns', 'test-strategy', 'antislop', 'antislop-code',
          'antislop-ui', 'antislop-human', 'antislop-copywriting',
          'kent-beck-style', 'thermos', 'thermo-nuclear-review',
          'thermo-nuclear-code-quality-review')
START = b'<!-- personal-dev-skills:start -->'
END = b'<!-- personal-dev-skills:end -->'


class Conflict(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return path.read_bytes() if path.exists() else None


def safe_path(home, relative):
    """Reject traversal and symlinks/junctions before accessing managed files."""
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts or not rel.parts:
        raise Conflict(f'Invalid manifest path: {relative}')
    path = home / rel
    current = path
    while current != home:
        if current.is_symlink() or (hasattr(current, 'is_junction') and current.is_junction()):
            raise Conflict(f'Linked destination: {current}')
        # Python 3.10/3.11 on Windows: junctions are reparse points too.
        if os.name == 'nt' and current.exists():
            if getattr(current.stat(follow_symlinks=False), 'st_file_attributes', 0) & 1024:
                raise Conflict(f'Reparse destination: {current}')
        current = current.parent
    if not path.resolve().is_relative_to(home):
        raise Conflict(f'Destination escapes home: {path}')
    return path


def layout(client):
    return {
        'claude': ('.claude/skills', '.claude/CLAUDE.md'),
        'codex': ('.agents/skills', '.codex/AGENTS.md'),
        'opencode': ('.config/opencode/skills', '.config/opencode/AGENTS.md'),
    }[client]


def validate(root=ROOT):
    errors = []
    if sorted(p.name for p in (root / 'skills').iterdir() if p.is_dir()) != sorted(NAMES):
        errors.append('The catalog must contain exactly the five declared skills.')
    for name in NAMES:
        path = root / 'skills' / name / 'SKILL.md'
        text = path.read_text(encoding='utf-8')
        match = re.match(r'---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n', text)
        if not match or match[1] != name or not 1 <= len(match[2]) <= 1024:
            errors.append(f'Invalid portable frontmatter: {path}')
    for path in (root / 'skills').rglob('*.md'):
        text = path.read_text(encoding='utf-8')
        for link in re.findall(r'\]\(([^)#]+)(?:#[^)]*)?\)', text):
            if '://' not in link:
                target = (path.parent / link).resolve()
                if not target.is_relative_to((root / 'skills').resolve()) or not target.is_file():
                    errors.append(f'Broken or nonportable link: {path}: {link}')
        for forbidden in ('run_in_background:', 'subagent_type:', 'Companion check', 'npx skills add', 'antislop.md'):
            if forbidden in text:
                errors.append(f'Client-specific/legacy dependency in {path}: {forbidden}')
    for required in ('preferences/COMMON.md', 'NOTICE.md', 'sources.json', 'licenses/MIT.txt'):
        if not (root / required).is_file():
            errors.append(f'Missing {required}')
    if errors:
        raise Conflict('\n'.join(errors))


def desired(clients, root=ROOT):
    result = {}
    notice = (root / 'NOTICE.md').read_bytes() + b'\n' + (root / 'licenses/MIT.txt').read_bytes()
    for client in sorted(clients):
        skills, rules = layout(client)
        for name in NAMES:
            for path in sorted((root / 'skills' / name).rglob('*')):
                if path.is_file():
                    rel = path.relative_to(root / 'skills').as_posix()
                    result[f'{skills}/{rel}'] = ('file', path.read_bytes(), client)
            result[f'{skills}/{name}/NOTICE.txt'] = ('file', notice, client)
        prefs = (root / 'preferences/COMMON.md').read_bytes().rstrip(b'\r\n')
        result[rules] = ('block', START + b'\n' + prefs + b'\n' + END + b'\n', client)
    return result


def inspect_duplicates(home, managed):
    roots = ('.claude/skills', '.agents/skills', '.codex/skills', '.config/opencode/skills')
    problems = []
    for rel in roots:
        directory = safe_path(home, rel)
        if not directory.exists():
            continue
        for skill in directory.glob('*/SKILL.md'):
            key = skill.relative_to(home).as_posix()
            name_match = re.search(r'^name:\s*[\'"]?([\w-]+)', skill.read_text(encoding='utf-8-sig'), re.M)
            name = name_match[1] if name_match else skill.parent.name
            if (name in NAMES or name in LEGACY or skill.parent.name in NAMES + LEGACY) and key not in managed:
                problems.append(f'Unmanaged overlapping skill: {skill}')
    if problems:
        raise Conflict('\n'.join(problems) + '\nArchive/disable these outside discovery paths before installing. Nothing was changed.')


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.personal-skills-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def prepare(home, action, clients, root=ROOT):
    state_path = safe_path(home, '.personal-dev-skills/state.json')
    original_state = read(state_path)
    state = json.loads(original_state) if original_state else {'version': 1, 'clients': [], 'files': {}}
    if state.get('version') != 1:
        raise Conflict('Unsupported manifest version')
    registered = set(state['clients'])
    if not registered <= set(CLIENTS):
        raise Conflict('Invalid registered clients')
    # Never trust a changed manifest to nominate arbitrary files for deletion.
    for rel, entry in state['files'].items():
        client = entry['client']
        if client not in registered:
            raise Conflict(f'Invalid owner: {rel}')
        folder, rules = layout(client)
        valid_file = any(rel.startswith(f'{folder}/{name}/') for name in NAMES)
        if not ((entry['kind'] == 'file' and valid_file) or (entry['kind'] == 'block' and rel == rules)):
            raise Conflict(f'Invalid managed destination: {rel}')
        safe_path(home, rel)
    chosen = set(clients)
    target = registered | chosen if action == 'install' else registered - chosen
    if action == 'check':
        if not registered or (chosen and not chosen <= registered):
            raise Conflict('Requested clients are not installed')
        target = registered
    wanted = {} if action == 'uninstall' else desired(target, root)
    if action != 'uninstall':
        validate(root)
        inspect_duplicates(home, state['files'])
    changes, records = {}, {}
    for rel in sorted(set(wanted) | set(state['files'])):
        path = safe_path(home, rel)
        before = read(path)
        old = state['files'].get(rel)
        spec = wanted.get(rel)
        if old:
            if old['kind'] == 'file':
                if before is None or digest(before) != old['sha256']:
                    raise Conflict(f'Managed file changed or missing: {path}')
                base = None
            else:
                token = base64.b64decode(old['token'])
                if before is None or before.count(START) != 1 or before.count(END) != 1 or before.count(token) != 1:
                    raise Conflict(f'Managed preferences changed: {path}')
                base = before.replace(token, b'', 1)
        else:
            base = before
        if action == 'uninstall' and old['client'] in target:
            records[rel] = old
            continue
        if spec:
            kind, content, client = spec
            if kind == 'file':
                if old is None and before is not None:
                    raise Conflict(f'Will not adopt/overwrite existing file: {path}')
                after = content
                records[rel] = {'kind': kind, 'client': client, 'sha256': digest(content)}
            else:
                if old is None and base and (START in base or END in base):
                    raise Conflict(f'Unmanaged preference markers: {path}')
                # Reinsert at the same location to preserve external edits byte-for-byte.
                if old:
                    previous = base64.b64decode(old['token'])
                    prefix = previous[:previous.index(START)]
                    token = prefix + content
                    after = before.replace(previous, token, 1)
                else:
                    token = (b'\n\n' if base else b'') + content
                    after = (base or b'') + token
                records[rel] = {'kind': kind, 'client': client, 'sha256': digest(token),
                                'token': base64.b64encode(token).decode(),
                                'existed': old['existed'] if old else before is not None}
        else:
            after = base
            if old['kind'] == 'block' and not after and not old['existed']:
                after = None
        if before != after:
            changes[path] = (before, after)
    new_state = json.dumps({'version': 1, 'clients': sorted(target), 'files': records}, indent=2).encode() + b'\n'
    if action == 'check':
        if changes:
            raise Conflict('Installed collection differs from source; run install to update:\n' + '\n'.join(map(str, changes)))
    elif new_state != original_state:
        changes[state_path] = (original_state, new_state)
    return changes, target


def transact(home, changes):
    if not changes:
        return
    lock = safe_path(home, '.personal-dev-skills/install.lock')
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        handle = lock.open('xb')
    except FileExistsError:
        raise Conflict(f'Another installation or stale lock exists: {lock}') from None
    applied = []
    try:
        with handle:
            handle.write(str(os.getpid()).encode())
        for path, (before, _) in changes.items():
            safe_path(home, path.relative_to(home))
            if read(path) != before:
                raise Conflict(f'File changed after preflight: {path}')
        for path, (before, after) in changes.items():
            if after is None:
                path.unlink()
            else:
                atomic_write(path, after)
            applied.append((path, before))
    except BaseException:
        for path, before in reversed(applied):
            if before is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, before)
        raise
    finally:
        lock.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('validate', 'install', 'check', 'uninstall', 'run-opencode'))
    parser.add_argument('--client', action='append', choices=CLIENTS + ('all',), default=[])
    parser.add_argument('--home', type=Path, help='Isolated target home; defaults to the current user home')
    parser.add_argument('--dry-run', action='store_true', help='Preflight and display changes without writing')
    args, forwarded = parser.parse_known_args(argv)
    try:
        if args.action == 'validate':
            validate()
            print('Catalog valid: 5 skills, portable metadata and resolved references.')
            return 0
        if args.action == 'run-opencode':
            if args.home or args.dry_run or args.client:
                raise Conflict('run-opencode accepts only arguments after --; install/check separately.')
            # Both flags cover older and newer OpenCode releases. No global env is changed.
            env = dict(os.environ, OPENCODE_DISABLE_EXTERNAL_SKILLS='1', OPENCODE_DISABLE_CLAUDE_CODE_SKILLS='1')
            executable = shutil.which('opencode')
            if not executable:
                raise Conflict('opencode is not on PATH')
            return subprocess.call([executable] + (forwarded[1:] if forwarded[:1] == ['--'] else forwarded), env=env)
        if forwarded:
            parser.error('unrecognized arguments: ' + ' '.join(forwarded))
        if args.home is None:
            for key in ('CODEX_HOME', 'CLAUDE_CONFIG_DIR', 'XDG_CONFIG_HOME', 'OPENCODE_CONFIG_DIR'):
                if os.environ.get(key):
                    raise Conflict(f'{key} is set. Custom client roots are not managed; use standard roots or --home for an isolated sandbox.')
        home = (args.home or Path.home()).absolute()
        if home.is_symlink() or (hasattr(home, 'is_junction') and home.is_junction()):
            raise Conflict('Home must not be a link')
        home = home.resolve()
        clients = set(CLIENTS if 'all' in args.client else args.client)
        if args.action in ('install', 'uninstall') and not clients:
            parser.error('--client is required for install/uninstall')
        changes, target = prepare(home, args.action, clients)
        for path, (before, after) in changes.items():
            verb = 'DELETE' if after is None else 'CREATE' if before is None else 'UPDATE'
            print(f'{verb} {path}')
        if not args.dry_run and args.action != 'check':
            transact(home, changes)
        print(('Preview' if args.dry_run else 'OK') + ': ' + ', '.join(sorted(target)))
        if 'opencode' in target and len(target) > 1:
            print('Use: python manage.py run-opencode -- [args] to avoid scanning Claude/Codex copies.')
        return 0
    except (Conflict, OSError, ValueError, KeyError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
