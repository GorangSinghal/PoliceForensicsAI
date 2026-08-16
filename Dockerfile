# Use official Python 3.10 slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Set work directory
WORKDIR /app

# Install system dependencies for OpenCV and BasicSR
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
# Note: BasicSR and GFPGAN sometimes require numpy and cython beforehand, but standard pip install usually handles it
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project including weights and assets
COPY . /app/

# Expose Gradio default port
EXPOSE 7860

# Command to run the application
CMD ["python", "src/app.py"]
