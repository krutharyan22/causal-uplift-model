FROM python:3.11-slim

WORKDIR /app

# Install system build tools
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8001"]