# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/api.py
# This file defines the FastAPI routes for geometry optimization and result download.

import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from app.logger import logger
from app.schemas import OptimizeParams, OptimizeResponse, ErrorResponse
from app.core import run_xtb_optimization
from app.config import BASE_DIR

router = APIRouter()


@router.post("/optimize", response_model=OptimizeResponse, responses={400: {"model": ErrorResponse}})
async def optimize(
    file: UploadFile = File(...),
    charge: int = Form(0),
    uhf: int = Form(0),
    gfn: int = Form(1)
):
    """Run geometry optimization using uploaded .xyz file."""
    try:
        contents = await file.read()
        result = run_xtb_optimization(
            file_bytes=contents,
            charge=charge,
            uhf=uhf,
            gfn=gfn
        )
        if result.get("status") == "error":
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": result["message"],
                    "error": result.get("error", "Unknown error")
                }
            )
        return result
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
    """Download all result files as a ZIP archive."""
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
