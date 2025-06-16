# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

import random
import string
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile

BASE_DIR = Path("jobs")


def generate_job_id() -> str:
    """Generate a unique job ID consisting of:
    'xtb_' + 8 random characters + current datetime string.

    Returns:
        str: A unique job ID, e.g., xtb_ab12cd34_20250519_153005
    """
    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"xtb_{rand}_{timestamp}"


def create_job_dir(job_id: str) -> Path:
    """Create a working directory for the given job ID under jobs/.

    Args:
        job_id (str): The unique job identifier.

    Returns:
        Path: The path to the created job directory.
    """
    job_path = BASE_DIR / job_id
    job_path.mkdir(parents=True, exist_ok=False)
    return job_path


def save_uploaded_file(file: UploadFile, save_path: Path) -> None:
    """Save uploaded .xyz file to the specified path.

    Args:
        file (UploadFile): The uploaded file from the API.
        save_path (Path): The destination path to save the file.

    Returns:
        None
    """
    with open(save_path, "wb") as f:
        content = file.file.read()
        f.write(content)
