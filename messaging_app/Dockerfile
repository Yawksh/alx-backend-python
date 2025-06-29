# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . /app/

# Create a non-root user and switch
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose port 8000
EXPOSE 8000

# Start the application with Gunicorn
CMD ["gunicorn", "messaging_app.wsgi:application", "--bind", "0.0.0.0:8000"]