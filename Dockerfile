# Use base image
FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install base dependencies
RUN apt-get update && apt-get install -y \
    git cmake build-essential gfortran libblas-dev liblapack-dev \
    python3 python3-pip curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Install xtb (compiled from source)
RUN git clone https://github.com/grimme-lab/xtb.git /opt/xtb \
    && cd /opt/xtb && mkdir build && cd build \
    && cmake .. && make -j$(nproc) && make install

# Set xtb path explicitly
ENV PATH="/usr/local/bin:$PATH"

# Create app directory
WORKDIR /app

# Copy project code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
