FROM python:3.10-slim

# Install system dependencies (including Tesseract)
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only what's needed for installation
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py query.py extraction.py utils.py ./

# Expose the FastAPI port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
