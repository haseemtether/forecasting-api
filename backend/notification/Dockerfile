# Use a minimal and secure base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies and update packages securely
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    libffi-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Use non-root user for security
RUN useradd --create-home appuser
USER appuser

# Copy dependencies
COPY requirements.txt ./

# Install dependencies in a virtual environment
RUN python -m venv /home/appuser/venv && \
    /home/appuser/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /home/appuser/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY --chown=appuser:appuser src/ .

# Expose port
EXPOSE 8000

# Use virtual environment for execution
ENV PATH="/home/appuser/venv/bin:$PATH"

# Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
