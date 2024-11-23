# Then, use a final image without uv
FROM python:3.12-slim-bookworm

# Install uv
RUN pip install uv

# Set the working directory
WORKDIR /app

# Copy the source code
COPY uv.lock README.md pyproject.toml /app/

# Copy the source code
COPY src /app/src

# Install the dependencies
RUN uv sync --frozen

# Run the FastAPI application by default
CMD ["uv", "run", "src/needle/"]