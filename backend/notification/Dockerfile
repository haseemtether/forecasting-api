# Use a minimal and secure base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Update OS packages and install security updates
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install required system dependencies
RUN apt-get install -y --no-install-recommends gcc musl-dev libffi-dev

# Create a non-root user and set correct permissions
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# Create and activate a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ .

# Expose port (necessary for Kubernetes Service)
EXPOSE 8000

# Set correct permissions for Kubernetes volume mounts (if needed)
RUN chmod -R 755 /app

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
