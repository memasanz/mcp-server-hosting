# syntax=docker/dockerfile:1.7-labs
# Build a small image that uses uv for dependency management only
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install uv (package manager)
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install the application dependencies
RUN uv venv --python "/usr/local/bin/python3.12" && \
    uv sync --no-cache

# Copy the application code
COPY app ./app

# Activate venv by default
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Expose default port
EXPOSE 8000

# Run the MCP server with uvicorn from venv
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
