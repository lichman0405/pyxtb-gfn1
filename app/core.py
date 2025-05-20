# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/core.py
# This module performs geometry optimization using a compiled xTB binary.

import json
from pathlib import Path
from sh import Command, ErrorReturnCode
from app.logger import logger
from app.utils import generate_job_id, create_job_dir
from app.config import BASE_DIR, DEFAULT_CHARGE, DEFAULT_UHF, DEFAULT_GFN, OPT_BLOCK


def run_xtb_optimization(
    file_bytes: bytes,
    charge: int = DEFAULT_CHARGE,
    uhf: int = DEFAULT_UHF,
    gfn: int = DEFAULT_GFN,
    xtb_path: str = "/usr/local/bin/xtb"
) -> dict:
    """Run geometry optimization using compiled xTB.

    Args:
        file_bytes (bytes): Content of the uploaded .xyz file.
        charge (int): Total charge of the system.
        uhf (int): Number of unpaired electrons.
        gfn (int): GFN level (usually 1).
        xtb_path (str): Absolute path to the compiled xTB binary.

    Returns:
        dict: Result info including energy, convergence, and job ID.
    """
    job_id = generate_job_id()
    job_path = create_job_dir(job_id)
    input_xyz = job_path / "input.xyz"
    input_ctl = job_path / "input"
    log_path = job_path / "xtbopt.log"

    # Write input files
    input_xyz.write_bytes(file_bytes)
    input_ctl.write_text(OPT_BLOCK)

    logger.rule(f"Optimization started: {job_id}")
    logger.info(f"xTB binary: {xtb_path}")
    logger.info(f"Charge={charge}, UHF={uhf}, GFN={gfn}")
    logger.info(f"Working directory: {job_path}")

    # Construct xtb command
    xtb = Command(xtb_path)
    cmd = [
        str(input_xyz),
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

    # Try to parse energy
    energy = None
    opt_xyz = job_path / "xtbopt.xyz"
    if opt_xyz.exists():
        try:
            with open(opt_xyz, "r") as f:
                for line in f:
                    if "total energy" in line.lower():
                        energy = float(line.strip().split()[-1])
        except Exception as e:
            logger.warning("Failed to parse energy from output.")

    meta = {
        "job_id": job_id,
        "converged": True,
        "energy": energy,
        "gradient_norm": None,
        "fmax": 0.1
    }
    (job_path / "meta.json").write_text(json.dumps(meta, indent=2))

    return {
        "job_id": job_id,
        "status": "success",
        "energy": energy,
        "gradient_norm": None,
        "message": "Optimization complete.",
        "download_url": f"/download/{job_id}",
        "log_url": f"/download/{job_id}/log"
    }
