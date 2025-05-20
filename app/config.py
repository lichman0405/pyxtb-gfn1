# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/config.py

from pathlib import Path

# 工作目录，用于存放任务结果
BASE_DIR = Path("/app/jobs")

# 默认优化参数
DEFAULT_CHARGE = 0
DEFAULT_UHF = 0
DEFAULT_GFN = 1

# xTB 可执行文件路径
XTB_EXEC = "/usr/local/bin/xtb"  # 可通过环境变量覆盖，或修改 Dockerfile 保持一致

# 优化控制块（fmax = 0.1）
OPT_BLOCK = """$opt
tight=0
xtol=0.1
$end
"""
