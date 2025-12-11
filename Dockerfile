FROM python:3.12-slim-bookworm

# Set the working directory
WORKDIR /app

# Basic utils for easier debugging
RUN apt-get update && apt-get install -y \
    iputils-ping \
    procps \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Create directories for pip
RUN mkdir -p /app/.pip_cache
RUN mkdir -p /app/.pip_packages

# Set environment variables for pip to store packages locally
ENV PIP_CACHE_DIR=/app/.pip_cache
ENV PIP_TARGET=/app/.pip_packages
ENV PYTHONPATH=/app:/app/.pip_packages:$PYTHONPATH
ENV PATH=/app/.pip_packages/bin:$PATH

# Copy and set up entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
