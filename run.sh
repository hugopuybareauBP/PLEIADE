#!/bin/bash

source env_pleiade/bin/activate
export PYTHONPATH=$(pwd)

# Launch backend
python backend/app/main.py &

# Launch frontend
cd frontend
npm run dev
