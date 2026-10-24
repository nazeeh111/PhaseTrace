# PhaseTrace preservation record

## Change boundary

The initial presentation revision updated documentation entry points and source comments while preserving executable behavior. A later correction adds the omitted `lh1e6` argument to the first training-filter call in `sets/24-07-04_nrf52-ref/src/process.sh`. That selector already appears in the original training reproduction guide and downstream environment. Filter implementations, other recipe commands, filenames and data formats are unchanged. First-party licensing is MIT under nazeeh111. Separate bundled-component terms and external submodule notices are retained.

## Verified locally

For the initial presentation revision, all 42 retained Python files passed parsing with baseline-identical executable syntax trees, and all 52 shell scripts passed `bash -n`. Those historical checks do not assert that every later source revision is identical. The three external modules retain their exact Git commit references and URLs but were not initialized. Large external datasets, device firmware and full experiment reproduction were not exercised.

The source comparison checks Python syntax trees without comments or source locations, so changes in documentation do not obscure computational changes. This is an equivalence check against the supplied source, not a claim that every experiment is correct or portable. Existing invalid-escape warnings in legacy Python strings also occur in the baseline and were not changed.

The container recipe now retrieves this repository while explicitly retaining the existing `phasesca` directory name. External dependency URLs and pinned submodules remain unchanged. The container was not built.

For the filter-argument correction, isolated checks executed the actual shell recipe and callee with inert command, configuration and filtering substitutes. The original first call failed before filtering; the corrected recipe supplied all eight documented selectors in order. The other seven filter calls and non-filter commands matched. The new `tests/test_process_recipe.py` regression passed. These are orchestration checks, not numerical filtering, training or experiment reproduction. The shell still has its existing non-fail-fast exit behavior.

## Execution boundary

No RF transmission, signal acquisition, connected-device commands, firmware changes or live-target experiments were performed. No external experimental datasets were downloaded. Build and reproduction requirements remain those documented by the source; absent dependencies have not been silently replaced with new algorithms.
