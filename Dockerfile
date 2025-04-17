FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    python3.12 \
    python3-pip \
    ocl-icd-opencl-dev \
    libssl-dev \
    cmake

WORKDIR /app
COPY . .

RUN mkdir -p /build && cd /build \
    && cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-fopenmp" ../ \
    && make FractalCash

RUN python3 -m venv /opt/fractalenv \
    && /opt/fractalenv/bin/pip install -r requirements.txt pybind11 cryptography pytest

ENV PATH="/opt/fractalenv/bin:$PATH"
CMD ["python", "main.py"]
