#!/usr/bin/env bash
# iscandar-linux-setup.sh: set up the Iscandar engine on a Linux machine.
#
# Written 2026-11-04 from the steps proven live on telesart the same day:
# the venv package install, the bitstruct and numpy installs, the status.h
# regeneration, the gcc gear build, and the acceptance tests.
#
# Usage:
#   ./iscandar-linux-setup.sh [REPO_DIR] [--oracles]
# REPO_DIR defaults to ~/iscandar (the repo root; the engine files live
# at the root, there is no engine/ subfolder).
#
# With --oracles, the script also regenerates the oracle tables and runs
# the oracle smoke test against them. The tables are about 52 GB and the
# run takes a while (the Center table alone is about 36 GB). They land
# in $ORACLES_OUTDIR, which defaults to ~/workspace/iscandar/oracles,
# the path oracle_smoke_test.py checks by default on Linux.
#
# The script stops at the first failed step and says which one failed.
# It does not touch git state.

set -euo pipefail

REPO_DIR="${1:-$HOME/iscandar}"
WITH_ORACLES="${2:-}"
ORACLES_OUTDIR="${ORACLES_OUTDIR:-$HOME/workspace/iscandar/oracles}"
cd "$REPO_DIR"

echo "== Step 1: system package for Python virtual environments =="
# The venv module needs its matching system package; without it the
# venv creation fails with an ensurepip error. Version-matched name,
# e.g. python3.12-venv on the Ubuntu 24.04 family.
PYV="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
sudo apt install "python${PYV}-venv"

echo "== Step 2: virtual environment and Python packages =="
# bitstruct is the engine's one third-party import (MPUPointer).
# numpy is needed only by the oracle creators, not by the engine.
python3 -m venv .venv
.venv/bin/pip install bitstruct numpy

echo "== Step 3: regenerate status.h from Status.py =="
# Expected output reports 22 codes.
.venv/bin/python gen_status.py

echo "== Step 4: build the gears (the Linux twin of build_gears.bat) =="
# The C sources use __declspec for Windows; the one-line prefix header
# defines it away, and the output keeps the name RowsCheck.dll because
# Gears.py loads that exact filename on every platform.
printf '#define __declspec(x)\n' > /tmp/declspec.h
gcc -shared -fPIC -include /tmp/declspec.h -o RowsCheck.dll \
    RowsCheck.c PlanesCheck.c PairsRowDriver.c PlaneSmallDriver.c \
    LargePlanesDriver.c LargeRowsDriver.c HugePlanesDriver.c \
    HugeRowsDriver.c Mark.c Unmark.c Commit.c

echo "== Step 5: acceptance tests =="
# Expected: 22 tests, OK.
.venv/bin/python test_engine.py

if [ "$WITH_ORACLES" = "--oracles" ]; then
    echo "== Step 6: regenerate the oracle tables (about 52 GB; this takes a while) =="
    mkdir -p "$ORACLES_OUTDIR"
    df -h "$ORACLES_OUTDIR" | tail -1
    .venv/bin/python oracle/creators/src/create_oracles.py all --outdir "$ORACLES_OUTDIR"

    echo "== Step 7: oracle smoke test =="
    .venv/bin/python oracle_smoke_test.py --oracles "$ORACLES_OUTDIR"
fi

echo "Setup complete. The engine is built and tested in $REPO_DIR."
if [ "$WITH_ORACLES" != "--oracles" ]; then
    echo "Oracle tables not built. Rerun with --oracles to regenerate them,"
    echo "or see iscandar-linux-setup.md."
fi
