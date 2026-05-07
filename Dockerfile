# Base Python image
FROM python:3.11-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent buffering
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    build-essential \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Streamlit configuration
RUN mkdir -p /root/.streamlit

RUN echo "\
[server]\n\
headless = true\n\
port = 8501\n\
enableCORS = false\n\
address = '0.0.0.0'\n\
" > /root/.streamlit/config.toml

# Start Streamlit app
CMD ["streamlit", "run", "app.py"]