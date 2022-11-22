#!/bin/bash

find . -name '*.*' | entr python3 day$@.py
