# Use a more robust base image with build tools
FROM python:3.10-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_TIMEOUT=100 \
    PIP_DEFAULT_TIMEOUT=100

# Set working directory
WORKDIR /app

# Install system dependencies for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies first (for caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir --retries 5 -r requirements.txt

# Copy project code
COPY . ./

# Create a non-root user and switch
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose port 8000
EXPOSE 8000

# Start the application with Gunicorn
CMD ["gunicorn", "messaging_app.wsgi:application", "--bind", "0.0.0.0:8000"]