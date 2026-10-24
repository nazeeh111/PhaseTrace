"""Execute actual collect() metadata setup, stopping before any device access."""
import ast
import os
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ('24-07-04_nrf52-ref', '24-07-09_arduino-ref',
           '24-07-09_stm32l1-ref', '24-10-10_nrf51-ref')


class SerialBoundary(Exception):
    pass


def metadata(folder, target, *, fixed_vs_fixed, fixed_key=False,
             fixed_plaintext=False, key_override=None, points_override=-1):
    source = ROOT / 'sets' / folder / 'src/collect.py'
    tree = ast.parse(source.read_text(), filename=str(source))
    collect = next(node for node in tree.body
                   if isinstance(node, ast.FunctionDef) and node.name == 'collect')
    # Remove only Click registration decorators, not the function body.
    collect.decorator_list = []
    module = ast.Module(body=[collect], type_ignores=[])
    random_calls, serial_calls = [], []

    def random_bytes(length):
        random_calls.append(length)
        return bytes([len(random_calls)]) * length

    def stop_before_serial():
        serial_calls.append(True)
        raise SerialBoundary()

    config = {'fw': {'mode': 'tinyaes', 'fixed_key': fixed_key,
                     'fixed_plaintext': fixed_plaintext, 'fixed_vs_fixed': fixed_vs_fixed},
              'scaff': {'legacy': {'num_traces_per_point': 25}}, 'num_points': 4}
    namespace = {'CONFIG': config, 'os': SimpleNamespace(urandom=random_bytes),
                 'path': os.path, 'YKUSH_PORT': 0,
                 'TINY_AES_MODE': SimpleNamespace(have_keys=True),
                 '_open_serial_port': stop_before_serial}
    # No source imports, Click initialization, serial, RF, model or dataset calls.
    exec(compile(module, str(source), 'exec'), namespace)
    try:
        namespace['collect'](str(target), None, False, None, False, False, 0,
                             points_override, key_override)
    except SerialBoundary:
        pass
    else:
        raise AssertionError('Expected inert pre-device stop')
    assert serial_calls == [True]
    return [(target / name).read_text().splitlines() for name in ('pt.txt', 'key.txt')], random_calls


class CollectionMetadataTests(unittest.TestCase):
    def test_fixed_vs_fixed_serializes_exact_existing_patterns_without_randomness(self):
        for folder in FOLDERS:
            with self.subTest(folder=folder), tempfile.TemporaryDirectory() as tmp:
                target = Path(tmp)
                (target / 'untouched').write_bytes(b'fixture marker')
                values, calls = metadata(folder, target, fixed_vs_fixed=True)
                self.assertEqual(values[0], ['00' * 16] * 4)
                self.assertEqual(values[1], ['00' * 16, '30' * 16] * 2)
                self.assertEqual(calls, [])
                self.assertEqual((target / 'untouched').read_bytes(), b'fixture marker')

    def test_ordinary_fixed_variable_and_override_paths_keep_exact_metadata(self):
        cases = [(False, False, None, -1), (True, True, None, -1),
                 (True, False, False, 3), (False, True, True, 3)]
        for folder in FOLDERS:
            for fixed_key, fixed_plaintext, override, points in cases:
                with self.subTest(folder=folder, case=(fixed_key, fixed_plaintext, override, points)), tempfile.TemporaryDirectory() as tmp:
                    values, calls = metadata(folder, Path(tmp), fixed_vs_fixed=False,
                                             fixed_key=fixed_key, fixed_plaintext=fixed_plaintext,
                                             key_override=override, points_override=points)
                    count = 4 if points == -1 else points
                    plaintext_count = 1 if fixed_plaintext else count
                    effective_key = fixed_key if override is None else override
                    key_count = 1 if effective_key else count
                    expected = [bytes([i]).hex() * 16
                                for i in range(1, plaintext_count+key_count+1)]
                    self.assertEqual(values, [expected[:plaintext_count], expected[plaintext_count:]])
                    self.assertEqual(calls, [16] * (plaintext_count+key_count))


if __name__ == '__main__':
    unittest.main()
