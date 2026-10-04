# Stage 1: Builder
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Enable bytecode compilation and direct file copy for independence
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies before project for layer caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev --extra workflow

# Copy the rest of the source code and install the project itself
COPY . /app
RUN uv sync --frozen --no-dev --extra workflow

# Stage 2: Runtime
FROM python:3.12-slim

# Install git for the reproducible run manifest
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the virtual environment and source code from the builder stage
COPY --from=builder /app /app

# Add the virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Default entrypoint and command
ENTRYPOINT ["rnax"]
CMD ["analyze", "--config", "config/pasilla.yaml"]
