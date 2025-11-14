# Module 5 : Correction et explications détaillées

## Correction de l'exercice 5

### 1. Dépendances (app/dependencies.py)

```python
"""
Dépendances réutilisables pour FastAPI
"""
from fastapi import HTTPException
import joblib
import os

# Pattern Singleton pour le modèle
_model = None
_model_path = "C:/Users/dell/Desktop/mlops/details/fastapi/app/model.pkl"

# Mapping des classes (constant)
CLASS_NAMES = {
    0: "setosa",
    1: "versicolor",
    2: "virginica"
}

def get_model():
    """
    Dépendance pour obtenir le modèle ML chargé
    
    Explication :
    - Utilise le pattern Singleton pour charger le modèle une seule fois
    - Cache le modèle dans une variable globale _model
    - Gère les erreurs de chargement
    
    Returns:
        Modèle scikit-learn chargé
        
    Raises:
        HTTPException: Si le modèle ne peut pas être chargé
    """
    global _model
    
    # Si le modèle est déjà chargé, le retourner
    if _model is not None:
        return _model
    
    # Sinon, charger le modèle
    try:
        if not os.path.exists(_model_path):
            raise HTTPException(
                status_code=500,
                detail=f"Model file not found at {_model_path}"
            )
        
        _model = joblib.load(_model_path)
        return _model
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error loading model: {str(e)}"
        )

def get_class_names():
    """
    Dépendance pour obtenir le mapping des classes
    
    Returns:
        dict: Mapping des classes (int -> str)
    """
    return CLASS_NAMES
```

### 2. Utilisation dans main.py

```python
from fastapi import FastAPI, HTTPException, Depends
import numpy as np
from app.schemas import IrisFeatures, PredictionResponse
from app.dependencies import get_model, get_class_names

# Plus besoin de charger le modèle ici !
# model = joblib.load(...)  #  Supprimé

app = FastAPI(
    title="Iris Classification API",
    description="API pour classifier des fleurs Iris avec un modèle de Machine Learning.",
    version="1.0.0"
)

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
    model = Depends(get_model),  #  Injection de dépendance
    class_names = Depends(get_class_names)  #  Injection de dépendance
):
    """
    Endpoint de prédiction avec dépendances injectées
    
    Explication :
    - model est automatiquement injecté par FastAPI
    - class_names est également injecté
    - Pas besoin de vérifier si model est None, la dépendance le garantit
    """
    # Convertir les features en array numpy
    feature_array = np.array([[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width
    ]])
    
    # Prédiction
    prediction = model.predict(feature_array)[0]
    probabilities = model.predict_proba(feature_array)[0]
    prediction_probability = probabilities[prediction]
    
    # Mapper la classe
    class_name = class_names[prediction]
    
    return PredictionResponse(
        prediction=int(prediction),
        probability=float(prediction_probability),
        class_name=class_name,
        features=features
    )

@app.get(
    "/model/info",
    summary="Informations sur le modèle",
    description="Retourne des informations sur le modèle ML chargé",
    tags=["ML Predictions"]
)
def model_info(model = Depends(get_model)):
    """
    Endpoint pour obtenir des informations sur le modèle
    
    Explication :
    - Utilise la même dépendance get_model()
    - Le modèle est chargé une seule fois (singleton)
    - Retourne des métadonnées utiles
    """
    return {
        "model_type": type(model).__name__,
        "model_loaded": model is not None,
        "n_features": model.n_features_in_ if hasattr(model, 'n_features_in_') else None,
        "n_classes": len(model.classes_) if hasattr(model, 'classes_') else None,
        "classes": model.classes_.tolist() if hasattr(model, 'classes_') else None
    }

@app.get(
    "/health",
    summary="Vérifier l'état de l'API",
    description="Vérifie si l'API et le modèle sont opérationnels",
    tags=["Monitoring"]
)
def health_check(model = Depends(get_model)):
    """
    Health check avec vérification du modèle
    
    Explication :
    - Utilise la dépendance pour vérifier que le modèle peut être chargé
    - Si le modèle ne peut pas être chargé, l'exception est levée automatiquement
    """
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }
```

## Points clés à retenir

### 1. Pattern Singleton

```python
_model = None

def get_model():
    global _model
    if _model is None:
        _model = load_model()
    return _model
```

**Avantages :**
- Le modèle est chargé une seule fois
- Économise de la mémoire
- Plus rapide (pas de rechargement)

### 2. Injection de dépendances

```python
def predict(features: IrisFeatures, model = Depends(get_model)):
    # model est automatiquement injecté
    pass
```

**Avantages :**
- Code réutilisable
- Facile à tester (mock des dépendances)
- Séparation des responsabilités

### 3. Ordre des dépendances

FastAPI résout les dépendances dans l'ordre :
1. Path parameters
2. Query parameters
3. Dependencies (dans l'ordre)
4. Body

### 4. Dépendances avec paramètres

```python
def get_item(item_id: int):
    return {"id": item_id}

@app.get("/items/{item_id}")
def read_item(item = Depends(get_item)):
    # item_id est automatiquement passé à get_item
    pass
```

### 5. Dépendances multiples

```python
@app.post("/predict")
def predict(
    features: IrisFeatures,
    model = Depends(get_model),
    class_names = Depends(get_class_names),
    auth = Depends(verify_token)
):
    # Toutes les dépendances sont résolues automatiquement
    pass
```

## Interface Docs - Impact des dépendances

Dans `/docs`, vous verrez :

1. **Dépendances listées :**
   - Les dépendances apparaissent dans la documentation
   - Vous pouvez voir quels endpoints utilisent quelles dépendances

2. **Test simplifié :**
   - Les dépendances sont résolues automatiquement
   - Vous testez seulement les paramètres de l'endpoint

3. **Séparation claire :**
   - La logique métier est séparée de la logique de chargement
   - Code plus maintenable

## Prochaines étapes

Maintenant que notre architecture est propre, nous allons gérer les erreurs proprement dans le **Module 6** !

