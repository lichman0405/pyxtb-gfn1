# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/core.py

import json
import re
from sh import Command, ErrorReturnCode
from app.logger import logger
from app.utils import generate_job_id, create_job_dir
from app.config import DEFAULT_CHARGE, DEFAULT_UHF, DEFAULT_GFN, OPT_BLOCK, XTB_EXEC


def run_xtb_optimization(
    file_bytes: bytes,
    filename: str,
    charge: int = DEFAULT_CHARGE,
    uhf: int = DEFAULT_UHF,
    gfn: int = DEFAULT_GFN,
    xtb_path: str = XTB_EXEC
) -> dict:
    """
    Run xTB optimization on the uploaded file.
    """
    job_id = generate_job_id()
    job_path = create_job_dir(job_id)
    input_xyz = job_path / filename
    input_ctl = job_path / "input"
    log_path = job_path / "xtbopt.log"

    input_xyz.write_bytes(file_bytes)
    input_ctl.write_text(OPT_BLOCK)

    logger.rule(f"Optimization started: {job_id}")
    logger.info(f"xTB binary: {xtb_path}")
    logger.info(f"Charge={charge}, UHF={uhf}, GFN={gfn}")
    logger.info(f"Working directory: {job_path}")

    xtb = Command(xtb_path)
    cmd = [
        filename,
        "--opt",
        "--gfn", str(gfn),
        "--charge", str(charge),
        "--uhf", str(uhf)
    ]

    try:
        xtb(
            *cmd,
            _cwd=job_path,
            _out=log_path.open("w"),
            _err_to_out=True
        )
        logger.success("xTB optimization completed successfully.")
    except ErrorReturnCode as e:
        logger.error("xTB optimization failed.")
        meta = {
            "job_id": job_id,
            "converged": False,
            "error": str(e)
        }
        (job_path / "meta.json").write_text(json.dumps(meta, indent=2))
        return {
            "job_id": job_id,
            "status": "error",
            "message": "xTB execution failed.",
            "error": str(e)
        }

    # Parse energy and gradient norm from xtbopt.xyz
    energy = None
    gradient = None
    opt_xyz = job_path / "xtbopt.xyz"
    if opt_xyz.exists():
        try:
            with open(opt_xyz, "r") as f:
                for line in f:
                    match_energy = re.search(r"energy:\s*(-?\d+\.\d+)", line.lower())
                    match_gradient = re.search(r"gnorm:\s*(-?\d+\.\d+)", line.lower())
                    if match_energy:
                        energy = float(match_energy.group(1))
                    if match_gradient:
                        gradient = float(match_gradient.group(1))
                    if energy is not None and gradient is not None:
                        break
        except Exception as e:
            logger.warning(f"Failed to parse energy or gradient: {e}")

    meta = {
        "job_id": job_id,
        "converged": True,
        "energy": energy,
        "gradient_norm": gradient,
        "fmax": 0.1
    }
    (job_path / "meta.json").write_text(json.dumps(meta, indent=2))

    return {
        "job_id": job_id,
        "status": "success",
        "energy": energy,
        "gradient_norm": gradient,
        "message": "Optimization complete.",
        "download_url": f"/download/{job_id}",
        "log_url": f"/download/{job_id}/log"
    }
