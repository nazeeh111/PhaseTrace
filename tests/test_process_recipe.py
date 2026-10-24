"""Run the actual shell recipe with inert command/dependency substitutes.

No acquisition, external datasets, filtering or key recovery is executed.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sets/24-07-04_nrf52-ref/src'


class ProcessRecipe(unittest.TestCase):
    def test_each_filter_recipe_receives_its_required_selector(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp); src = folder / 'src'; src.mkdir()
            for name in ('process.sh', 'env.sh'):
                shutil.copyfile(SOURCE / name, src / name)
            # Preserve the real script's command ordering and argument boundaries.
            # This substitute only records argv; it performs no signal operations.
            stub = src / 'process_filt.py'
            stub.write_text('''#!/usr/bin/env python3
import json,os,sys
with open(os.environ['RECIPE_CALLS'],'a') as f:
    f.write(json.dumps(sys.argv[1:])+'\\n')
raise SystemExit(0 if len(sys.argv)==5 else 2)
''')
            stub.chmod(0o755)
            bin_dir = folder / 'bin'; bin_dir.mkdir()
            for name in ('scaff', 'cp'):
                f = bin_dir / name; f.write_text('#!/bin/sh\nexit 0\n'); f.chmod(0o755)
            calls = folder / 'calls.jsonl'
            env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ['PATH'],
                       RECIPE_CALLS=str(calls), TERM='xterm')
            run = subprocess.run(['bash', str(src / 'process.sh')], cwd=folder,
                                 env=env, capture_output=True, text=True, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            records = [json.loads(line) for line in calls.read_text().splitlines()]
            self.assertEqual(len(records), 8)
            for args in records:
                with self.subTest(args=args):
                    self.assertEqual(len(args), 4, 'process_filt.py requires load, save, config and filter')
                    self.assertEqual(args[2], 'src/collect.toml')
                    self.assertEqual(args[3], args[1].split('_filt_')[1])


if __name__ == '__main__':
    unittest.main()
