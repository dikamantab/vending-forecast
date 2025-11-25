FROM python:3.10


WORKDIR /app


RUN apt-get update && apt-get install -y build-essential libpq-dev wget curl git \
&& rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


ENV PYTHONUNBUFFERED=1


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]