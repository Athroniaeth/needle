# Then, use a final image without uv
FROM python:3.12-slim-bookworm

# Set the working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the necessary (fake) files for uv install this allows you to install
# uv without losing the `uv sync` cache after modifying pyproject or README
COPY docker/cache /app/

# Copy the necessary files for uv install
COPY uv.lock /app/

# Install the dependencies
RUN uv sync --frozen

# Copy the source code
COPY src /app/src

# Replace skeleton by content
COPY uv.lock /app/

# Copy dotenv file config
COPY .env /app/

# Run the FastAPI application by default
CMD ["uv", "run", "needle"]