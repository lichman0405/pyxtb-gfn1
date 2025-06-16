
<div align="center">
  <a href="https://github.com/lichman0405/pyxtb-gfn1.git">
    <img src="assets/edit_logo.png" alt="Logo" width="200px">
  </a>

  <h1 align="center">xTB Geometry Optimization API</h1>

  <p align="center">
    A production-ready FastAPI service that wraps the powerful xTB structure optimization capabilities as modern, containerized HTTP endpoints.
    <br>
    <a href="./README.md"><strong>中文</strong></a>
    ·
    <a href="https://github.com/lichman0405/pyxtb-gfn1.git/issues">Report Bugs</a>
    ·
    <a href="https://github.com/lichman0405/pyxtb-gfn1.git/issues">Request Features</a>
  </p>
</div>

<div align="center">


[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker)
[![GitHub issues](https://img.shields.io/github/issues/lichman0405/pyxtb-gfn1.svg)](https://github.com/lichman0405/pyxtb-gfn1/issues)
[![GitHub stars](https://img.shields.io/github/stars/lichman0405/pyxtb-gfn1.svg?style=social)](https://github.com/lichman0405/pyxtb-gfn1.git)

</div>

---

## 🚀 Features

- Supports `.xyz` file upload and geometry optimization
- Uses the GFN1-xTB method with convergence threshold `fmax = 0.1`
- Compiles and installs xTB from source for stable and fast execution
- Outputs optimized structure, log, and energy information
- All tasks are archived in separate folders based on `job_id`
- Direct download of the optimized files is available
- Supports one-click deployment via Docker Compose

---

## 🧪 Quick API Test

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📦 Installation (Docker Recommended)

### 1. Build the Docker image

```bash
docker build -t xtbopt-api .
```

### 2. Run the container

```bash
docker run -d -p 8000:8000 -v $(pwd)/jobs:/app/jobs xtbopt-api
```

> All task outputs will be stored in the `jobs/` directory.

---

## 🧠 API Endpoints

### 🔹 POST `/optimize`

Submit a `.xyz` file for geometry optimization.

**Request format: `multipart/form-data`**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `file` | file | - | `.xyz` file |
| `charge` | int | 0 | Total molecular charge |
| `uhf` | int | 0 | Number of unpaired electrons |
| `gfn` | int | 1 | GFN model version (usually 1) |

**Example response:**

```json
{
  "job_id": "xtb_ab12cd34_20250519_162314",
  "status": "success",
  "energy": -305.2381,
  "gradient_norm": null,
  "message": "Optimization complete.",
  "download_url": "/download/xtb_ab12cd34_20250519_162314",
  "log_url": "/download/xtb_ab12cd34_20250519_162314/log"
}
```

---

### 🔹 GET `/download/{job_id}`

Download a ZIP archive of the optimization task results, including:

- `input.xyz`
- `xtbopt.xyz`
- `xtbopt.log`
- `meta.json`
- `rich_log.txt` (optional)

---

## 📁 Directory Structure

```
jobs/
└── xtb_ab12cd34_20250519_162314/
    ├── input.xyz
    ├── xtbopt.xyz
    ├── xtbopt.log
    ├── meta.json
    └── rich_log.txt
```

---

## 🧱 Tech Stack

- FastAPI
- Python `sh` + `rich`
- Pydantic v2
- xTB (compiled from source)

---

## 🧩 Parameter Notes

- **GFN1-xTB**: Compared to GFN2-xTB, it often converges faster and is recommended for MOFs or highly distorted structures.
- **Convergence threshold**: Uses the `$opt` control block with `fmax = 0.1`, passed via the input file.

---

## ⚠️ Notes

- This service performs synchronous blocking optimizations. Please control request frequency accordingly.
- All uploaded data and results are stored locally on the server.
- Log information is written to the server only and not included directly in API responses.

---

## 🧑‍💻 Example (using curl)

```bash
curl -X POST http://localhost:8000/optimize   -F "file=@input.xyz"   -F "charge=0"   -F "uhf=0"   -F "gfn=1"
```

---

## 📄 License

MIT License
