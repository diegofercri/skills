"""Optional discovery smoke test: python tests/smoke_codex.py /path/to/codex.

Starts only the local app-server and requests its skill catalog, never a model turn.
"""
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import manage


def main():
    executable = str(Path(sys.argv[1]).resolve())
    with tempfile.TemporaryDirectory(prefix='codex-skills-smoke-') as temp:
        home = Path(temp)
        changes, _ = manage.prepare(home, 'install', ['codex'])
        manage.transact(home, changes)
        env = dict(os.environ, HOME=temp, USERPROFILE=temp, CODEX_HOME=str(home / '.codex'))
        messages = queue.Queue()
        with tempfile.TemporaryFile() as errors:
            process = subprocess.Popen([executable, 'app-server', '--stdio'], cwd=home,
                                       env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=errors, text=True, encoding='utf-8')
            def receive():
                for line in process.stdout:
                    try:
                        messages.put(json.loads(line))
                    except ValueError:
                        pass
            threading.Thread(target=receive, daemon=True).start()

            def send(value):
                process.stdin.write(json.dumps(value) + '\n')
                process.stdin.flush()

            def response(identifier):
                while True:
                    message = messages.get(timeout=20)
                    if message.get('id') == identifier:
                        if 'error' in message:
                            raise RuntimeError(message['error'])
                        return message['result']

            try:
                send({'id': 1, 'method': 'initialize', 'params': {
                    'clientInfo': {'name': 'skill_catalog_smoke', 'version': '1.0'}}})
                response(1)
                send({'method': 'initialized', 'params': {}})
                send({'id': 2, 'method': 'skills/list', 'params': {'cwds': [temp], 'forceReload': True}})
                result = response(2)
                skills = [skill for entry in result['data'] for skill in entry['skills']]
                own = [skill for skill in skills if skill['name'] in manage.NAMES]
                counts = {name: sum(s['name'] == name for s in own) for name in manage.NAMES}
                print(json.dumps({'counts': counts, 'errors': [e for item in result['data'] for e in item.get('errors', [])]}, indent=2))
                if any(count != 1 for count in counts.values()):
                    raise RuntimeError('Expected exactly one entry per curated skill')
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                process.stdin.close()
                process.stdout.close()


if __name__ == '__main__':
    main()
