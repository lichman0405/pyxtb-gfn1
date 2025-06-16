# -*- coding: utf-8 -*-
# Author: Shibo Li
# Date: 2025-05-15


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as api_router
from app.logger import logger

app = FastAPI(
    title="xTB Geometry Optimization API",
    description="A lightweight API for structure optimization using GFN1-xTB.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router)

@app.get("/")
def root():
    logger.info("Health check: API is live.")
    return {"message": "xTB Geometry Optimization API is running."}
