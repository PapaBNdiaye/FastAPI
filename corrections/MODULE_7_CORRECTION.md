# Module 7 : Correction et explications détaillées

## Correction de l'exercice 7

### 1. Configuration du logging et middleware (app/main.py)

```python
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
import numpy as np
import time
import logging
from pathlib import Path
from collections import defaultdict
from app.schemas import IrisFeatures, PredictionResponse
from app.dependencies import get_model, get_class_names
from app.exceptions import ModelNotLoadedError, PredictionError, InvalidFeaturesError

# ==================== Configuration du logging ====================

# Créer le dossier logs s'il n'existe pas
Path("logs").mkdir(exist_ok=True)

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/api.log"),
        logging.StreamHandler()  # Aussi afficher dans la console
    ]
)

logger = logging.getLogger("iris_api")

# ==================== Métriques globales ====================

# Stocker les métriques (en production, utilisez une base de données ou Redis)
metrics = {
    "total_predictions": 0,
    "total_requests": 0,
    "prediction_times": [],  # Liste des temps de prédiction
    "errors": defaultdict(int)  # Compteur d'erreurs par type
}

app = FastAPI(
    title="Iris Classification API",
    description="API pour classifier des fleurs Iris avec un modèle de Machine Learning.",
    version="1.0.0"
)

# ==================== Middleware ====================

@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    """
    Middleware pour logger toutes les requêtes
    
    Explication :
    - S'exécute avant et après chaque requête
    - call_next() exécute la requête suivante dans la chaîne
    - Mesure le temps de traitement
    """
    # Avant la requête
    start_time = time.time()
    metrics["total_requests"] += 1
    
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Exécuter la requête
    try:
        response = await call_next(request)
        
        # Après la requête
        process_time = time.time() - start_time
        
        # Ajouter le header de temps de traitement
        response.headers["X-Process-Time"] = str(round(process_time, 4))
        
        logger.info(
            f"Response: {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.4f}s"
        )
        
        return response
        
    except Exception as e:
        # Logger les erreurs
        process_time = time.time() - start_time
        logger.error(
            f"Error: {request.method} {request.url.path} - "
            f"Exception: {str(e)} - "
            f"Time: {process_time:.4f}s"
        )
        raise

@app.middleware("http")
async def log_predictions_middleware(request: Request, call_next):
    """
    Middleware spécifique pour logger les prédictions
    
    Explication :
    - Intercepte les requêtes POST /predict
    - Log les features et prédictions
    - Mesure le temps de prédiction spécifiquement
    """
    if request.url.path == "/predict" and request.method == "POST":
        start_time = time.time()
        
        # Exécuter la requête
        response = await call_next(request)
        
        # Si succès (status 200), logger la prédiction
        if response.status_code == 200:
            prediction_time = time.time() - start_time
            metrics["total_predictions"] += 1
            metrics["prediction_times"].append(prediction_time)
            
            # Garder seulement les 1000 dernières mesures (pour éviter la fuite mémoire)
            if len(metrics["prediction_times"]) > 1000:
                metrics["prediction_times"] = metrics["prediction_times"][-1000:]
            
            logger.info(
                f"Prediction completed - Time: {prediction_time:.4f}s - "
                f"Total predictions: {metrics['total_predictions']}"
            )
        else:
            # Logger les erreurs de prédiction
            error_type = "unknown"
            if response.status_code == 500:
                error_type = "server_error"
            elif response.status_code == 400:
                error_type = "client_error"
            metrics["errors"][error_type] += 1
            
            logger.warning(
                f"Prediction failed - Status: {response.status_code}"
            )
        
        return response
    
    # Pour les autres requêtes, juste passer
    return await call_next(request)

# ==================== Exception Handlers ====================

@app.exception_handler(ModelNotLoadedError)
async def model_not_loaded_handler(request: Request, exc: ModelNotLoadedError):
    metrics["errors"]["model_not_loaded"] += 1
    return JSONResponse(
        status_code=500,
        content={
            "error": "ModelNotLoadedError",
            "message": "The ML model could not be loaded",
            "detail": str(exc)
        }
    )

@app.exception_handler(PredictionError)
async def prediction_error_handler(request: Request, exc: PredictionError):
    metrics["errors"]["prediction_error"] += 1
    return JSONResponse(
        status_code=500,
        content={
            "error": "PredictionError",
            "message": "An error occurred during prediction",
            "detail": str(exc)
        }
    )

@app.exception_handler(InvalidFeaturesError)
async def invalid_features_handler(request: Request, exc: InvalidFeaturesError):
    metrics["errors"]["invalid_features"] += 1
    return JSONResponse(
        status_code=400,
        content={
            "error": "InvalidFeaturesError",
            "message": "The provided features are invalid",
            "detail": str(exc)
        }
    )

# ==================== Endpoints ====================

@app.get("/", tags=["General"])
def homepage():
    return {"message": "Welcome to the home page of iris classification"}

@app.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Faire une prédiction Iris",
    description="Prédit la classe d'une fleur Iris à partir de ses 4 features",
    tags=["ML Predictions"]
)
def predict(
    features: IrisFeatures,
    model = Depends(get_model),
    class_names = Depends(get_class_names)
):
    """
    Endpoint de prédiction avec logging automatique via middleware
    """
    try:
        if model is None:
            raise ModelNotLoadedError("Model is None")
        
        feature_values = [
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ]
        
        # Validation
        for i, val in enumerate(feature_values):
            if np.isnan(val) or np.isinf(val):
                raise InvalidFeaturesError(f"Feature {i} contains NaN or Inf: {val}")
        
        feature_array = np.array([feature_values])
        
        if feature_array.shape != (1, 4):
            raise InvalidFeaturesError(f"Invalid shape: {feature_array.shape}")
        
        # Prédiction
        prediction = model.predict(feature_array)[0]
        probabilities = model.predict_proba(feature_array)[0]
        
        if prediction not in class_names:
            raise PredictionError(f"Invalid prediction: {prediction}")
        
        prediction_probability = float(probabilities[prediction])
        class_name = class_names[prediction]
        
        # Logger les détails de la prédiction (optionnel, peut être fait dans middleware)
        logger.debug(
            f"Prediction: {class_name} (class {prediction}) "
            f"with probability {prediction_probability:.4f}"
        )
        
        return PredictionResponse(
            prediction=int(prediction),
            probability=prediction_probability,
            class_name=class_name,
            features=features
        )
        
    except (ModelNotLoadedError, PredictionError, InvalidFeaturesError):
        raise
    except Exception as e:
        raise PredictionError(f"Unexpected error: {str(e)}")

@app.get(
    "/metrics",
    summary="Métriques de l'API",
    description="Retourne les métriques de performance et d'utilisation de l'API",
    tags=["Monitoring"]
)
def get_metrics():
    """
    Endpoint pour obtenir les métriques de l'API
    
    Explication :
    - Compte les prédictions totales
    - Calcule le temps moyen de prédiction
    - Affiche les erreurs par type
    """
    avg_prediction_time = 0.0
    if metrics["prediction_times"]:
        avg_prediction_time = sum(metrics["prediction_times"]) / len(metrics["prediction_times"])
    
    return {
        "total_requests": metrics["total_requests"],
        "total_predictions": metrics["total_predictions"],
        "average_prediction_time_seconds": round(avg_prediction_time, 4),
        "min_prediction_time_seconds": round(min(metrics["prediction_times"]), 4) if metrics["prediction_times"] else 0,
        "max_prediction_time_seconds": round(max(metrics["prediction_times"]), 4) if metrics["prediction_times"] else 0,
        "errors": dict(metrics["errors"])
    }

@app.get("/health", tags=["Monitoring"])
def health_check(model = Depends(get_model)):
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }
```

