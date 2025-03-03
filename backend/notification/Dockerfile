# Use a minimal and secure base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Update OS packages and install security updates
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    build-essential libffi-dev python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home appuser

# Ensure the working directory is owned by the non-root user before switching
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Create and activate a virtual environment inside the user home directory
RUN python -m venv /home/appuser/venv
ENV PATH="/home/appuser/venv/bin:$PATH"

# Copy dependencies first for better caching
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code and set correct ownership
COPY --chown=appuser:appuser src/ .

# Expose port (necessary for Kubernetes Service)
EXPOSE 8000

# No need to change permissions explicitly
# Remove `chmod` step as files are copied with correct ownership

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
