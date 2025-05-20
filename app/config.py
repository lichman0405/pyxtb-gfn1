# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

from pathlib import Path

# base directory to store job data
BASE_DIR: Path = Path("jobs")

# default optimization parameters
DEFAULT_CHARGE: int = 0
DEFAULT_UHF: int = 0
DEFAULT_GFN: int = 1  # GFN1-xTB
DEFAULT_FMAX: float = 0.1

# optimization control block content for fmax = 0.1
OPT_BLOCK: str = """$opt
tight=0
xtol=0.1
$end
"""
