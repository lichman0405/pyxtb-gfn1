FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
    build-essential \
    cmake \
    ninja-build \
    gfortran \
    libopenblas-dev \
    pkg-config \
    wget \
    git \
    ca-certificates \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    locales \
    && rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

WORKDIR /opt

RUN git clone https://github.com/grimme-lab/xtb.git && \
    cd xtb && \
    cmake -B_build -S. -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_Fortran_COMPILER=gfortran && \
    ninja -C _build && \
    ninja -C _build install

ENV XTBPATH=/usr/local/share/xtb \
    OMP_STACKSIZE=4G \
    OMP_NUM_THREADS=4 \
    OMP_MAX_ACTIVE_LEVELS=1 \
    MKL_NUM_THREADS=4 \
    PATH="/usr/local/bin:${PATH}"

RUN echo "source /usr/local/share/xtb/config_env.bash" >> /etc/bash.bashrc

WORKDIR /app

COPY . /app

RUN python3 -m venv /venv
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
