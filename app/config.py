# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/config.py

from pathlib import Path

BASE_DIR = Path("/app/jobs")

DEFAULT_CHARGE = 0
DEFAULT_UHF = 0
DEFAULT_GFN = 1


XTB_EXEC = "/usr/local/bin/xtb"  


OPT_BLOCK = """$opt
tight=0
xtol=0.1
$end
"""
