# test_postgres_connection.py
import psycopg2
from psycopg2 import OperationalError

def test_postgres_connection():
    print("🔍 Test de connexion à PostgreSQL 18...")
    
    # Essayer avec différents mots de passe courants
    test_passwords = [
        "admin123",        # Mot de passe courant 1
        "password",        # Mot de passe courant 2  
        "postgres",        # Mot de passe courant 3
        "root",            # Mot de passe courant 4
        "123456",          # Mot de passe courant 5
        ""                 # Mot de passe vide
    ]
    
    for password in test_passwords:
        try:
            print(f"Essai avec mot de passe: '{password}'")
            
            connection = psycopg2.connect(
                host="localhost",
                database="postgres",  # Essayer la DB par défaut d'abord
                user="postgres",
                password=password,
                port="5432"
            )
            
            print(f"✅ SUCCÈS! Mot de passe trouvé: '{password}'")
            
            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print(f"📊 Version PostgreSQL: {db_version[0]}")
            
            cursor.close()
            connection.close()
            
            # Retourner le mot de passe qui fonctionne
            return password
            
        except OperationalError as e:
            if "password authentication" in str(e):
                continue  # Essayer le mot de passe suivant
            else:
                print(f"❌ Autre erreur: {e}")
                break
    
    print("❌ Aucun mot de passe standard n'a fonctionné.")
    print("\n💡 Solutions:")
    print("1. Vérifie le mot de passe que tu as défini lors de l'installation")
    print("2. Réinitialise le mot de passe avec pgAdmin")
    print("3. Essaie de te connecter avec pgAdmin pour voir quel mot de passe fonctionne")
    return None

def create_database():
    """Crée la base de données trendia_db"""
    password = test_postgres_connection()
    
    if password:
        try:
            print("\n🗄️  Création de la base de données...")
            
            # Se connecter à la DB postgres par défaut
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password=password,
                port="5432"
            )
            conn.autocommit = True  # Important pour CREATE DATABASE
            
            cursor = conn.cursor()
            
            # Créer la base de données
            cursor.execute("CREATE DATABASE trendia_db;")
            print("✅ Base 'trendia_db' créée")
            
            # Vérifier
            cursor.execute("SELECT datname FROM pg_database;")
            databases = cursor.fetchall()
            print("\n📋 Bases de données disponibles:")
            for db in databases:
                print(f"  - {db[0]}")
            
            cursor.close()
            conn.close()
            
            # Mettre à jour le .env avec le bon mot de passe
            update_env_file(password)
            
        except Exception as e:
            print(f"❌ Erreur création DB: {e}")

def update_env_file(password):
    """Met à jour le fichier .env avec le bon mot de passe"""
    try:
        env_path = "C:\\Users\\ASUS\\Desktop\\TrendIAHackathon\\.env"
        
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Mettre à jour les lignes avec le mot de passe
        updated_lines = []
        for line in lines:
            if "POSTGRES_PASSWORD=" in line:
                updated_lines.append(f'POSTGRES_PASSWORD={password}\n')
            elif "DATABASE_URL=" in line and "postgresql://" in line:
                # Remplacer le mot de passe dans l'URL
                import re
                line = re.sub(r'postgresql://postgres:[^@]*@', f'postgresql://postgres:{password}@', line)
                updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        with open(env_path, 'w') as f:
            f.writelines(updated_lines)
        
        print(f"\n✅ Fichier .env mis à jour avec le mot de passe: {password}")
        
    except Exception as e:
        print(f"⚠️ Impossible de mettre à jour .env: {e}")

if __name__ == "__main__":
    create_database()