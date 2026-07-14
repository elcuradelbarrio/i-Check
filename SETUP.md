# i-Check Setup Guide

## Opción 1: Local (Development)

### Requirements
- Python 3.11+
- pip

### Steps

```bash
# 1. Clonar/Descargar repo
cd i-check

# 2. Setup Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configurar .env
cp .env.example .env
# Editar .env y agregar OPENAI_API_KEY

# 4. Ejecutar Backend
python main.py
# Accede a http://localhost:8000/docs

# 5. En otra terminal, servir Frontend
cd ../frontend
# Opción A: Python simple server
python -m http.server 3000

# Opción B: npm + vite (si tienes Node)
npm install
npm run dev
```

Accede a http://localhost:3000

## Opción 2: Docker

```bash
# 1. Setup .env
cp .env.example .env
# Editar .env con tus keys

# 2. Docker Compose
docker-compose up

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## Requisitos

- OpenAI API Key (para detección de IA con GPT)
- JWT Secret (auto-generado en .env)

## Testing

### 1. Registrarse
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

### 2. Subir Documento
```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload?token=YOUR_TOKEN" \
  -F "file=@document.pdf"
```

### 3. Analizar
```bash
curl -X POST "http://localhost:8000/api/v1/analyze?document_id=1&token=YOUR_TOKEN"
```

## Estructura

```
i-check/
├── backend/
│   ├── app/
│   │   ├── api/routes.py          # Endpoints
│   │   ├── services/
│   │   │   ├── ai_detector.py     # OpenAI + heurísticos
│   │   │   └── plagiarism_detector.py
│   │   ├── models.py              # SQLAlchemy
│   │   ├── schemas.py             # Pydantic
│   │   ├── auth.py                # JWT
│   │   ├── database.py
│   │   └── config.py
│   ├── main.py                    # FastAPI app
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── index.html                 # Single page app (Vanilla JS)
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Next Steps

- [ ] Mejorar detector IA (más APIs o modelos ML)
- [ ] Agregar upload de PDF/DOCX
- [ ] Dashboard con historial de análisis
- [ ] Email notifications
- [ ] Pricing tiers
- [ ] Deploy en Railway
