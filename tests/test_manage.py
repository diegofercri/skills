import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('manage', Path(__file__).resolve().parents[1] / 'manage.py')
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='skills test spaces ')
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / 'home with spaces'
        self.home.mkdir()
        self.root = Path(self.temp.name) / 'source'
        self.root.mkdir()
        shutil.copytree(m.ROOT / 'skills', self.root / 'skills')
        shutil.copytree(m.ROOT / 'preferences', self.root / 'preferences')
        shutil.copytree(m.ROOT / 'licenses', self.root / 'licenses')
        for file in ('NOTICE.md', 'sources.json'):
            shutil.copy2(m.ROOT / file, self.root / file)

    def run_action(self, action='install', clients=m.CLIENTS):
        changes, target = m.prepare(self.home, action, clients, self.root)
        m.transact(self.home, changes)
        return changes, target

    def snapshot(self):
        return {p.relative_to(self.home).as_posix(): p.read_bytes() for p in self.home.rglob('*') if p.is_file()}

    def test_install_check_idempotent_and_copies(self):
        self.run_action()
        first = self.snapshot()
        self.assertEqual(self.run_action()[0], {})
        self.assertEqual(self.snapshot(), first)
        self.assertEqual(m.prepare(self.home, 'check', [], self.root)[0], {})
        for client in m.CLIENTS:
            folder, _ = m.layout(client)
            for name in m.NAMES:
                self.assertEqual((self.home / folder / name / 'SKILL.md').read_bytes(),
                                 (self.root / 'skills' / name / 'SKILL.md').read_bytes())
                self.assertTrue((self.home / folder / name / 'NOTICE.txt').is_file())

    def test_preview_writes_nothing(self):
        changes, _ = m.prepare(self.home, 'install', m.CLIENTS, self.root)
        self.assertTrue(changes)
        self.assertEqual(self.snapshot(), {})

    def test_preserve_external_preferences_bytes(self):
        rule = self.home / '.claude/CLAUDE.md'
        rule.parent.mkdir()
        original = b'Personal\r\nUTF8: \xc3\xb1\r\n'
        rule.write_bytes(original)
        self.run_action(clients=['claude'])
        rule.write_bytes(rule.read_bytes() + b'\r\nNew external note\r\n')
        self.run_action('uninstall', ['claude'])
        self.assertEqual(rule.read_bytes(), original + b'\r\nNew external note\r\n')

    def test_update_preferences_preserves_external_suffix(self):
        self.run_action(clients=['codex'])
        rule = self.home / '.codex/AGENTS.md'
        rule.write_bytes(rule.read_bytes() + b'Outside')
        prefs = self.root / 'preferences/COMMON.md'
        prefs.write_bytes(prefs.read_bytes() + b'\nNew preference\n')
        self.run_action(clients=['codex'])
        self.assertTrue(rule.read_bytes().endswith(b'Outside'))
        self.assertEqual(rule.read_bytes().count(m.START), 1)
        self.run_action('uninstall', ['codex'])
        self.assertEqual(rule.read_bytes(), b'Outside')

    def test_uninstall_one_client_preserves_others(self):
        self.run_action()
        self.run_action('uninstall', ['claude'])
        self.assertFalse((self.home / '.claude/skills/review/SKILL.md').exists())
        self.assertTrue((self.home / '.agents/skills/review/SKILL.md').exists())
        self.assertTrue((self.home / '.config/opencode/skills/review/SKILL.md').exists())
        m.prepare(self.home, 'check', ['codex', 'opencode'], self.root)

    def test_uninstall_preserves_foreign_files(self):
        self.run_action()
        extra = self.home / '.agents/skills/review/my-notes.txt'
        extra.write_text('mine')
        self.run_action('uninstall')
        self.assertEqual(extra.read_text(), 'mine')
        self.assertFalse(list(self.home.rglob('SKILL.md')))
        self.assertFalse((self.home / '.claude/CLAUDE.md').exists())

    def test_uninstall_does_not_upgrade_remaining_clients(self):
        self.run_action()
        installed = self.home / '.agents/skills/review/SKILL.md'
        before = installed.read_bytes()
        source = self.root / 'skills/review/SKILL.md'
        source.write_bytes(before + b'\nNew source revision\n')
        self.run_action('uninstall', ['claude'])
        self.assertEqual(installed.read_bytes(), before)

    def test_modified_skill_stops_entire_update(self):
        self.run_action()
        path = self.home / '.agents/skills/review/SKILL.md'
        path.write_bytes(path.read_bytes() + b'changed')
        before = self.snapshot()
        with self.assertRaises(m.Conflict):
            self.run_action()
        self.assertEqual(self.snapshot(), before)

    def test_modified_block_stops_uninstall(self):
        self.run_action()
        rule = self.home / '.claude/CLAUDE.md'
        rule.write_bytes(rule.read_bytes().replace(b'Approach', b'Changed'))
        before = self.snapshot()
        with self.assertRaises(m.Conflict):
            self.run_action('uninstall')
        self.assertEqual(self.snapshot(), before)

    def test_missing_managed_file_stops_update(self):
        self.run_action()
        (self.home / '.agents/skills/testing/SKILL.md').unlink()
        with self.assertRaises(m.Conflict):
            self.run_action()

    def test_unmanaged_same_name_blocked_even_identical(self):
        destination = self.home / '.claude/skills/review'
        shutil.copytree(self.root / 'skills/review', destination)
        before = self.snapshot()
        with self.assertRaises(m.Conflict):
            self.run_action()
        self.assertEqual(self.snapshot(), before)

    def test_legacy_overlap_blocked(self):
        path = self.home / '.config/opencode/skills/clean-code/SKILL.md'
        path.parent.mkdir(parents=True)
        path.write_text('---\nname: clean-code\n---\n')
        with self.assertRaisesRegex(m.Conflict, 'overlapping'):
            self.run_action()

    def test_name_collision_in_different_folder(self):
        path = self.home / '.claude/skills/custom-folder/SKILL.md'
        path.parent.mkdir(parents=True)
        path.write_text('---\nname: "review"\n---\n')
        with self.assertRaises(m.Conflict):
            self.run_action()

    def test_source_update_and_removed_reference(self):
        self.run_action()
        path = self.root / 'skills/review/references/temporary.md'
        path.write_text('version one')
        self.run_action()
        installed = self.home / '.agents/skills/review/references/temporary.md'
        self.assertEqual(installed.read_text(), 'version one')
        path.write_text('version two')
        with self.assertRaisesRegex(m.Conflict, 'differs from source'):
            m.prepare(self.home, 'check', [], self.root)
        self.run_action()
        self.assertEqual(installed.read_text(), 'version two')
        path.unlink()
        self.run_action()
        self.assertFalse(installed.exists())

    def test_rollback_after_midwrite_failure(self):
        changes, _ = m.prepare(self.home, 'install', m.CLIENTS, self.root)
        write = m.atomic_write
        counter = [0]

        def fail_once(path, data):
            counter[0] += 1
            if counter[0] == 4:
                raise OSError('simulated disk failure')
            return write(path, data)

        with patch.object(m, 'atomic_write', fail_once):
            with self.assertRaises(OSError):
                m.transact(self.home, changes)
        self.assertEqual(self.snapshot(), {})

    def test_file_changed_between_prepare_and_apply(self):
        changes, _ = m.prepare(self.home, 'install', ['claude'], self.root)
        path = self.home / '.claude/CLAUDE.md'
        path.parent.mkdir()
        path.write_text('new user file')
        with self.assertRaises(m.Conflict):
            m.transact(self.home, changes)
        self.assertEqual(path.read_text(), 'new user file')
        self.assertFalse(list(self.home.rglob('SKILL.md')))

    def test_lock_blocks_mutation(self):
        changes, _ = m.prepare(self.home, 'install', ['claude'], self.root)
        lock = self.home / '.personal-dev-skills/install.lock'
        lock.parent.mkdir()
        lock.write_text('existing process')
        with self.assertRaises(m.Conflict):
            m.transact(self.home, changes)
        self.assertEqual(lock.read_text(), 'existing process')

    def test_manifest_cannot_delete_arbitrary_file(self):
        self.run_action()
        path = self.home / '.personal-dev-skills/state.json'
        state = json.loads(path.read_bytes())
        state['files']['private.txt'] = {'kind': 'file', 'client': 'claude', 'sha256': m.digest(b'private')}
        path.write_text(json.dumps(state))
        (self.home / 'private.txt').write_bytes(b'private')
        with self.assertRaises(m.Conflict):
            self.run_action('uninstall')
        self.assertEqual((self.home / 'private.txt').read_bytes(), b'private')

    def test_traversal_rejected(self):
        with self.assertRaises(m.Conflict):
            m.safe_path(self.home, '../outside')

    def test_linked_destination_rejected(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        try:
            (self.home / '.claude').symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('Creating symlinks is unavailable in this environment')
        with self.assertRaises(m.Conflict):
            self.run_action()

    def test_catalog_and_broken_reference(self):
        m.validate(self.root)
        path = self.root / 'skills/review/SKILL.md'
        path.write_text(path.read_text() + '\n[broken](missing.md)\n')
        with self.assertRaisesRegex(m.Conflict, 'Broken'):
            m.validate(self.root)

    def test_check_uninstalled(self):
        with self.assertRaises(m.Conflict):
            m.prepare(self.home, 'check', [], self.root)

    def test_opencode_launcher_flags_and_args(self):
        with patch.object(m.shutil, 'which', return_value='opencode'), patch.object(m.subprocess, 'call', return_value=0) as call:
            self.assertEqual(m.main(['run-opencode', '--', '--version']), 0)
        self.assertEqual(call.call_args.args[0], ['opencode', '--version'])
        self.assertEqual(call.call_args.kwargs['env']['OPENCODE_DISABLE_EXTERNAL_SKILLS'], '1')
        self.assertEqual(call.call_args.kwargs['env']['OPENCODE_DISABLE_CLAUDE_CODE_SKILLS'], '1')


if __name__ == '__main__':
    unittest.main()
