FROM python:3.10-slim

# Prevent Python from buffering output
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Disable uvloop/httptools (Railway often incompatible)
ENV UVICORN_LOOP=asyncio
ENV UVICORN_HTTP=auto

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "asyncio"]


# FROM python:3.10-slim

# # Set workdir
# WORKDIR /app

# # Install dependencies for mysqlclient & other common needs
# RUN apt-get update && \
#     apt-get install -y \
#         build-essential \
#         default-libmysqlclient-dev \
#         pkg-config \
#         git \
#     && rm -rf /var/lib/apt/lists/*

# # Copy & install Python deps
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy project
# COPY . .

# # Environment
# ENV PYTHONUNBUFFERED=1

# # Run app
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]