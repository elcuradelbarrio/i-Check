from difflib import SequenceMatcher
import re

async def detect_plagiarism(text: str, reference_texts: list = None) -> dict:
    """
    Detecta plagio comparando el texto con referencias.
    Si no hay referencias, usa heurísticas básicas.
    """
    if not reference_texts:
        # Sin referencias, usar análisis básico de patrones
        return _local_plagiarism_check(text)
    
    # Comparar contra textos de referencia
    similarities = []
    for ref_text in reference_texts:
        similarity = _calculate_similarity(text, ref_text)
        similarities.append(similarity)
    
    max_similarity = max(similarities) if similarities else 0
    
    return {
        "plagiarism_percentage": int(max_similarity * 100),
        "method": "reference_comparison",
        "matches_found": len([s for s in similarities if s > 0.7]),
        "confidence": "high" if max_similarity > 0.5 else "medium"
    }

def _calculate_similarity(text1: str, text2: str) -> float:
    """Calcula similitud usando SequenceMatcher (cosine similarity)"""
    text1_clean = _normalize_text(text1)
    text2_clean = _normalize_text(text2)
    
    matcher = SequenceMatcher(None, text1_clean, text2_clean)
    return matcher.ratio()

def _normalize_text(text: str) -> str:
    """Normaliza texto removiendo espacios y signos"""
    text = text.lower()
    text = re.sub(r'[^a-záéíóúñ\s]', '', text)
    text = ' '.join(text.split())
    return text

def _local_plagiarism_check(text: str) -> dict:
    """
    Análisis básico sin referencias.
    Detecta características sospechosas de plagio.
    """
    indicators = 0
    
    # Check: Citas incorrectamente integradas
    if '\"' in text and text.count('\"') > text.count('\n'):
        indicators += 5
    
    # Check: Saltos temáticos abruptos
    sentences = text.split('.')
    if len(sentences) > 5:
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
        for sentence in sentences:
            if len(sentence.split()) > avg_length * 2:
                indicators += 3
    
    # Check: Inconsistencia de vocabulario
    words = text.split()
    if len(set(words)) < len(words) * 0.3:  # Poca variedad de palabras
        indicators += 10
    
    return {
        "plagiarism_percentage": min(indicators, 100),
        "method": "heuristic",
        "confidence": "low",
        "note": "Sin textos de referencia. Resultado basado en patrones."
    }
