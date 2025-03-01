# Use a lightweight Python image
FROM python:3.9

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY src/ .

# Expose port and run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
