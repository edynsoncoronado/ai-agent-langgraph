FROM python:3.12-slim

# --- system deps ---
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# --- install uv ---
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.cargo/bin:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
CMD  ["bash"]