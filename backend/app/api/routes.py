from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import (
    UserRegister, UserLogin, TokenResponse, DocumentUpload, 
    AnalysisResultResponse, DocumentResponse
)
from app import models, auth
from app.services.ai_detector import detect_ai_content
from app.services.plagiarism_detector import detect_plagiarism

router = APIRouter()

# AUTH ENDPOINTS
@router.post("/auth/register", response_model=TokenResponse)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    """Registra nuevo usuario"""
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    hashed_pwd = auth.hash_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = auth.create_access_token(new_user.id)
    return {"access_token": token}

@router.post("/auth/login", response_model=TokenResponse)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login de usuario"""
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = auth.create_access_token(db_user.id)
    return {"access_token": token}

# DOCUMENT ENDPOINTS
@router.post("/documents/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    token: str = None,
    db: Session = Depends(get_db)
):
    """Sube un documento para análisis"""
    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")
    
    user_id = auth.decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    content = await file.read()
    try:
        text_content = content.decode('utf-8')
    except:
        text_content = str(content)
    
    doc = models.Document(
        user_id=user_id,
        filename=file.filename,
        content=text_content
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    return doc

@router.get("/documents", response_model=list[DocumentResponse])
async def get_documents(token: str = None, db: Session = Depends(get_db)):
    """Obtiene documentos del usuario"""
    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")
    
    user_id = auth.decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    docs = db.query(models.Document).filter(models.Document.user_id == user_id).all()
    return docs

# ANALYSIS ENDPOINTS
@router.post("/analyze", response_model=AnalysisResultResponse)
async def analyze_document(
    document_id: int,
    token: str = None,
    db: Session = Depends(get_db)
):
    """Analiza un documento (IA + Plagio)"""
    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")
    
    user_id = auth.decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    doc = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == user_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    # Detectar IA
    ai_result = await detect_ai_content(doc.content)
    ai_percentage = ai_result.get("ai_percentage", 0)
    
    # Detectar Plagio
    plagiarism_result = await detect_plagiarism(doc.content)
    plagiarism_percentage = plagiarism_result.get("plagiarism_percentage", 0)
    
    # Guardar resultados
    result = models.AnalysisResult(
        document_id=document_id,
        ai_percentage=ai_percentage,
        plagiarism_percentage=plagiarism_percentage
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    
    return result

@router.get("/results/{document_id}", response_model=AnalysisResultResponse)
async def get_analysis_result(
    document_id: int,
    token: str = None,
    db: Session = Depends(get_db)
):
    """Obtiene resultados de análisis"""
    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")
    
    user_id = auth.decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Verificar que el documento pertenece al usuario
    doc = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == user_id
    ).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    
    result = db.query(models.AnalysisResult).filter(
        models.AnalysisResult.document_id == document_id
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Análisis no encontrado")
    
    return result
