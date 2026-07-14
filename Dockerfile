FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app
COPY frontend /app/../frontend

ENV DATABASE_URL=sqlite:///./i_check.db
ENV PORT=8000

CMD ["python", "main.py"]
