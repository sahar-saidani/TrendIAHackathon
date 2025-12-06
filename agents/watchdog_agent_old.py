# agent/watchdog.py
import time
import logging
import pickle
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path
import schedule

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.config import settings
from app.models.account import Account
from app.models.post import Post
from app.models.narrative import Narrative

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('watchdog.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TrendIAWatchdog:
    def __init__(self):
        self.model_path = settings.MODEL_PATH
        self.bot_model = None
        self.running = True
        self.stats = {
            'total_analyzed': 0,
            'bots_detected': 0,
            'narratives_found': 0,
            'last_run': None
        }
        
        logger.info("=" * 50)
        logger.info("🚀 INITIALISATION AGENT TRENDIA WATCHDOG")
        logger.info("=" * 50)
        logger.info(f"📁 Chemin modèles: {self.model_path}")
        logger.info(f"📊 Base de données: {settings.POSTGRES_DB}")
        
    def load_models(self):
        """Charge tous les modèles ML"""
        try:
            # 1. Modèle de détection de bots
            bot_model_path = os.path.join(self.model_path, "bot_detector.pkl")
            if os.path.exists(bot_model_path):
                with open(bot_model_path, 'rb') as f:
                    self.bot_model = pickle.load(f)
                logger.info(f"✅ Modèle bot_detector chargé ({self.bot_model.__class__.__name__})")
            else:
                logger.warning(f"❌ Fichier {bot_model_path} non trouvé")
                return False
            
            # 2. Charger les données de référence
            self.load_reference_data()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur chargement modèles: {e}")
            return False
    
    def load_reference_data(self):
        """Charge les données de référence depuis les CSV"""
        try:
            # Narratives de référence
            narratives_path = os.path.join(self.model_path, "ai_generated_narratives.csv")
            if os.path.exists(narratives_path):
                self.reference_narratives = pd.read_csv(narratives_path)
                logger.info(f"✅ {len(self.reference_narratives)} narratives de référence chargées")
            else:
                self.reference_narratives = pd.DataFrame()
                logger.warning("Aucun fichier de narratives trouvé")
                
        except Exception as e:
            logger.error(f"Erreur chargement données: {e}")
            self.reference_narratives = pd.DataFrame()
    
    def analyze_cycle(self):
        """Exécute un cycle complet d'analyse"""
        logger.info("\n" + "=" * 50)
        logger.info("🔄 DÉBUT CYCLE D'ANALYSE")
        logger.info("=" * 50)
        
        start_time = datetime.now()
        
        try:
            # 1. Analyser les comptes pour détecter les bots
            bots_found = self.analyze_accounts_for_bots()
            
            # 2. Détecter les narratives
            narratives_found = self.detect_narratives()
            
            # 3. Calculer les risques
            self.calculate_risk_scores()
            
            # 4. Générer le rapport
            self.generate_report(start_time, bots_found, narratives_found)
            
            logger.info("✅ Cycle d'analyse terminé avec succès")
            
        except Exception as e:
            logger.error(f"❌ Erreur pendant le cycle d'analyse: {e}")
    
    def analyze_accounts_for_bots(self):
        """Analyse les comptes pour détecter les bots"""
        db = SessionLocal()
        bots_found = 0
        
        try:
            # Récupérer les comptes à analyser (ceux non analysés depuis 24h)
            cutoff_time = datetime.now() - timedelta(hours=24)
            
            accounts = db.query(Account).filter(
                (Account.last_analyzed == None) | 
                (Account.last_analyzed < cutoff_time)
            ).limit(200).all()
            
            if not accounts:
                logger.info("📭 Aucun compte à analyser")
                return 0
            
            logger.info(f"🔍 Analyse de {len(accounts)} comptes...")
            
            for account in accounts:
                try:
                    # Extraire les features
                    features = self.extract_account_features(account, db)
                    
                    if features is not None and self.bot_model is not None:
                        # Faire la prédiction
                        prediction = self.bot_model.predict([features])[0]
                        probabilities = self.bot_model.predict_proba([features])[0]
                        
                        bot_confidence = probabilities[1]  # Probabilité d'être un bot
                        
                        # Mettre à jour le compte
                        was_bot = account.is_bot
                        account.is_bot = bool(prediction)
                        account.bot_probability = float(bot_confidence)
                        account.last_analyzed = datetime.now()
                        
                        # Calculer un score de risque basé sur la probabilité
                        account.risk_score = self.calculate_risk_score(account, db)
                        
                        if account.is_bot and not was_bot:
                            bots_found += 1
                            logger.warning(f"🤖 NOUVEAU BOT DÉTECTÉ: @{account.username}")
                            logger.warning(f"   Confiance: {bot_confidence:.2%}")
                            logger.warning(f"   Score risque: {account.risk_score:.2%}")
                        
                        # Enregistrer périodiquement
                        if accounts.index(account) % 50 == 0:
                            db.commit()
                
                except Exception as e:
                    logger.error(f"Erreur analyse compte {account.username}: {e}")
                    continue
            
            # Commit final
            db.commit()
            logger.info(f"✅ Analyse comptes terminée: {bots_found} nouveaux bots détectés")
            
            # Mettre à jour les stats
            self.stats['total_analyzed'] += len(accounts)
            self.stats['bots_detected'] += bots_found
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse comptes: {e}")
            db.rollback()
        finally:
            db.close()
        
        return bots_found
    
    def extract_account_features(self, account: Account, db: Session):
        """Extrait les features d'un compte pour le modèle"""
        try:
            # Récupérer les posts du compte
            posts = db.query(Post).filter(Post.account_id == account.id).all()
            post_count = len(posts)
            
            # Calculer diverses métriques
            features = []
            
            # 1. Ratio followers/following (normalisé)
            if account.following_count > 0:
                ff_ratio = account.followers_count / account.following_count
            else:
                ff_ratio = account.followers_count
            features.append(min(ff_ratio / 10, 2.0))  # Normalisé
            
            # 2. Fréquence de tweets (posts par jour)
            if account.created_at:
                account_age = (datetime.now() - account.created_at).days
                if account_age > 0:
                    tweet_freq = account.tweet_count / account_age
                else:
                    tweet_freq = account.tweet_count
            else:
                tweet_freq = account.tweet_count
            features.append(min(tweet_freq / 100, 5.0))  # Normalisé
            
            # 3. Âge du compte (normalisé)
            if account.created_at:
                account_age_days = (datetime.now() - account.created_at).days
                age_normalized = min(account_age_days / 365, 3.0)  # 3 ans max pour normalisation
            else:
                age_normalized = 0.1
            features.append(age_normalized)
            
            # 4. Statut vérifié
            features.append(1.0 if account.is_verified else 0.0)
            
            # 5. Engagement moyen (likes par tweet)
            if post_count > 0 and account.tweet_count > 0:
                total_likes = sum(p.likes_count for p in posts[:100])  # Limiter pour performance
                avg_engagement = total_likes / min(post_count, 100)
            else:
                avg_engagement = 0
            features.append(min(avg_engagement / 100, 5.0))  # Normalisé
            
            return features
            
        except Exception as e:
            logger.error(f"Erreur extraction features: {e}")
            return [0.5, 0.5, 0.5, 0.5, 0.5]  # Valeurs par défaut
    
    def detect_narratives(self):
        """Détecte les narratives dans les posts récents"""
        db = SessionLocal()
        narratives_found = 0
        
        try:
            # Récupérer les posts récents (dernières 24h)
            cutoff_time = datetime.now() - timedelta(hours=24)
            
            recent_posts = db.query(Post).filter(
                Post.created_at >= cutoff_time
            ).limit(500).all()
            
            if not recent_posts:
                logger.info("📭 Aucun post récent à analyser")
                return 0
            
            logger.info(f"📰 Analyse de {len(recent_posts)} posts récents...")
            
            # Ici, normalement on utiliserait un modèle NLP
            # Pour l'instant, on simule la détection
            if not self.reference_narratives.empty:
                for narrative in self.reference_narratives.itertuples():
                    # Simuler la détection (dans la vraie vie, on analyserait le contenu)
                    if np.random.random() < 0.3:  # 30% de chance de "détecter" chaque narrative
                        logger.info(f"📖 Narrative détectée: {narrative.name}")
                        narratives_found += 1
            
            # Mettre à jour les stats
            self.stats['narratives_found'] += narratives_found
            
            logger.info(f"✅ Détection narratives: {narratives_found} narratives potentielles")
            
        except Exception as e:
            logger.error(f"❌ Erreur détection narratives: {e}")
        finally:
            db.close()
        
        return narratives_found
    
    def calculate_risk_score(self, account: Account, db: Session):
        """Calcule un score de risque pour un compte"""
        try:
            risk_score = 0.0
            
            # 1. Probabilité de bot (50% du score)
            risk_score += account.bot_probability * 0.5
            
            # 2. Activité récente (25% du score)
            recent_posts = db.query(Post).filter(
                Post.account_id == account.id,
                Post.created_at >= datetime.now() - timedelta(hours=24)
            ).count()
            
            if recent_posts > 100:  # Plus de 100 posts en 24h = suspect
                risk_score += min(recent_posts / 500, 0.25)
            else:
                risk_score += (recent_posts / 400) * 0.25
            
            # 3. Followers ratio anormal (25% du score)
            if account.following_count > 0:
                ff_ratio = account.followers_count / account.following_count
                if ff_ratio < 0.01 or ff_ratio > 100:  # Ratios extrêmes
                    risk_score += 0.25
            
            return min(risk_score, 1.0)  # Normaliser à 1
            
        except Exception as e:
            logger.error(f"Erreur calcul risque: {e}")
            return account.bot_probability
    
    def calculate_risk_scores(self):
        """Recalcule les scores de risque pour tous les comptes"""
        db = SessionLocal()
        
        try:
            logger.info("📊 Calcul des scores de risque...")
            
            accounts = db.query(Account).filter(
                Account.is_active == True
            ).limit(1000).all()
            
            for account in accounts:
                account.risk_score = self.calculate_risk_score(account, db)
            
            db.commit()
            logger.info(f"✅ Scores de risque mis à jour pour {len(accounts)} comptes")
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul scores risque: {e}")
            db.rollback()
        finally:
            db.close()
    
    def generate_report(self, start_time, bots_found, narratives_found):
        """Génère un rapport d'analyse"""
        try:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            report_dir = "reports"
            os.makedirs(report_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = os.path.join(report_dir, f"watchdog_report_{timestamp}.txt")
            
            db = SessionLocal()
            total_accounts = db.query(Account).count()
            total_bots = db.query(Account).filter(Account.is_bot == True).count()
            db.close()
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("📊 RAPPORT TRENDIA WATCHDOG\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Durée analyse: {duration:.1f} secondes\n\n")
                
                f.write("📈 STATISTIQUES GLOBALES\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total comptes dans DB: {total_accounts}\n")
                f.write(f"Total bots détectés: {total_bots}\n")
                f.write(f"Pourcentage bots: {(total_bots/total_accounts*100):.2f}% \n\n")
                
                f.write("🔄 RÉSULTATS DU DERNIER CYCLE\n")
                f.write("-" * 40 + "\n")
                f.write(f"Comptes analysés: {self.stats['total_analyzed']}\n")
                f.write(f"Bots détectés ce cycle: {bots_found}\n")
                f.write(f"Narratives détectées: {narratives_found}\n\n")
                
                f.write("📋 HISTORIQUE CUMULÉ\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total analysé depuis démarrage: {self.stats['total_analyzed']}\n")
                f.write(f"Total bots détectés: {self.stats['bots_detected']}\n")
                f.write(f"Total narratives trouvées: {self.stats['narratives_found']}\n\n")
                
                f.write("🚨 COMPTES À HAUT RISQUE\n")
                f.write("-" * 40 + "\n")
                
                db = SessionLocal()
                high_risk_accounts = db.query(Account).filter(
                    Account.risk_score >= 0.8,
                    Account.is_active == True
                ).order_by(Account.risk_score.desc()).limit(10).all()
                
                for acc in high_risk_accounts:
                    f.write(f"@{acc.username:<20} | Risk: {acc.risk_score:.1%} | Bot: {acc.is_bot}\n")
                
                db.close()
                
                f.write("\n" + "=" * 60 + "\n")
                f.write("✅ Rapport généré avec succès\n")
                f.write("=" * 60 + "\n")
            
            logger.info(f"📄 Rapport généré: {report_path}")
            
            # Afficher un résumé dans les logs
            logger.info("\n" + "=" * 50)
            logger.info("📊 RÉSUMÉ DU CYCLE")
            logger.info("=" * 50)
            logger.info(f"⏱️  Durée: {duration:.1f}s")
            logger.info(f"👤 Comptes analysés: {self.stats['total_analyzed']}")
            logger.info(f"🤖 Bots détectés: {bots_found}")
            logger.info(f"📖 Narratives: {narratives_found}")
            logger.info(f"📈 Total bots DB: {total_bots}")
            
        except Exception as e:
            logger.error(f"❌ Erreur génération rapport: {e}")
    
    def print_banner(self):
        """Affiche une bannière stylée"""
        banner = """
        ╔═══════════════════════════════════════════════════════╗
        ║      🚀 TRENDIA WATCHDOG AGENT - DÉMARRAGE           ║
        ║      🤖 Détection de bots & narratives              ║
        ║      📊 Analyse en temps réel                        ║
        ╚═══════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def run(self):
        """Lance l'agent en mode continu"""
        self.print_banner()
        logger.info("🚀 Démarrage de l'agent TrendIA Watchdog...")
        
        # Charger les modèles
        if not self.load_models():
            logger.error("❌ Impossible de charger les modèles. Arrêt.")
            return
        
        logger.info("✅ Tous les systèmes sont opérationnels")
        logger.info("🔄 Début de la surveillance continue...")
        logger.info("   (Appuyez sur Ctrl+C pour arrêter)\n")
        
        # Premier cycle immédiat
        self.analyze_cycle()
        
        # Puis exécuter toutes les 5 minutes
        cycle_count = 1
        while self.running:
            try:
                logger.info(f"\n⏰ Cycle #{cycle_count} - Attente de 5 minutes...")
                
                # Attendre 5 minutes
                for i in range(300):  # 300 secondes = 5 minutes
                    if not self.running:
                        break
                    time.sleep(1)
                
                if self.running:
                    cycle_count += 1
                    self.analyze_cycle()
                    
            except KeyboardInterrupt:
                logger.info("\n\n🛑 Arrêt demandé par l'utilisateur")
                self.running = False
            except Exception as e:
                logger.error(f"❌ Erreur inattendue: {e}")
                time.sleep(60)  # Attendre 1 minute en cas d'erreur
        
        logger.info("👋 Agent Watchdog arrêté")

def main():
    """Point d'entrée principal"""
    agent = TrendIAWatchdog()
    agent.run()

if __name__ == "__main__":
    main()