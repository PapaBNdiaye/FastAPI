# Module 8 : Correction et explications détaillées

## Correction de l'exercice 8

### 1. Ajout des schémas pour batch (app/schemas.py)

Ajoutez à la fin du fichier :

```python
from typing import List

class BatchPredictionRequest(BaseModel):
    """Requête pour prédictions batch"""
    features_list: List[IrisFeatures] = Field(
        ...,
        description="Liste des features à prédire",
        min_items=1,
        max_items=100  # Limiter à 100 pour éviter la surcharge
    )

class BatchPredictionResponse(BaseModel):
    """Réponse pour prédictions batch"""
    predictions: List[PredictionResponse] = Field(
        ...,
        description="Liste des prédictions"
    )
    total: int = Field(..., description="Nombre total de prédictions")
    successful: int = Field(..., description="Nombre de prédictions réussies")
    failed: int = Field(..., description="Nombre de prédictions échouées")
```

### 2. Endpoints avancés (app/main.py)

Ajoutez au début du fichier :

```python
import time
from typing import List
from app.schemas import (
    IrisFeatures, PredictionResponse, 
    BatchPredictionRequest, BatchPredictionResponse
)
```

Ajoutez après la création de l'app :

```python
# Temps de démarrage pour calculer l'uptime
start_time = time.time()
```

Ajoutez les nouveaux endpoints :

```python
@app.post(
    "/predict/batch",
    response_model=BatchPredictionResponse,
    summary="Prédictions batch",
    description="""
    Faire des prédictions sur plusieurs fleurs Iris en une seule requête.
    
    **Avantages :**
    * Plus efficace qu'une requête par prédiction
    * Réduction de la latence réseau
    * Meilleure utilisation du modèle
    
    **Limites :**
    * Maximum 100 prédictions par requête
    * Si une prédiction échoue, les autres continuent
    """,
    tags=["ML Predictions"]
)
def predict_batch(
    batch_request: BatchPredictionRequest,
    model = Depends(get_model),
    class_names = Depends(get_class_names)
):
    """
    Endpoint pour prédictions batch
    
    Explication :
    - Accepte une liste de features
    - Fait toutes les prédictions
    - Retourne les résultats avec statistiques
    """
    predictions = []
    successful = 0
    failed = 0
    
    for features in batch_request.features_list:
        try:
            # Validation des features
            feature_values = [
                features.sepal_length,
                features.sepal_width,
                features.petal_length,
                features.petal_width
            ]
            
            # Vérifier NaN/Inf
            for val in feature_values:
                if np.isnan(val) or np.isinf(val):
                    raise InvalidFeaturesError("Feature contains NaN or Inf")
            
            # Créer l'array
            feature_array = np.array([feature_values])
            
            # Prédiction
            prediction = model.predict(feature_array)[0]
            probabilities = model.predict_proba(feature_array)[0]
            prediction_probability = float(probabilities[prediction])
            class_name = class_names[prediction]
            
            predictions.append(PredictionResponse(
                prediction=int(prediction),
                probability=prediction_probability,
                class_name=class_name,
                features=features
            ))
            successful += 1
            
        except Exception as e:
            # Si une prédiction échoue, logger et continuer
            logger.warning(f"Batch prediction failed for one item: {str(e)}")
            failed += 1
            # Optionnel : ajouter une réponse d'erreur dans la liste
            # Pour l'instant, on ignore les échecs
    
    return BatchPredictionResponse(
        predictions=predictions,
        total=len(batch_request.features_list),
        successful=successful,
        failed=failed
    )

@app.get(
    "/health",
    summary="Health check avancé",
    description="Vérifie l'état complet de l'API, du modèle et du système",
    tags=["Monitoring"]
)
def health_check(model = Depends(get_model)):
    """
    Health check amélioré avec plus d'informations
    
    Explication :
    - Vérifie l'état du modèle
    - Calcule l'uptime
    - Vérifie l'existence du fichier modèle
    """
    import os
    from pathlib import Path
    
    model_path = "C:/Users/dell/Desktop/mlops/details/fastapi/app/model.pkl"
    model_exists = os.path.exists(model_path)
    model_loaded = model is not None
    
    # Calculer l'uptime
    uptime_seconds = time.time() - start_time
    uptime_hours = uptime_seconds / 3600
    
    status = "healthy" if (model_exists and model_loaded) else "degraded"
    
    return {
        "status": status,
        "model": {
            "loaded": model_loaded,
            "file_exists": model_exists,
            "path": model_path
        },
        "api": {
            "version": "1.0.0",
            "uptime_seconds": round(uptime_seconds, 2),
            "uptime_hours": round(uptime_hours, 2)
        },
        "timestamp": time.time()
    }

@app.get(
    "/model/info",
    summary="Informations détaillées sur le modèle",
    description="Retourne des informations complètes sur le modèle ML chargé",
    tags=["ML Predictions"]
)
def model_info(model = Depends(get_model)):
    """
    Informations détaillées sur le modèle
    
    Explication :
    - Type de modèle
    - Paramètres du modèle
    - Features et classes
    """
    info = {
        "model_type": type(model).__name__,
        "model_module": type(model).__module__,
        "model_loaded": model is not None
    }
    
    if model is not None:
        # Informations sur les features
        if hasattr(model, 'n_features_in_'):
            info["n_features"] = model.n_features_in_
        
        # Informations sur les classes
        if hasattr(model, 'classes_'):
            info["n_classes"] = len(model.classes_)
            info["classes"] = model.classes_.tolist()
        
        # Paramètres du modèle (si RandomForest)
        if hasattr(model, 'n_estimators'):
            info["n_estimators"] = model.n_estimators
        if hasattr(model, 'max_depth'):
            info["max_depth"] = model.max_depth
        if hasattr(model, 'random_state'):
            info["random_state"] = model.random_state
    
    return info

@app.get(
    "/model/classes",
    summary="Liste des classes disponibles",
    description="Retourne toutes les classes que le modèle peut prédire",
    tags=["ML Predictions"]
)
def get_classes(class_names = Depends(get_class_names)):
    """
    Liste des classes avec leurs IDs et noms
    
    Explication :
    - Format structuré pour faciliter l'utilisation
    - Utile pour les interfaces utilisateur
    """
    classes = [
        {"id": class_id, "name": class_name}
        for class_id, class_name in class_names.items()
    ]
    
    return {
        "classes": classes,
        "total": len(classes)
    }
```

