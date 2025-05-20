# xTB Geometry Optimization API

基于 FastAPI 的轻量级结构优化服务，使用 GFN1-xTB 力场对 `.xyz` 文件结构进行几何优化。服务封装了编译安装的 [xTB](https://github.com/grimme-lab/xtb) 程序，并通过 REST API 提供高通量优化功能。

---

## 🚀 功能特点

- 支持 `.xyz` 文件上传与优化
- 使用 GFN1-xTB 方法，收敛阈值 `fmax = 0.1`
- 编译安装 xTB，调用方式稳定、快速
- 输出优化后结构、日志、能量信息
- 所有任务自动归档至独立目录（基于 `job_id`）
- 支持结果打包下载
- 支持 Docker 一键部署

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