# model/run_ml_api.py
import uvicorn
import os
import sys

if __name__ == "__main__":
    print("🤖 Démarrage de l'API des modèles ML...")
    print("📡 URL: http://localhost:8001")
    print("📚 Documentation: http://localhost:8001/docs")
    
    # S'assurer qu'on est dans le bon répertoire
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    uvicorn.run(
        "train_main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )