# PhaseTrace

Experiment scripts, figures and dataset recipes for analyzing phase-modulated electromagnetic measurements.

[Inspect a bundled trace](#inspect-a-bundled-trace) · [Explore the workspace](#explore-the-workspace) · [Full reproduction guide](docs/2025-01-23_tches-artifact/README.md)

![Stored nRF52 phase-rotation traces from the reproduction guide](docs/2025-01-23_tches-artifact/gfx/24-07-04_nrf52-ref_attack_filt_lh1e6_0_phr.png)

The plotted, aligned phase-rotation traces are a retained figure from the [nRF52 artifact guide](docs/2025-01-23_tches-artifact/README.md), not a new experimental run. The guide explains the measured input, processing and attack workflow; complete reproduction needs its external datasets and environment.

## Inspect a bundled trace

From a checkout, read the small stored I/Q example with **NumPy alone**:

```sh
python -m pip install numpy
python - <<'PYTHON'
from pathlib import Path
import numpy as np

folder = Path('expe/24-03-19_phasor-plot')
i = np.load(folder / 'i__0.npy', allow_pickle=False)
q = np.load(folder / 'q__0.npy', allow_pickle=False)
assert i.shape == q.shape == (2400,)
assert np.isfinite(i).all() and np.isfinite(q).all()
iq = i + 1j*q
print(f'{iq.size} complex samples from stored I/Q')
print(f'{iq.dtype}; finite: {bool(np.isfinite(iq).all())}')
PYTHON
```

```text
2400 complex samples from stored I/Q
complex64; finite: True
```

This reads the retained arrays without writing files, initializing submodules or downloading datasets. It follows the I/Q construction in [`phasor.py`](expe/24-03-19_phasor-plot/phasor.py); its [stored phasor plot](expe/24-03-19_phasor-plot/plot_polar_abs(iq);angle(iq).pdf) is available separately. This small input check does not rerun filtering, alignment or key recovery, and the figure above belongs to a different experiment in the artifact guide.

## Explore the workspace

| Location | Purpose |
| --- | --- |
| `expe/` | Experiment-specific analysis scripts, stored arrays and figures |
| `sets/` | Dataset definitions and supporting files |
| `src/` | Dataset utility scripts |
| `mods/` | Pinned external firmware, analysis and recording modules |
| [Reproduction guide](docs/2025-01-23_tches-artifact/README.md) | Existing container workflow and dataset references |

## Source checkout

```sh
git clone https://github.com/nazeeh111/PhaseTrace.git
cd PhaseTrace
git submodule update --init --recursive
```

The three external modules retain their original URLs and exact commit pins so that existing experiments resolve the same implementations. Their licenses and interfaces are independent of this repository's presentation.

The reproduction guide preserves its `phasesca` container and directory names for compatibility. Complete reproduction requires external datasets, some measured in tens of gigabytes, plus the specified analysis environment. The publication checks did not download these datasets or initialize device firmware.

[Preservation and verification](COMPATIBILITY.md) distinguishes source checks from experimental reproduction.

## Source terms

First-party source is available under the [MIT license](LICENSE). Separate bundled components and external modules retain their own terms.
