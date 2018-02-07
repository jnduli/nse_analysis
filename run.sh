#!/bin/bash
echo "$(dirname "$0")"
cd "$(dirname "$0")"
pwd
source env/bin/activate
python3 collect_data_from_nse.py
