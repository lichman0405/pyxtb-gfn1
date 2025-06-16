# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-06-16

# app/api.py

import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from app.logger import logger
from app.core import run_xtb_optimization
from app.config import BASE_DIR

router = APIRouter()


@router.post("/optimize")
async def optimize(
    file: UploadFile = File(...),
    charge: int = Form(0),
    uhf: int = Form(0),
    gfn: int = Form(1)
):
    """
    Run geometry optimization using uploaded .xyz file
    and directly return the optimized .xyz with a custom filename.
    """
    try:
        contents = await file.read()

        result = run_xtb_optimization(
            file_bytes=contents,
            filename=file.filename,
            charge=charge,
            uhf=uhf,
            gfn=gfn
        )

        if result.get("status") == "error":
            return JSONResponse(
                status_code=400,
                content=result
            )

        job_id = result["job_id"]
        job_path = BASE_DIR / job_id
        xtbopt = job_path / "xtbopt.xyz"

        input_stem = Path(file.filename).stem  
        opt_filename = f"{input_stem}_opt.xyz"
        opt_file = job_path / opt_filename

        xtbopt.rename(opt_file)

        logger.success(f"Returning optimized file: {opt_filename}")

        return FileResponse(
            path=opt_file,
            filename=opt_filename,
            media_type='text/plain'
        )

    except Exception as e:
        logger.error(f"Exception occurred during optimization: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal server error.",
                "error": str(e)
            }
        )


@router.get("/download/{job_id}")
def download_job_output(job_id: str):
    """
    (Optional) Download all result files as a ZIP archive.
    """
    job_path = BASE_DIR / job_id
    if not job_path.exists():
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "message": f"Job {job_id} not found.",
                "error": "Invalid job ID"
            }
        )

    zip_path = BASE_DIR / f"{job_id}.zip"
    shutil.make_archive(str(zip_path.with_suffix("")), 'zip', job_path)
    return FileResponse(
        path=zip_path,
        media_type='application/zip',
        filename=f"{job_id}.zip"
    )
