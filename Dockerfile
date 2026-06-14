FROM python:3.11-slim

LABEL maintainer="AI Art Animator Team"
LABEL description="AI Art Animator - Stroke-level drawing animation system"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml setup.py ./
COPY src/ ./src/
COPY config/ ./config/
COPY README.md LICENSE ./

# Install package
RUN pip install --no-cache-dir -e .

# Create output directory
RUN mkdir -p /outputs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV OUTPUT_DIR=/outputs

# Expose volume for outputs
VOLUME ["/outputs"]

# Default command
CMD ["art-animator", "--help"]
