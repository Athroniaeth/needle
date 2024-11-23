# Then, use a final image without uv
FROM python:3.12-slim-bookworm

# Set the working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the source code
COPY src /app/src

# Copy the necessary files for uv install
COPY uv.lock README.md pyproject.toml /app/

# Install the dependencies
RUN uv sync --frozen

# Run the FastAPI application by default
CMD ["uv", "run", "needle", "hello-world"]