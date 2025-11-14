# Module 7 : Middleware et logging

## Explication théorique

### 1. Qu'est-ce qu'un middleware ?

Un middleware est une fonction qui s'exécute avant et après chaque requête. Utile pour :
- Logging des requêtes
- Mesure du temps de réponse
- Authentification
- CORS
- Rate limiting

### 2. Middleware dans FastAPI

```python
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### 3. Logging des requêtes

```python
import logging

logger = logging.getLogger("api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

### 4. Logging des prédictions ML

Pour MLOps, vous voulez logger :
- Les features reçues
- Les prédictions faites
- Le temps de prédiction
- Les erreurs

### 5. Middleware pour monitoring

```python
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    # Avant la requête
    start = time.time()
    
    # Exécuter la requête
    response = await call_next(request)
    
    # Après la requête
    duration = time.time() - start
    
    # Logger ou envoyer à un système de monitoring
    log_metrics(request, response, duration)
    
    return response
```

## Exercice 7 : Ajouter middleware et logging

**Objectif :** Créer un middleware pour logger les prédictions et mesurer les performances.

**Instructions :**

1. **Configurer le logging** dans `app/main.py` :
   - Créer un logger nommé "iris_api"
   - Configurer le format : timestamp, niveau, message
   - Logger dans un fichier `logs/api.log`

2. **Créer un middleware de logging** :
   - Logger toutes les requêtes (méthode, URL, status code)
   - Mesurer le temps de traitement
   - Ajouter un header `X-Process-Time` à la réponse

3. **Créer un middleware spécifique pour `/predict`** :
   - Logger les features reçues (sans données sensibles si nécessaire)
   - Logger les prédictions faites
   - Logger le temps de prédiction spécifiquement

4. **Créer un endpoint `/metrics`** :
   - GET endpoint qui retourne des métriques basiques
   - Nombre de prédictions totales (depuis le démarrage)
   - Temps moyen de prédiction
   - Tag: "Monitoring"

**Fichiers à modifier :**
- `app/main.py` : Middleware et logging
- `app/middleware.py` : Middleware personnalisé (optionnel, peut être dans main.py)

**Indices :**
- Utilisez `logging` de Python
- Utilisez `@app.middleware("http")`
- Utilisez une variable globale pour stocker les métriques
- Utilisez `request.url.path` pour vérifier le chemin

---

