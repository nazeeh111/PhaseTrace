"""Actual baseline shell setup, stopped before any experiment iteration."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = [('24-06-01_nrf52-baseline', name)
         for name in ('profile.sh', 'attack.sh', 'attack_plot.sh')]
CASES += [('24-06-05_nrf52-baseline', name)
          for name in ('profile.sh', 'attack.sh', 'attack_plot.sh')]


def setup_events(repository, folder, name, relative=False):
    with tempfile.TemporaryDirectory(prefix='phase-baseline-setup-') as tmp:
        root = Path(tmp).resolve()
        source = root / 'dataset/src'
        source.mkdir(parents=True)
        for item in (name, 'env.sh'):
            shutil.copyfile(repository / 'sets' / folder / 'src' / item, source / item)
        if name == 'attack_plot.sh':
            (source/'attack_plot.py').write_text('# inert path-resolution marker\n')
        external = root / 'external'
        external.mkdir()
        marker = external / 'untouched'
        marker.write_bytes(b'not a real checkout')
        commands = root / 'commands'
        commands.mkdir()
        git = commands / 'git'
        git.write_text('#!' + sys.executable + '''
import json,os,sys
with open(os.environ['SETUP_EVENTS'],'a') as f:
    f.write(json.dumps({'argv':sys.argv[1:],'cwd':os.getcwd()})+'\\n')
''')
        git.chmod(0o755)
        blocked = commands / 'scaff'
        blocked.write_text('#!/bin/sh\nprintf blocked > "$SETUP_BLOCKED"\nexit 99\n')
        blocked.chmod(0o755)
        # Real entry scripts all reach this top-level loop after their checkout.
        # Do not execute a profile, attack, CSV write or plotting command.
        stop = root / 'stop.bash'
        stop.write_text('''trap 'case "$BASH_COMMAND" in for\\ comp\\ in*) pwd -P > "$SETUP_LOOP_CWD"; printf stopped > "$SETUP_LOOP_STOP"; exit 0;; esac' DEBUG
''')
        events = root / 'events.jsonl'
        env = {k: v for k, v in os.environ.items() if not k.startswith('BASH_FUNC_')}
        env.update(PATH=str(commands)+os.pathsep+os.environ['PATH'],
                   PATH_SCAFF=str(external), BASH_ENV=str(stop),
                   SETUP_EVENTS=str(events), SETUP_LOOP_STOP=str(root/'stopped'),
                   SETUP_BLOCKED=str(root/'blocked'), SETUP_LOOP_CWD=str(root/'loop-cwd'))
        argument = str((source/name).relative_to(root)) if relative else str(source/name)
        run = subprocess.run(['/bin/bash', argument], cwd=root,
                             env=env, capture_output=True, text=True, timeout=5)
        records = [json.loads(s) for s in events.read_text().splitlines()] if events.exists() else []
        assert (root/'stopped').read_text() == 'stopped'
        assert not (root/'blocked').exists()
        loop_cwd = Path((root/'loop-cwd').read_text().strip())
        affected = folder.startswith('24-06-01') or name == 'attack_plot.sh'
        assert loop_cwd == (root if affected else external)
        if name == 'attack_plot.sh':
            # Preserve the real final command's ${0/.sh/.py} resolution.
            plot_argument = Path(argument.replace('.sh', '.py'))
            plot_path = plot_argument if plot_argument.is_absolute() else loop_cwd/plot_argument
            assert plot_path.resolve() == source/'attack_plot.py'
        assert marker.read_bytes() == b'not a real checkout'
        assert list(external.iterdir()) == [marker]
        assert not (root / 'dataset/profile').exists()
        assert not (root / 'dataset/logs').exists()
        assert not (root / 'dataset/csv').exists()
        for event in records:
            assert event['cwd'] == str(external)
            event['cwd'] = '<disposable external directory>'
        return run.returncode, run.stderr, records


class BaselineCheckoutTests(unittest.TestCase):
    def test_all_six_entries_use_their_declared_checkout_helper_before_the_loop(self):
        for folder, name in CASES:
            for relative in (False, True):
                with self.subTest(folder=folder, name=name, relative=relative):
                    status, stderr, records = setup_events(ROOT, folder, name, relative)
                    self.assertEqual(status, 0, stderr)
                    self.assertNotIn('command not found', stderr)
                    revision = ('4aed4cb37b968774cb9e188cf201c2335310e1e0'
                                if folder.startswith('24-06-01') else 'master')
                    self.assertEqual(records, [{'argv': ['checkout', revision],
                                               'cwd': '<disposable external directory>'}])


if __name__ == '__main__':
    unittest.main()
