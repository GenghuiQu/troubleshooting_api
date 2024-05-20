FROM python:3.8-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libtesseract-dev \
    libleptonica-dev \
    poppler-utils \
    && apt-get clean

# Set environment variables
ENV LOG_FILENAME=/app/logs/app.log

# Set working directory
WORKDIR /app

# Copy dependency file and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Define mount point
VOLUME ["/app/logs"]

# Run Flask application
CMD ["python", "app.py"]
