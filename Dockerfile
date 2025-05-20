FROM debian:bullseye

# 安装基础依赖和编译工具
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

# 设置环境变量
ENV XTBPATH=/usr/local/share/xtb \
    OMP_STACKSIZE=4G \
    OMP_NUM_THREADS=4 \
    OMP_MAX_ACTIVE_LEVELS=1 \
    MKL_NUM_THREADS=4 \
    PATH="/usr/local/bin:${PATH}"

# 可选：配置默认 shell 环境
RUN echo "source /usr/local/share/xtb/config_env.bash" >> /etc/bash.bashrc

# 设置 API 服务工作目录
WORKDIR /app

# 复制 Python 项目代码
COPY . /app

# 安装 Python 依赖
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# 启动 FastAPI 服务
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