## Points clés à retenir

### 1. Middleware HTTP

```python
@app.middleware("http")
async def my_middleware(request: Request, call_next):
    # Avant la requête
    response = await call_next(request)
    # Après la requête
    return response
```

**Ordre d'exécution :**
- Middleware 1 (avant)
- Middleware 2 (avant)
- Endpoint
- Middleware 2 (après)
- Middleware 1 (après)

### 2. Logging structuré

```python
logger.info(f"Message avec {variable}")
logger.error(f"Erreur: {exception}")
logger.debug(f"Debug: {details}")
```

**Niveaux :**
- `DEBUG` : Détails pour déboguer
- `INFO` : Informations générales
- `WARNING` : Avertissements
- `ERROR` : Erreurs
- `CRITICAL` : Erreurs critiques

### 3. Métriques en mémoire

**Note :** En production, utilisez :
- Redis pour les métriques
- Prometheus pour le monitoring
- Base de données pour l'historique

### 4. Headers personnalisés

```python
response.headers["X-Custom-Header"] = "value"
```

**Utile pour :**
- Temps de traitement
- Version de l'API
- ID de requête

## Interface Docs - Monitoring

Dans `/docs`, vous verrez :

1. **Endpoint `/metrics`** :
   - Métriques en temps réel
   - Performance de l'API
   - Statistiques d'erreurs

2. **Headers de réponse** :
   - `X-Process-Time` dans chaque réponse
   - Visible dans les outils de développement du navigateur

3. **Logs** :
   - Fichier `logs/api.log` avec toutes les requêtes
   - Format structuré pour analyse

## Prochaines étapes

Maintenant que le monitoring est en place, nous allons créer des endpoints avancés dans le **Module 8** !

