# i-Check Backend

## Setup

```bash
pip install -r ../requirements.txt
cp .env.example .env
# Actualiza .env con tus credenciales
```

## Ejecutar

```bash
cd backend
python main.py
```

Accede a: http://localhost:8000/docs

## API Endpoints

### Auth
- POST /api/v1/auth/register
- POST /api/v1/auth/login

### Documents
- POST /api/v1/documents/upload
- GET /api/v1/documents

### Analysis
- POST /api/v1/analyze
- GET /api/v1/results/{document_id}

## Estado

- [x] Setup proyecto
- [x] Detector IA (OpenAI + heurísticos)
- [x] Detector Plagio (SequenceMatcher)
- [x] API FastAPI
- [x] Auth JWT
- [ ] Frontend React
- [ ] Deploy

## Next

Frontend + Deploy
