#!/bin/bash
cd "$(dirname "$0")"
source env/bin/activate
python3 collect_data_from_nse.py
