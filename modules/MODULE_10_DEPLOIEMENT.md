# Module 10 : Déploiement et production

## Explication théorique

### 1. Configuration avec variables d'environnement

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_path: str
    api_version: str = "1.0.0"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 2. Uvicorn pour production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Options importantes :**
- `--host 0.0.0.0` : Écouter sur toutes les interfaces
- `--port 8000` : Port d'écoute
- `--workers 4` : Nombre de workers (processus)
- `--reload` : Rechargement automatique (développement uniquement)

### 3. Docker pour containerisation

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Gunicorn avec Uvicorn workers

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 5. Configuration de production

- Variables d'environnement pour secrets
- Logging vers fichiers
- Monitoring et alertes
- Rate limiting
- CORS configuré

## Exercice 10 : Configurer pour la production

**Objectif :** Préparer l'application pour le déploiement en production.

**Instructions :**

1. **Créer un fichier `.env.example`** :
   - Variables d'environnement nécessaires
   - Exemples de valeurs

2. **Créer `app/config.py`** :
   - Classe `Settings` avec Pydantic
   - Variables : `MODEL_PATH`, `API_VERSION`, `LOG_LEVEL`, etc.
   - Chargement depuis `.env`

3. **Modifier `app/main.py`** :
   - Utiliser `Settings` pour la configuration
   - Charger le chemin du modèle depuis les settings

4. **Créer `requirements.txt`** :
   - Toutes les dépendances nécessaires
   - Versions spécifiées

5. **Créer `Dockerfile`** :
   - Image Python
   - Installation des dépendances
   - Copie du code
   - Commande de démarrage

6. **Créer `docker-compose.yml`** (optionnel) :
   - Service API
   - Volumes pour logs
   - Variables d'environnement

7. **Créer `.dockerignore`** :
   - Exclure fichiers inutiles

**Fichiers à créer/modifier :**
- `.env.example`
- `app/config.py`
- `app/main.py` (modifier)
- `app/dependencies.py` (modifier pour utiliser config)
- `requirements.txt`
- `Dockerfile`
- `docker-compose.yml` (optionnel)
- `.dockerignore`

**Indices :**
- Utilisez `pydantic-settings` pour les settings
- Utilisez `python-dotenv` pour charger `.env`
- Dans Docker, copiez le modèle dans l'image

---

