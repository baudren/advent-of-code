#!/bin/bash

day="${1:-$(date +%d)}"
streamlit run --server.runOnSave true day$day.py
