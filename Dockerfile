FROM python:3.11-slim

WORKDIR /app

# Копируем requirements.txt из backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем app.py из backend
COPY backend/app.py .

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]

