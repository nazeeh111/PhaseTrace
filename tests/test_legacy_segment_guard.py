"""Exercise only actual legacy segmentation loops on synthetic arrays, without I/O."""
import ast
from pathlib import Path
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PATHS = [f'expe/240116/{name}.py' for name in
         ('visualize_phase', 'visualize_phase_4', 'visualize_phase_8',
          'visualize_phase_figquiestbien')]
PATHS += [f'expe/{day}/generate_subsignals.py' for day in ('240118', '240119')]


def loops(path):
    tree = ast.parse((ROOT / path).read_text())
    # Select top-level loops that assign to the accumulator. Never import the
    # scripts: their top-level loads, saves and plots must remain unexecuted.
    selected = [node for node in tree.body if isinstance(node, ast.For)
                and any(isinstance(child, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == 'signal'
                                for t in child.targets)
                        for child in ast.walk(node))]
    if len(selected) != 2:
        raise AssertionError(f'{path}: expected two segmentation loops')
    return selected


def execute(node, sig):
    namespace = dict(np=np, sig=sig, n=100, factor=[], signals=[], signal=[])
    code = compile(ast.Module(body=[node], type_ignores=[]), '<actual loop>', 'exec')
    exec(code, namespace)
    return namespace


class LegacySegmentGuardTests(unittest.TestCase):
    def test_synthetic_runs_and_existing_boundaries(self):
        # Each tuple defines block values, expected completed sample ranges,
        # pending range, and the original factor mask. The final complete block
        # is deliberately excluded by the existing range; pending runs are not
        # flushed. This change does not alter either historical policy.
        cases = [
            ('joined', [2001., 2002., 0., 0.], [(0, 200)], None, [1000, 1000, 0]),
            ('separate', [2001., 0., 2002., 0., 0.], [(0, 100), (200, 300)], None,
             [1000, 0, 1000, 0]),
            ('threshold', [1000., 0., 0.], [], None, [0, 0]),
            ('pending', [0., 2001., 2002., 0.], [], (100, 300), [0, 1000, 1000]),
            ('complex', [2001.+3j, 2002.+4j, 0j, 0j], [(0, 200)], None,
             [1000, 1000, 0]),
        ]
        for path in PATHS:
            for node in loops(path):
                for name, blocks, completed, pending, mask in cases:
                    dtype = np.complex64 if name == 'complex' else np.float32
                    sig = np.repeat(np.array(blocks, dtype=dtype), 100)
                    with self.subTest(path=path, line=node.lineno, case=name):
                        result = execute(node, sig)
                        self.assertEqual(len(result['signals']), len(completed))
                        for actual, (start, stop) in zip(result['signals'], completed):
                            np.testing.assert_array_equal(actual, sig[start:stop])
                            self.assertEqual(actual.dtype, sig.dtype)
                        if pending is None:
                            self.assertEqual(result['signal'], [])
                        else:
                            np.testing.assert_array_equal(result['signal'],
                                                          sig[slice(*pending)])
                            self.assertEqual(result['signal'].dtype, sig.dtype)
                        self.assertEqual(result['factor'], np.repeat(mask, 100).tolist())
                for length, completed, mask in [(90, [], []), (350, [(0, 200)],
                                                                          [1000, 1000, 0])]:
                    with self.subTest(path=path, line=node.lineno, length=length):
                        sig = np.r_[np.full(200, 2001, dtype=np.float32),
                                    np.zeros(150, dtype=np.float32)][:length]
                        result = execute(node, sig)
                        self.assertEqual(len(result['signals']), len(completed))
                        for actual, (start, stop) in zip(result['signals'], completed):
                            np.testing.assert_array_equal(actual, sig[start:stop])
                            self.assertEqual(actual.dtype, sig.dtype)
                        self.assertEqual(result['signal'], [])
                        self.assertEqual(result['factor'], np.repeat(mask, 100).tolist())


if __name__ == '__main__':
    unittest.main()
