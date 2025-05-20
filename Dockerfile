FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# 安装基本依赖 + UTF-8 locale
RUN apt-get update && apt-get install -y \
    git cmake build-essential gfortran libblas-dev liblapack-dev \
    python3 python3-pip curl unzip locales \
    && locale-gen en_US.UTF-8

# 设置 UTF-8 编码
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# 安装 xTB from source
RUN git clone https://github.com/grimme-lab/xtb.git /opt/xtb \
    && cd /opt/xtb && mkdir build && cd build \
    && cmake .. && make -j$(nproc) && make install

ENV PATH="/usr/local/bin:$PATH"

# 设置 Python 环境
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir  -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
