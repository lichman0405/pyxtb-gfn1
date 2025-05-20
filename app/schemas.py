# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/schemas.py
# This file defines the API input and output data models using Pydantic.

from pydantic import BaseModel, Field
from typing import Optional


class OptimizeParams(BaseModel):
    """Request parameters for /optimize endpoint."""
    charge: int = Field(0, description="Total charge of the system")
    uhf: int = Field(0, description="Number of unpaired electrons")
    gfn: int = Field(1, description="GFN version to use, e.g., 1 for GFN1-xTB")


class OptimizeResponse(BaseModel):
    """Response from /optimize endpoint."""
    job_id: str
    status: str
    energy: Optional[float] = Field(None, description="Final energy (Eh)")
    gradient_norm: Optional[float] = Field(None, description="Final gradient norm (Eh/bohr)")
    message: Optional[str] = Field(None, description="Convergence message or failure reason")
    download_url: str
    log_url: str


class ErrorResponse(BaseModel):
    """Standard error response."""
    status: str = "error"
    message: str
    error: str

if __name__ == "__main__":
    # Example usage
    params = OptimizeParams(charge=0, uhf=1, gfn=1)
    print(params.model_dump_json())
    
    response = OptimizeResponse(
        job_id="12345",
        status="success",
        energy=-76.123,
        gradient_norm=0.001,
        message="Converged successfully",
        download_url="http://example.com/download",
        log_url="http://example.com/log"
    )
    print(response.model_dump_json())
    error_response = ErrorResponse(
        message="An error occurred",
        error="Invalid parameters"
    )
    print(error_response.model_dump_json())
