# Module 10 : Correction et explications détaillées

## Correction de l'exercice 10

### 1. Configuration (app/config.py)

```python
"""
Configuration de l'application avec variables d'environnement
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """
    Settings de l'application
    
    Explication :
    - Hérite de BaseSettings pour charger depuis .env
    - Valeurs par défaut si non définies
    - Validation automatique des types
    """
    # Chemin du modèle
    MODEL_PATH: str = "app/model.pkl"
    
    # Version de l'API
    API_VERSION: str = "1.0.0"
    
    # Configuration du logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/api.log"
    
    # Configuration du serveur
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    # Configuration CORS (si nécessaire)
    CORS_ORIGINS: list[str] = ["*"]
    
    # Environment
    ENVIRONMENT: str = "development"  # development, staging, production
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Instance globale des settings
settings = Settings()
```

### 2. Fichier .env.example

```env
# Chemin du modèle ML
MODEL_PATH=app/model.pkl

# Version de l'API
API_VERSION=1.0.0

# Configuration du logging
LOG_LEVEL=INFO
LOG_FILE=logs/api.log

# Configuration du serveur
HOST=0.0.0.0
PORT=8000
WORKERS=1

# Environment
ENVIRONMENT=development
```

### 3. Modifier app/dependencies.py

```python
from fastapi import HTTPException
import joblib
import os
from app.config import settings

# Pattern Singleton pour le modèle
_model = None

# Mapping des classes
CLASS_NAMES = {
    0: "setosa",
    1: "versicolor",
    2: "virginica"
}

def get_model():
    """
    Dépendance pour obtenir le modèle ML chargé
    Utilise le chemin depuis les settings
    """
    global _model
    
    if _model is not None:
        return _model
    
    try:
        model_path = settings.MODEL_PATH
        
        # Résoudre le chemin (absolu ou relatif)
        if not os.path.isabs(model_path):
            # Chemin relatif depuis la racine du projet
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, model_path)
        
        if not os.path.exists(model_path):
            raise HTTPException(
                status_code=500,
                detail=f"Model file not found at {model_path}"
            )
        
        _model = joblib.load(model_path)
        return _model
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading model: {str(e)}"
        )

def get_class_names():
    return CLASS_NAMES
```

### 4. Modifier app/main.py (ajout de la config)

```python
from app.config import settings

# ... autres imports ...

app = FastAPI(
    title="Iris Classification API",
    description="API pour classifier des fleurs Iris avec un modèle de Machine Learning.",
    version=settings.API_VERSION  #  Utiliser depuis settings
)

# ... reste du code ...
```

### 5. requirements.txt

```txt
fastapi>=0.121.2
uvicorn[standard]>=0.38.0
pydantic>=2.12.4
pydantic-settings>=2.0.0
python-dotenv>=1.0.0
numpy>=2.3.4
scikit-learn>=1.7.2
joblib>=1.5.2
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

### 6. Dockerfile

```dockerfile
# Utiliser une image Python officielle
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système si nécessaire
# RUN apt-get update && apt-get install -y ...

# Copier le fichier requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app/ ./app/
COPY model.pkl ./app/model.pkl  # Copier le modèle (ou utiliser un volume)

# Créer le dossier logs
RUN mkdir -p logs

# Exposer le port
EXPOSE 8000

# Variable d'environnement pour Python
ENV PYTHONUNBUFFERED=1

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 7. docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=app/model.pkl
      - API_VERSION=1.0.0
      - LOG_LEVEL=INFO
      - ENVIRONMENT=production
    volumes:
      - ./logs:/app/logs
      - ./app/model.pkl:/app/app/model.pkl  # Si le modèle est externe
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 8. .dockerignore

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
.DS_Store
*.md
tests/
.env
.env.local
```

### 9. Script de démarrage (start.sh)

```bash
#!/bin/bash

# Script de démarrage pour production

# Charger les variables d'environnement
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Démarrer avec uvicorn
uvicorn app.main:app \
    --host ${HOST:-0.0.0.0} \
    --port ${PORT:-8000} \
    --workers ${WORKERS:-4} \
    --log-level ${LOG_LEVEL:-info}
```

### 10. README.md mis à jour

Ajoutez une section déploiement :

```markdown
## Déploiement

### Variables d'environnement

Copiez `.env.example` vers `.env` et configurez :

```bash
cp .env.example .env
```

### Développement local

```bash
uvicorn app.main:app --reload
```

### Production avec Docker

```bash
docker build -t iris-api .
docker run -p 8000:8000 iris-api
```

### Production avec docker-compose

```bash
docker-compose up -d
```

### Production avec uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Production avec gunicorn

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```
```

## Points clés à retenir

### 1. Variables d'environnement

**Avantages :**
- Sécurité (pas de secrets dans le code)
- Configuration par environnement
- Facile à changer sans modifier le code

### 2. Docker

**Avantages :**
- Environnement reproductible
- Isolation
- Facile à déployer

**Bonnes pratiques :**
- Utiliser `.dockerignore`
- Multi-stage builds pour réduire la taille
- Health checks
- Volumes pour les données persistantes

### 3. Production vs Développement

**Développement :**
- `--reload` activé
- Logging verbeux
- Un seul worker

**Production :**
- Pas de `--reload`
- Logging vers fichiers
- Plusieurs workers
- Monitoring activé

### 4. Sécurité

- Ne jamais commiter `.env`
- Utiliser des secrets managers en production
- HTTPS en production
- Rate limiting
- CORS configuré

## Commandes utiles

### Développement

```bash
# Démarrer avec reload
uvicorn app.main:app --reload

# Démarrer sur un port spécifique
uvicorn app.main:app --port 8080
```

### Production

```bash
# Avec uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Avec gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Avec Docker
docker build -t iris-api .
docker run -p 8000:8000 iris-api

# Avec docker-compose
docker-compose up -d
```

### Monitoring

```bash
# Vérifier les logs
docker logs iris-api

# Health check
curl http://localhost:8000/health

# Métriques
curl http://localhost:8000/metrics
```

## Félicitations !

Vous avez maintenant une API FastAPI complète et production-ready pour le MLOps ! 

**Récapitulatif de ce que vous avez appris :**
-  Fondamentaux FastAPI (routes, paramètres)
-  Pydantic et validation
-  Endpoints ML avec prédictions
-  Documentation automatique
-  Dependencies et injection
-  Gestion d'erreurs
-  Middleware et logging
-  Endpoints avancés (batch, health, metrics)
-  Tests complets
-  Déploiement en production

**Prochaines étapes suggérées :**
- Ajouter l'authentification (JWT, OAuth)
- Intégrer avec des outils MLOps (MLflow, Weights & Biases)
- Ajouter du caching (Redis)
- Monitoring avancé (Prometheus, Grafana)
- CI/CD pipeline

