# PhaseTrace preservation record

## Change boundary

The repository presentation, documentation entry points and source comments were updated. Existing executable entry points, algorithms, defaults, filenames, formats and numerical operations remain unchanged. First-party licensing is MIT under nazeeh111. Separate bundled-component terms and external submodule notices are retained.

## Verified locally

All 42 Python files passed parsing with baseline-identical executable syntax trees. All 52 shell scripts passed `bash -n`. The three external modules retain their exact Git commit references and URLs but were not initialized. Large external datasets, device firmware and full experiment reproduction were not exercised.

The source comparison checks Python syntax trees without comments or source locations, so changes in documentation do not obscure computational changes. This is an equivalence check against the supplied source, not a claim that every experiment is correct or portable. Existing invalid-escape warnings in legacy Python strings also occur in the baseline and were not changed.

The container recipe now retrieves this repository while explicitly retaining the existing `phasesca` directory name. External dependency URLs and pinned submodules remain unchanged. The container was not built.

## Execution boundary

No RF transmission, signal acquisition, connected-device commands, firmware changes or live-target experiments were performed. No external experimental datasets were downloaded. Build and reproduction requirements remain those documented by the source; absent dependencies have not been silently replaced with new algorithms.
