# Base lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (needed for pandas, numpy, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Upgrade pip and install PyTorch separately for caching
RUN pip install --upgrade pip && \
    pip install torch==2.1.0+cpu --index-url https://download.pytorch.org/whl/cpu --no-cache-dir

# Install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Default command
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
