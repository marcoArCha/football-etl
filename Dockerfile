# Base image — official Python 3.11 slim (smaller size, faster to download)
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (Docker caching trick)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Run the pipeline
CMD ["python", "-m", "src.pipeline"]