FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖和工具
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    gfortran \
    libblas-dev \
    liblapack-dev \
    wget \
    git \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    locales \
    && rm -rf /var/lib/apt/lists/*

# 设置 UTF-8 locale
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# 设置工作目录
WORKDIR /opt

# 克隆并编译安装 xTB
RUN git clone https://github.com/grimme-lab/xtb.git && \
    cd xtb && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -j$(nproc) && \
    make install

# 设置环境变量（含 xtb 参数路径、OpenMP 并行控制）
ENV XTBPATH=/usr/local/share/xtb \
    OMP_STACKSIZE=4G \
    OMP_NUM_THREADS=4 \
    OMP_MAX_ACTIVE_LEVELS=1 \
    MKL_NUM_THREADS=4 \
    PATH="/usr/local/bin:${PATH}"

# 可选：配置默认 shell 环境
RUN echo "source /usr/local/share/xtb/config_env.bash" >> /etc/bash.bashrc

# 设置工作目录为项目路径
WORKDIR /app

# 拷贝 FastAPI 项目代码
COPY . /app

# 创建 Python 虚拟环境
RUN python3 -m venv /venv

# 安装 Python 项目依赖到虚拟环境中
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# 显式暴露 API 服务端口
EXPOSE 8000

# 启动 FastAPI 服务，使用虚拟环境中的 uvicorn
CMD ["/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
