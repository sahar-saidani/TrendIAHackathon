""" from typing import Dict

def simple_watchdog_answer(token_id: str, risk_obj: Dict):
    score = risk_obj.get("score", 0)
    label = risk_obj.get("label", "Safe")
    reason = risk_obj.get("reason", "")
    answer = f"Token {token_id} risk: {label} ({score}). Reason: {reason}."
    return {"answer": answer, "score": score, "label": label, "reason": reason}
"""
"""
Agent Watchdog Service - Génère des analyses narratives intelligentes
"""

from typing import Dict, List, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
import json

class NarrativeWatchdogAgent:
    def __init__(self, db: Session):
        self.db = db
    
    def analyze_token_narrative(self, token_id: str, risk_data: Dict, posts_data: List[Dict]) -> Dict:
        """
        Analyse complète du narratif d'un token
        """
        # 1. Analyse des patterns de posts
        post_patterns = self._analyze_post_patterns(posts_data)
        
        # 2. Détection de coordination
        coordination_signals = self._detect_coordination(posts_data)
        
        # 3. Analyse temporelle
        temporal_patterns = self._analyze_temporal_patterns(posts_data)
        
        # 4. Analyse sémantique
        semantic_analysis = self._analyze_semantic_themes(posts_data)
        
        # 5. Génération du rapport narratif
        narrative_report = self._generate_narrative_report(
            token_id=token_id,
            risk_data=risk_data,
            post_patterns=post_patterns,
            coordination=coordination_signals,
            temporal=temporal_patterns,
            semantic=semantic_analysis
        )
        
        return narrative_report
    
    def _analyze_post_patterns(self, posts: List[Dict]) -> Dict:
        """Analyse les patterns de posts"""
        if not posts:
            return {"status": "no_data", "patterns": []}
        
        # Group par compte
        account_posts = {}
        for post in posts:
            account = post.get('account_id', 'unknown')
            if account not in account_posts:
                account_posts[account] = []
            account_posts[account].append(post)
        
        # Calcul des métriques
        total_posts = len(posts)
        unique_accounts = len(account_posts)
        
        # Posts par compte
        posts_per_account = {}
        for account, account_posts_list in account_posts.items():
            posts_per_account[account] = len(account_posts_list)
        
        # Distribution
        suspicious_posts = [p for p in posts if p.get('label') == 'Suspicious']
        organic_posts = [p for p in posts if p.get('label') == 'Organic']
        
        return {
            "total_posts": total_posts,
            "unique_accounts": unique_accounts,
            "suspicious_ratio": len(suspicious_posts) / total_posts if total_posts > 0 else 0,
            "organic_ratio": len(organic_posts) / total_posts if total_posts > 0 else 0,
            "concentration_score": max(posts_per_account.values()) / total_posts if total_posts > 0 else 0,
            "posts_per_account": posts_per_account
        }
    
    def _detect_coordination(self, posts: List[Dict]) -> Dict:
        """Détecte les signes de coordination"""
        if not posts:
            return {"coordinated": False, "clusters": [], "similarity_score": 0}
        
        # Regroupement par cluster
        cluster_groups = {}
        for post in posts:
            cluster = post.get('cluster_id')
            if cluster:
                if cluster not in cluster_groups:
                    cluster_groups[cluster] = []
                cluster_groups[cluster].append(post)
        
        # Filtre les clusters significatifs (>1 post)
        significant_clusters = {k: v for k, v in cluster_groups.items() if len(v) > 1}
        
        # Calcule le score de coordination
        total_in_clusters = sum(len(v) for v in significant_clusters.values())
        coordination_score = total_in_clusters / len(posts) if posts else 0
        
        return {
            "coordinated": coordination_score > 0.2,
            "coordination_score": coordination_score,
            "significant_clusters": len(significant_clusters),
            "total_posts_in_clusters": total_in_clusters,
            "cluster_details": [
                {
                    "cluster_id": cluster_id,
                    "post_count": len(posts),
                    "accounts": list(set(p.get('account_id') for p in posts)),
                    "sample_texts": [p.get('text', '')[:50] + '...' for p in posts[:2]]
                }
                for cluster_id, posts in list(significant_clusters.items())[:5]
            ]
        }
    
    def _analyze_temporal_patterns(self, posts: List[Dict]) -> Dict:
        """Analyse les patterns temporels"""
        if not posts:
            return {"bursts": [], "frequency": 0, "pattern": "no_data"}
        
        # Trie par timestamp
        sorted_posts = sorted(posts, key=lambda x: x.get('timestamp', ''))
        
        # Détection de bursts (groupes de posts rapprochés dans le temps)
        bursts = []
        current_burst = []
        
        for i in range(1, len(sorted_posts)):
            prev_time = sorted_posts[i-1].get('timestamp')
            curr_time = sorted_posts[i].get('timestamp')
            
            if prev_time and curr_time:
                # Convertir en datetime si string
                if isinstance(prev_time, str):
                    prev_time = datetime.fromisoformat(prev_time.replace('Z', '+00:00'))
                if isinstance(curr_time, str):
                    curr_time = datetime.fromisoformat(curr_time.replace('Z', '+00:00'))
                
                time_diff = (curr_time - prev_time).total_seconds()
                
                if time_diff < 300:  # 5 minutes entre les posts
                    if not current_burst:
                        current_burst.append(sorted_posts[i-1])
                    current_burst.append(sorted_posts[i])
                else:
                    if len(current_burst) > 1:
                        bursts.append({
                            "duration_seconds": time_diff,
                            "post_count": len(current_burst),
                            "accounts": list(set(p.get('account_id') for p in current_burst))
                        })
                    current_burst = []
        
        # Calcul de la fréquence moyenne
        if len(sorted_posts) > 1:
            first_time = sorted_posts[0].get('timestamp')
            last_time = sorted_posts[-1].get('timestamp')
            if first_time and last_time:
                if isinstance(first_time, str):
                    first_time = datetime.fromisoformat(first_time.replace('Z', '+00:00'))
                if isinstance(last_time, str):
                    last_time = datetime.fromisoformat(last_time.replace('Z', '+00:00'))
                
                total_seconds = (last_time - first_time).total_seconds()
                if total_seconds > 0:
                    frequency = len(sorted_posts) / (total_seconds / 3600)  # posts par heure
                else:
                    frequency = len(sorted_posts)
            else:
                frequency = len(sorted_posts)
        else:
            frequency = 0
        
        return {
            "total_posts": len(posts),
            "time_range": f"{sorted_posts[0].get('timestamp')} to {sorted_posts[-1].get('timestamp')}" if posts else "N/A",
            "frequency_posts_per_hour": frequency,
            "burst_detected": len(bursts) > 0,
            "burst_count": len(bursts),
            "burst_details": bursts[:3]  # Limite à 3 bursts pour éviter la surcharge
        }
    
    def _analyze_semantic_themes(self, posts: List[Dict]) -> Dict:
        """Analyse les thèmes sémantiques (version simplifiée)"""
        if not posts:
            return {"themes": [], "sentiment": "neutral", "hype_keywords": []}
        
        texts = [p.get('text', '') for p in posts]
        
        # Keywords pour détection de manipulation
        hype_keywords = [
            "moon", "pump", "dump", "to the moon", "shill", "buy now", 
            "sell now", "rug", "pull", "whale", "partnership", "confirmed",
            "announcement", "big news", "🚀", "📈", "🔥", "💎", "👐"
        ]
        
        fear_keywords = [
            "scam", "fake", "avoid", "warning", "danger", "lost", 
            "stolen", "hack", "exploit", "⚠️", "🚨", "💀"
        ]
        
        # Compte les occurrences
        hype_count = sum(1 for text in texts if any(keyword in text.lower() for keyword in hype_keywords))
        fear_count = sum(1 for text in texts if any(keyword in text.lower() for keyword in fear_keywords))
        
        # Détermine le sentiment dominant
        if hype_count > fear_count and hype_count > len(texts) * 0.3:
            sentiment = "hyper_positive"
        elif fear_count > hype_count and fear_count > len(texts) * 0.3:
            sentiment = "fearful"
        else:
            sentiment = "mixed"
        
        # Extrait les keywords les plus fréquents
        found_keywords = {}
        for text in texts:
            text_lower = text.lower()
            for keyword in hype_keywords + fear_keywords:
                if keyword in text_lower:
                    found_keywords[keyword] = found_keywords.get(keyword, 0) + 1
        
        top_keywords = sorted(found_keywords.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "sentiment": sentiment,
            "hype_percentage": hype_count / len(texts) if texts else 0,
            "fear_percentage": fear_count / len(texts) if texts else 0,
            "top_keywords": [{"keyword": k, "count": v} for k, v in top_keywords],
            "manipulation_indicators": hype_count > len(texts) * 0.4
        }
    
    def _generate_narrative_report(self, token_id: str, risk_data: Dict, 
                                   post_patterns: Dict, coordination: Dict, 
                                   temporal: Dict, semantic: Dict) -> Dict:
        """Génère un rapport narratif complet"""
        
        risk_score = risk_data.get('score', 0)
        risk_label = risk_data.get('label', 'Safe')
        
        # Logique de génération narrative
        narrative_points = []
        warnings = []
        recommendations = []
        
        # 1. Évaluation du risque global
        if risk_score > 70:
            narrative_points.append(f"⚠️ **Risque Élevé Détecté** - Score: {risk_score}/100")
            warnings.append("Ce token présente des signes forts de manipulation de marché.")
        elif risk_score > 40:
            narrative_points.append(f"⚠️ **Risque Modéré Détecté** - Score: {risk_score}/100")
            warnings.append("Activité suspecte détectée. Surveillance recommandée.")
        else:
            narrative_points.append(f"✅ **Risque Faible** - Score: {risk_score}/100")
        
        # 2. Analyse de coordination
        if coordination.get('coordinated'):
            narrative_points.append(f"🤖 **Coordination Détectée** - {coordination['significant_clusters']} clusters identifiés")
            narrative_points.append(f"   • {coordination['total_posts_in_clusters']} posts semblent coordonnés")
            warnings.append("Activité coordonnée détectée - peut indiquer un bot farm.")
        
        # 3. Patterns temporels
        if temporal.get('burst_detected'):
            narrative_points.append(f"⏱️ **Activité en Rafales** - {temporal['burst_count']} rafales détectées")
            narrative_points.append(f"   • Fréquence: {temporal['frequency_posts_per_hour']:.1f} posts/heure")
            warnings.append("Pattern de posting en rafales - typique des campagnes orchestrées.")
        
        # 4. Analyse sémantique
        if semantic.get('manipulation_indicators'):
            narrative_points.append(f"📢 **Langage de Manipulation** - {semantic['hype_percentage']*100:.1f}% de posts hype")
            top_keyword = semantic['top_keywords'][0]['keyword'] if semantic['top_keywords'] else "N/A"
            narrative_points.append(f"   • Mot-clé dominant: '{top_keyword}'")
            warnings.append("Langage excessivement promotionnel détecté.")
        
        # 5. Concentration des posts
        if post_patterns.get('concentration_score', 0) > 0.3:
            narrative_points.append(f"🎯 **Concentration Élevée** - {post_patterns['concentration_score']*100:.1f}% des posts par quelques comptes")
            warnings.append("Distribution inégale des posts - possible astroturfing.")
        
        # Génère les recommandations
        if risk_score > 70:
            recommendations = [
                "🚫 Éviter tout investissement",
                "🔍 Investiguer les comptes suspects",
                "📊 Surveiller les volumes de trading",
                "⚖️ Signaler aux autorités de régulation si nécessaire"
            ]
        elif risk_score > 40:
            recommendations = [
                "⚠️ Investir avec extrême prudence",
                "🔎 Vérifier les fondamentaux du token",
                "👥 Examiner la communauté réelle",
                "📈 Surveiller les mouvements de prix inhabituels"
            ]
        else:
            recommendations = [
                "✅ Risque acceptable pour investissement",
                "📚 Toujours faire votre propre recherche (DYOR)",
                "👀 Continuer la surveillance standard"
            ]
        
        # Construction du résumé exécutif
        executive_summary = f"""
        ## 📊 Rapport Narratif pour ${token_id}
        
        **Évaluation de Risque:** {risk_label} ({risk_score}/100)
        
        **Points Clés:**
        {chr(10).join(f'- {point}' for point in narrative_points)}
        
        **Recommandations:**
        {chr(10).join(f'- {rec}' for rec in recommendations)}
        
        **Dernière Mise à Jour:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
        """
        
        return {
            "token_id": token_id,
            "risk_score": risk_score,
            "risk_label": risk_label,
            "executive_summary": executive_summary.strip(),
            "narrative_points": narrative_points,
            "warnings": warnings,
            "recommendations": recommendations,
            "detailed_analysis": {
                "post_patterns": post_patterns,
                "coordination_analysis": coordination,
                "temporal_analysis": temporal,
                "semantic_analysis": semantic
            },
            "generated_at": datetime.utcnow().isoformat()
        }

def simple_watchdog_answer(token_id: str, risk_obj: Dict):
    """Version simplifiée pour compatibilité"""
    score = risk_obj.get("score", 0)
    label = risk_obj.get("label", "Safe")
    reason = risk_obj.get("reason", "")
    
    # Logique simple basée sur le score
    if score > 70:
        urgency = "🔴 URGENT - Manipulation détectée"
        action = "Éviter tout investissement"
    elif score > 40:
        urgency = "🟠 ALERTE - Activité suspecte"
        action = "Investir avec prudence"
    else:
        urgency = "🟢 SÉCURISÉ - Risque faible"
        action = "Surveillance standard"
    
    answer = f"""
    Token: ${token_id}
    Risque: {label} ({score}/100)
    Évaluation: {urgency}
    
    Raison: {reason}
    
    Recommandation: {action}
    
    Mise à jour: {datetime.utcnow().strftime('%H:%M UTC')}
    """
    
    return {
        "answer": answer.strip(),
        "score": score,
        "label": label,
        "reason": reason,
        "urgency": urgency,
        "recommendation": action
    }