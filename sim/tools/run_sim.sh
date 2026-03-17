#!/bin/bash

cd ~/psc

# 仮想環境があれば有効化
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

python3 sim/psc_sim.py

echo "simulation done"#!/bin/bash

cd ~/psc
source .venv/bin/activate

python3 sim/psc_sim.py

echo "simulation done"
