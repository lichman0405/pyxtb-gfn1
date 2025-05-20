# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15

# app/main.py
# This file defines the FastAPI application entry point.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as api_router
from app.logger import logger

app = FastAPI(
    title="xTB Geometry Optimization API",
    description="A lightweight API for structure optimization using GFN1-xTB.",
    version="1.0.0"
)

# Allow CORS for all origins (for development use)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount the main router
app.include_router(api_router)

# Optional: root endpoint
@app.get("/")
def root():
    logger.info("Health check: API is live.")
    return {"message": "xTB Geometry Optimization API is running."}
