# PhaseTrace

Experiment scripts, figures and dataset recipes for analyzing phase-modulated electromagnetic measurements.

![Stored nRF52 phase-rotation traces from the reproduction guide](docs/2025-01-23_tches-artifact/gfx/24-07-04_nrf52-ref_attack_filt_lh1e6_0_phr.png)

The plotted, aligned phase-rotation traces are a retained figure from the [nRF52 artifact guide](docs/2025-01-23_tches-artifact/README.md), not a new experimental run. The guide explains the measured input, processing and attack workflow; complete reproduction needs its external datasets and environment.

## Explore the workspace

| Location | Purpose |
| --- | --- |
| `expe/` | Experiment-specific analysis scripts, stored arrays and figures |
| `sets/` | Dataset definitions and supporting files |
| `src/` | Dataset utility scripts |
| `mods/` | Pinned external firmware, analysis and recording modules |
| [Reproduction guide](docs/2025-01-23_tches-artifact/README.md) | Existing container workflow and dataset references |

## Source checkout

Developed locally using Git before publication. The GitHub upload date does not indicate when this work began.

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
