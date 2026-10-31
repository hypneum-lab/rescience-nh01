# Hashed aarch64 requirements — review summary (NH-01 reproduction)

For the PI's HITL review before access. Generated 2026-10-31 on electron-server (uv 0.13.5, metadata and wheels only, nothing installed or built), Python 3.12, `aarch64-manylinux_2_35`, `--exclude-newer 2026-10-17` (no file newer than two weeks).

**Every package has an aarch64 or pure-Python wheel; none is built from source.** One declared change: `python-dateutil` 3.0.0 of the reference run (published 2026-10-21) is newer than the cutoff, so 2.9.0.post0 is used (matplotlib dependency only; no `tzdata`).

### `requirements-gb300-nh01-arm.txt`

| package | version | source | file | latest upload |
|---|---|---|---|---|
| contourpy | 1.4.0 | aarch64 wheel | `contourpy-1.4.0-cp312-cp312-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl` | 2026-09-11 |
| cycler | 0.12.1 | pure-Python wheel | `cycler-0.12.1-py3-none-any.whl` | 2023-10-07 |
| fonttools | 4.67.0 | aarch64 wheel | `fonttools-4.67.0-cp312-cp312-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl` | 2026-10-14 |
| iniconfig | 2.3.1 | pure-Python wheel | `iniconfig-2.3.1-py3-none-any.whl` | 2026-10-06 |
| kiwisolver | 1.5.1 | aarch64 wheel | `kiwisolver-1.5.1-cp312-cp312-manylinux_2_24_aarch64.manylinux_2_28_aarch64.whl` | 2026-08-28 |
| matplotlib | 3.11.2 | aarch64 wheel | `matplotlib-3.11.2-cp312-cp312-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl` | 2026-09-11 |
| numpy | 2.5.4 | aarch64 wheel | `numpy-2.5.4-cp312-cp312-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl` | 2026-10-10 |
| packaging | 26.3 | pure-Python wheel | `packaging-26.3-py3-none-any.whl` | 2026-08-04 |
| pillow | 13.0.0 | aarch64 wheel | `pillow-13.0.0-cp312-cp312-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl` | 2026-10-16 |
| pluggy | 1.7.0 | pure-Python wheel | `pluggy-1.7.0-py3-none-any.whl` | 2026-10-15 |
| pygments | 2.21.0 | pure-Python wheel | `pygments-2.21.0-py3-none-any.whl` | 2026-08-17 |
| pyparsing | 3.3.3 | pure-Python wheel | `pyparsing-3.3.3-py3-none-any.whl` | 2026-09-20 |
| pytest | 9.1.1 | pure-Python wheel | `pytest-9.1.1-py3-none-any.whl` | 2026-06-19 |
| python-dateutil | 2.9.0.post0 | pure-Python wheel | `python_dateutil-2.9.0.post0-py2.py3-none-any.whl` | 2024-03-01 |
| six | 1.17.0 | pure-Python wheel | `six-1.17.0-py2.py3-none-any.whl` | 2024-12-04 |
