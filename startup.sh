#!/bin/bash
python -m pip install -r requirements.txt
python -m streamlit run demo_incentivos.py --server.port 8080 --server.address 0.0.0.0