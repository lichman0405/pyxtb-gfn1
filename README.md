<div align="center">
  <a href="https://github.com/lichman0405/pyxtb-gfn1.git">
    <img src="assets/edit_logo.png" alt="Logo" width="200px">
  </a>

  <h1 align="center">xTB Geometry Optimization API</h1>

  <p align="center">
    一个生产级的 FastAPI 服务，将强大的 xTB 结构分析功能封装为现代化、容器化的 HTTP 端点。
    <br>
    <a href="./README-en.md"><strong>English</strong></a>
    ·
    <a href="https://github.com/lichman0405/pyxtb-gfn1.git/issues">报告 Bug</a>
    ·
    <a href="https://github.com/lichman0405/pyxtb-gfn1.git/issues">提出新特性</a>
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

## 🚀 功能特点

- 支持 `.xyz` 文件上传与优化
- 使用 GFN1-xTB 方法，收敛阈值 `fmax = 0.1`
- 编译安装 xTB，调用方式稳定、快速
- 输出优化后结构、日志、能量信息
- 所有任务自动归档至独立目录（基于 `job_id`）
- 可以直接下载优化后的文件。
- 支持 docker compose 一键部署

---

## 🧪 API 快速测试

Swagger 文档地址：[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📦 安装方式（Docker 推荐）

### 1. 构建镜像

```bash
docker build -t xtbopt-api .
```

### 2. 启动服务

```bash
docker run -d -p 8000:8000 -v $(pwd)/jobs:/app/jobs xtbopt-api
```

> 所有优化任务的输出将保存在 `jobs/` 目录中

---

## 🧠 API 接口说明

### 🔹 POST `/optimize`

提交 `.xyz` 文件并执行优化。

**请求格式：`multipart/form-data`**

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `file` | 文件 | - | `.xyz` 文件 |
| `charge` | int | 0 | 分子总电荷 |
| `uhf` | int | 0 | 非成对电子数 |
| `gfn` | int | 1 | GFN 模型版本（通常使用 1）|

**返回示例：**

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

打包下载优化任务结果（ZIP），包含：

- `input.xyz`
- `xtbopt.xyz`
- `xtbopt.log`
- `meta.json`
- `rich_log.txt`（可选）

---

## 📁 文件结构示意

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

## 🧱 技术栈

- FastAPI
- Python `sh` + `rich`
- Pydantic v2
- xTB (compiled from source)

---

## 🧩 参数说明

- **GFN1-xTB**：相较于 GFN2-xTB，收敛率更高，推荐用于 MOF、偏离平衡结构优化
- **收敛阈值**：使用 `$opt` 控制块，`fmax = 0.1`，通过 `input` 文件传入

---

## ⚠️ 注意事项

- 本服务为同步阻塞优化，请合理控制请求频率
- 所有上传数据与优化结果将保存在服务器本地
- 日志信息仅写入服务器，不直接随接口返回

---

## 🧑‍💻 示例（使用 curl）

```bash
curl -X POST http://localhost:8000/optimize \
  -F "file=@input.xyz" \
  -F "charge=0" \
  -F "uhf=0" \
  -F "gfn=1"
```

---

## 📄 License

MIT License