## Points clés à retenir

### 1. Batch Predictions

**Avantages :**
- Efficacité : une seule requête HTTP
- Performance : modèle peut optimiser les prédictions batch
- Réduction latence réseau

**Considérations :**
- Limiter la taille du batch (éviter timeout)
- Gérer les erreurs partiellement
- Logger les performances

### 2. Health Checks

**Éléments à vérifier :**
- Modèle chargé
- Fichiers existants
- Connexions (DB, cache, etc.)
- Uptime
- Version

**Codes de statut :**
- `healthy` : Tout fonctionne
- `degraded` : Fonctionne mais avec limitations
- `unhealthy` : Ne fonctionne pas

### 3. Versioning

**Stratégies :**
- URL : `/v1/predict`, `/v2/predict`
- Header : `X-API-Version: 1`
- Query param : `?version=1`

### 4. Endpoints de diagnostic

**Utiles pour :**
- Debugging
- Monitoring
- Support technique
- Documentation

## Interface Docs - Endpoints avancés

Dans `/docs`, vous verrez :

1. **POST /predict/batch** :
   - Body avec liste de features
   - Réponse avec statistiques
   - Exemple interactif

2. **GET /health** :
   - État complet du système
   - Informations de monitoring

3. **GET /model/info** :
   - Détails techniques du modèle
   - Paramètres et configuration

4. **GET /model/classes** :
   - Liste des classes disponibles
   - Format structuré

## Prochaines étapes

Maintenant que vous avez des endpoints avancés, nous allons créer des tests dans le **Module 9** !

