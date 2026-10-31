#!/usr/bin/env bash
# aarch64 reproduction of the NH-01 N = 1 000 runs (protocol.md, sections 3-9).
# One attempt = one new WORK directory with one fresh clone per run, so no
# earlier results/ or cells.jsonl.gz can be reused. Technical failures stop
# the script; checker verdicts (exit 0-3) are captured, never treated as errors.
#
# Required environment (absolute paths):
#   WORK       new attempt directory (must not exist)
#   COMMIT     freeze commit of the protocol (full SHA)
#   PYBIN      the reviewed CPython 3.12 interpreter
#   CORES_C / CORES_R  taskset CPU lists for confirmatory / correlated
#   END_EPOCH  end of access, Unix seconds
# Optional: RUNS="confirmatory correlated" (a restart may name one run),
#   EXPECTED_PY=3.12.15, REPO_URL.
set -euo pipefail
: "${WORK:?}" "${COMMIT:?}" "${PYBIN:?}" "${CORES_C:?}" "${CORES_R:?}" "${END_EPOCH:?}"
RUNS=${RUNS:-confirmatory correlated}
EXPECTED_PY=${EXPECTED_PY:-3.12.15}
REPO_URL=${REPO_URL:-https://github.com/hypneum-lab/rescience-nh01.git}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
[ ! -e "$WORK" ] || { echo "WORK exists: refuse" >&2; exit 64; }
mkdir -p "$WORK/record"
R="$WORK/record"
log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$R/driver.log"; }
declare -A WALL_CAP=([confirmatory]=28800 [correlated]=43200)   # runner caps (8 h, 12 h)
declare -A TASKS=([confirmatory]=10 [correlated]=30)
declare -A README_W=([confirmatory]=4 [correlated]=2)
declare -A CORES=([confirmatory]=$CORES_C [correlated]=$CORES_R)

log "attempt start commit $COMMIT runs: $RUNS"
{ uname -a; getconf PAGESIZE; lscpu; nproc; env | sort; } > "$R/host.txt" 2>&1
for run in $RUNS; do
  git clone -q "$REPO_URL" "$WORK/$run"
  git -C "$WORK/$run" checkout -q "$COMMIT"
  git -C "$WORK/$run" diff --quiet submission-20261031 HEAD -- code/ data/ article/
  (cd "$WORK/$run/code" && shasum -a 256 -c CODE_SHA256_AT_TAG.txt) >> "$R/manifests.txt"
  (cd "$WORK/$run/data" && shasum -a 256 -c MANIFEST.sha256) >> "$R/manifests.txt"
done
FIRST=$(echo "$RUNS" | awk '{print $1}')
P="$WORK/$FIRST/docs/prereg/arm-reproduction"

"$PYBIN" -m venv "$WORK/venv"
PY="$WORK/venv/bin/python"
"$PY" -m pip install -q --no-input --require-hashes -r "$P/requirements-aarch64.lock"
"$PY" -VV > "$R/python.txt"
"$PY" -c "import platform,sys; assert platform.python_version()=='$EXPECTED_PY', platform.python_version(); assert platform.machine()=='aarch64'"
"$PY" -m pip freeze > "$R/pip-freeze.txt"
"$PY" -c "import numpy; numpy.show_config()" > "$R/numpy-config.txt" 2>&1
# native-library smoke on 64 KiB pages: linalg and a headless figure
"$PY" - <<'EOF' > "$R/native-smoke.txt"
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
a = np.random.default_rng([20261025, 0]).standard_normal((200, 200)); a = a + a.T
w, v = np.linalg.eigh(a)
assert np.allclose(v @ np.diag(w) @ v.T, a, atol=1e-9)
plt.plot([0, 1]); plt.savefig("/dev/null", format="png")
print("rng witness", np.random.default_rng([20261025, 0, 1000, 0]).random(4).tolist())
print("ok")
EOF
(cd "$WORK/$FIRST/code" && PYTHONPATH=. "$PY" -m pytest -q tests/) > "$R/pytest.txt" 2>&1

workers_for() {  # run -> README count, or one task per worker if the probe projects > half the cap
  local run=$1 out="$R/probe-$1.json" per
  (cd "$WORK/$run/code" && PYTHONPATH=. "$PY" -m "experiments.nh01_hopfield_dream.$run" --probe) > "$out"
  # total task-seconds projected by the runner's own probe
  per=$("$PY" -I -c "import json,sys; d=json.load(open(sys.argv[1]));
print(int(d['projected_task_seconds']*10) if sys.argv[2]=='confirmatory'
      else int(d['projected_total_hours_2_workers']*2*3600))" "$out" "$run")
  local w=${README_W[$run]}
  if [ $(( per / w )) -gt $(( ${WALL_CAP[$run]} / 2 )) ]; then w=${TASKS[$run]}; fi
  echo "$w $per"
}

declare -A PIDS W
need=0
for run in $RUNS; do
  read -r w per < <(workers_for "$run"); W[$run]=$w
  log "probe $run: projected task-seconds $per, workers $w"
  t=$(( per / w )); [ "$t" -gt "$need" ] && need=$t
done
[ $(( $(date +%s) + 3 * need / 2 )) -le $(( END_EPOCH - 7200 )) ] \
  || { log "time rule: not started (needs ~${need}s x 1.5)"; exit 0; }

for run in $RUNS; do
  log "start $run workers ${W[$run]} cores ${CORES[$run]}"
  (cd "$WORK/$run/code" && PYTHON="$PY" exec taskset -c "${CORES[$run]}" ./run.sh "$run" "${W[$run]}") \
    > "$R/run-$run.log" 2>&1 &
  PIDS[$run]=$!
done
declare -A RC
for run in $RUNS; do
  set +e; wait "${PIDS[$run]}"; RC[$run]=$?; set -e
  log "end $run rc=${RC[$run]}"
done

declare -A V
for run in $RUNS; do
  res="$WORK/$run/code/results/nh01_$run"
  if [ "${RC[$run]}" != 0 ] || grep -q "wall-time cap reached" "$R/run-$run.log"; then
    log "$run: runner failed or hit its wall cap -> NO_RESULT"; V[$run]=3; continue
  fi
  if [ -e "$res/cells.jsonl.gz" ]; then log "$run: stale cells.jsonl.gz -> NO_RESULT"; V[$run]=3; continue; fi
  gzip -k "$res/cells.jsonl"
  (cd "$WORK/$run/code" && "$PY" -I scripts/compare_nh01.py "../data/nh01_$run" "results/nh01_$run" "$R/cmp-$run.json") \
    > "$R/cmp-$run.log" 2>&1 || log "$run: compare_nh01 failed (descriptive only, e.g. no figure)"
  set +e
  "$PY" -I "$P/check_arm_repro.py" "nh01_$run" "$WORK/$run/data/nh01_$run" "$res" \
    "$R/verdict-$run.json" --manifest "$WORK/$run/data/MANIFEST.sha256" >> "$R/verdict.log"
  V[$run]=$?; set -e
  log "$run: checker exit ${V[$run]}"
done
# study outcome: NOT_REPRODUCED > NO_RESULT > INCONCLUSIVE_STRICT > REPRODUCED
study=REPRODUCED
for run in $RUNS; do case ${V[$run]} in
  2) study=NOT_REPRODUCED ;;
  3|4) [ "$study" != NOT_REPRODUCED ] && study=NO_RESULT ;;
  1) [ "$study" = REPRODUCED ] && study=INCONCLUSIVE_STRICT ;;
esac; done
log "study outcome for runs [$RUNS]: $study"
(cd "$WORK" && find record */code/results -type f ! -name 'SHA256SUMS*' | LC_ALL=C sort | xargs sha256sum > record/SHA256SUMS.tmp && mv record/SHA256SUMS.tmp record/SHA256SUMS)
log "attempt done"
