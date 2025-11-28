FROM python:3.11-slim

WORKDIR /app

# Installer dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY app ./app

EXPOSE 4000

ENV DATABASE_URL="" 

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "4000"]