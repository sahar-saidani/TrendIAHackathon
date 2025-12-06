# app/services/ml_integration.py
import logging
from typing import Dict, Any, List
from datetime import datetime
from app.core.ml_client import ml_client  # Client pour l'API ML
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class FakeNewsDetector:
    """Service de détection de fake news qui utilise l'API ML"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ml_client = ml_client
    
    def detect_fake_news(self, text: str, metadata: Dict = None) -> Dict[str, Any]:
        """Détecte les fake news dans un texte"""
        try:
            # 1. Appeler l'API ML
            ml_result = self.ml_client.analyze_text(text)
            
            # 2. Analyser localement pour plus de détails
            local_analysis = self.analyze_locally(text, metadata)
            
            # 3. Combiner les résultats
            combined_score = self.combine_scores(
                ml_result.get("suspicion_score", 0),
                local_analysis.get("risk_score", 0)
            )
            
            # 4. Déterminer le niveau de risque
            risk_level = self.determine_risk_level(combined_score)
            
            return {
                "ml_analysis": ml_result,
                "local_analysis": local_analysis,
                "combined_risk_score": combined_score,
                "risk_level": risk_level,
                "is_fake_news": combined_score > 0.7,
                "confidence": ml_result.get("suspicion_score", 0),
                "analysis_timestamp": datetime.now().isoformat(),
                "recommendation": self.generate_recommendation(combined_score, risk_level)
            }
            
        except Exception as e:
            logger.error(f"Erreur détection fake news: {e}")
            return {
                "error": str(e),
                "is_fake_news": False,
                "risk_level": "UNKNOWN",
                "confidence": 0.0
            }
    
    def analyze_locally(self, text: str, metadata: Dict = None) -> Dict[str, Any]:
        """Analyse locale complémentaire"""
        # Ici tu peux ajouter ta propre logique d'analyse
        # ex: détection de patterns, vérification de sources, etc.
        
        risk_factors = []
        risk_score = 0.0
        
        # Facteur 1: Longueur du texte
        if len(text) < 50:
            risk_factors.append("Texte trop court")
            risk_score += 0.1
        
        # Facteur 2: Majuscules excessives
        if text.isupper() or sum(1 for c in text if c.isupper()) / len(text) > 0.5:
            risk_factors.append("Majuscules excessives")
            risk_score += 0.2
        
        # Facteur 3: Ponctuation exagérée
        if text.count('!') > 3 or text.count('?') > 5:
            risk_factors.append("Ponctuation exagérée")
            risk_score += 0.15
        
        # Facteur 4: Mots déclencheurs
        trigger_words = ['gratuit', 'free', 'urgent', 'immédiat', 'breaking', 'secret', 'miracle']
        found_triggers = [word for word in trigger_words if word in text.lower()]
        if found_triggers:
            risk_factors.append(f"Mots déclencheurs: {', '.join(found_triggers)}")
            risk_score += len(found_triggers) * 0.1
        
        return {
            "risk_factors": risk_factors,
            "risk_score": min(risk_score, 1.0),
            "text_length": len(text),
            "uppercase_ratio": sum(1 for c in text if c.isupper()) / len(text) if len(text) > 0 else 0,
            "trigger_words_found": found_triggers
        }
    
    def combine_scores(self, ml_score: float, local_score: float) -> float:
        """Combine les scores ML et local"""
        # Poids: 70% ML, 30% analyse locale
        return (ml_score * 0.7) + (local_score * 0.3)
    
    def determine_risk_level(self, score: float) -> str:
        """Détermine le niveau de risque"""
        if score >= 0.8:
            return "CRITICAL"
        elif score >= 0.6:
            return "HIGH"
        elif score >= 0.4:
            return "MEDIUM"
        elif score >= 0.2:
            return "LOW"
        else:
            return "VERY_LOW"
    
    def generate_recommendation(self, score: float, risk_level: str) -> str:
        """Génère une recommandation"""
        if risk_level == "CRITICAL":
            return "⚠️ ALERTE CRITIQUE - Contenu très suspect. Ne pas partager."
        elif risk_level == "HIGH":
            return "⚠️ Risque élevé - Vérifier absolument avant de partager."
        elif risk_level == "MEDIUM":
            return "⚠️ Risque modéré - Être prudent avec cette information."
        elif risk_level == "LOW":
            return "ℹ️ Risque faible - Mais vérifier quand même les sources."
        else:
            return "✅ Apparemment sûr - Mais rester vigilant."
    
    def batch_detect(self, texts: List[str]) -> Dict[str, Any]:
        """Détecte les fake news dans plusieurs textes"""
        results = []
        fake_count = 0
        high_risk_count = 0
        
        for text in texts:
            analysis = self.detect_fake_news(text)
            results.append({
                "text_preview": text[:100] + "..." if len(text) > 100 else text,
                "analysis": analysis
            })
            
            if analysis.get("is_fake_news", False):
                fake_count += 1
            
            if analysis.get("risk_level") in ["HIGH", "CRITICAL"]:
                high_risk_count += 1
        
        return {
            "total_analyzed": len(texts),
            "fake_news_detected": fake_count,
            "high_risk_content": high_risk_count,
            "results": results
        }