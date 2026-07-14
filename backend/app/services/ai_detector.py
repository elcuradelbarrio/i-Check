import openai
from app.config import get_settings
import json

settings = get_settings()
openai.api_key = settings.openai_api_key

async def detect_ai_content(text: str) -> dict:
    """
    Detecta contenido generado por IA usando patrones y APIs.
    Retorna porcentaje de confianza.
    """
    try:
        # Método 1: Usar OpenAI para análisis (más preciso)
        prompt = f"""Analiza el siguiente texto y determina si fue generado por IA.
        
Proporciona SOLO un JSON con este formato (sin explicación adicional):
{{"ai_confidence": <número entre 0-100>, "reasoning": "<breve explicación>"}}

Texto:
{text[:2000]}"""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en detectar texto generado por IA. Responde SOLO con JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        result_text = response.choices[0].message.content
        result = json.loads(result_text)
        
        return {
            "ai_percentage": result.get("ai_confidence", 0),
            "method": "openai",
            "confidence": "high"
        }
    except Exception as e:
        # Fallback: detector básico local
        return {
            "ai_percentage": _local_ai_detection(text),
            "method": "local_heuristic",
            "confidence": "medium",
            "error": str(e)
        }

def _local_ai_detection(text: str) -> float:
    """
    Detector local basado en heurísticas.
    Detecta características típicas de texto generado por IA.
    """
    indicators = 0
    total_checks = 0
    
    # Check: Perfecta puntuación y gramática
    sentences = text.split(".")
    total_checks += 1
    if len([s for s in sentences if s.strip()]) > 3:
        indicators += 0.05
    
    # Check: Ausencia de contracciones
    contractions = ["don't", "can't", "won't", "it's", "that's"]
    if not any(c in text.lower() for c in contractions):
        indicators += 0.1
        
    # Check: Lenguaje formal excesivo
    formal_words = ["furthermore", "moreover", "notwithstanding", "henceforth"]
    if sum(text.lower().count(w) for w in formal_words) > 3:
        indicators += 0.15
    
    # Check: Repetición de palabras clave
    words = text.lower().split()
    if len(words) > 100:
        top_words = [w for w in set(words) if words.count(w) > len(words) * 0.05]
        if len(top_words) > 10:
            indicators += 0.1
    
    # Retornar porcentaje (0-100)
    return min(int(indicators * 100), 100)
