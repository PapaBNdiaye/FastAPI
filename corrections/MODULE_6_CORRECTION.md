# Module 6 : Correction et explications détaillées

## Correction de l'exercice 6

### 1. Exceptions personnalisées (app/exceptions.py)

```python
"""
Exceptions personnalisées pour l'API ML
"""

class ModelNotLoadedError(Exception):
    """Exception levée quand le modèle n'est pas chargé"""
    pass

class PredictionError(Exception):
    """Exception levée lors d'une erreur de prédiction"""
    pass

class InvalidFeaturesError(Exception):
    """Exception levée quand les features sont invalides"""
    pass
```

### 2. Exception handlers et amélioration de main.py

```python
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import numpy as np
from app.schemas import IrisFeatures, PredictionResponse
from app.dependencies import get_model, get_class_names
from app.exceptions import ModelNotLoadedError, PredictionError, InvalidFeaturesError

app = FastAPI(
    title="Iris Classification API",
    description="API pour classifier des fleurs Iris avec un modèle de Machine Learning.",
    version="1.0.0"
)

# ==================== Exception Handlers ====================

@app.exception_handler(ModelNotLoadedError)
async def model_not_loaded_handler(request: Request, exc: ModelNotLoadedError):
    """
    Handler pour les erreurs de modèle non chargé
    
    Explication :
    - Intercepte toutes les ModelNotLoadedError
    - Retourne une réponse JSON avec code 500
    - Format standardisé pour les erreurs
    """
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
    """
    Handler pour les erreurs de prédiction
    
    Explication :
    - Intercepte les erreurs lors de la prédiction
    - Peut être dû à un shape incorrect, valeurs invalides, etc.
    """
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
    """
    Handler pour les features invalides
    
    Explication :
    - Intercepte les erreurs de validation des features
    - Code 400 car c'est une erreur client
    """
    return JSONResponse(
        status_code=400,
        content={
            "error": "InvalidFeaturesError",
            "message": "The provided features are invalid",
            "detail": str(exc)
        }
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """
    Handler pour les ValueError génériques
    
    Explication :
    - Capture les ValueError non gérées ailleurs
    - Utile pour les erreurs de conversion de types, etc.
    """
    return JSONResponse(
        status_code=400,
        content={
            "error": "ValueError",
            "message": "Invalid value provided",
            "detail": str(exc)
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler personnalisé pour les erreurs de validation Pydantic
    
    Explication :
    - FastAPI gère déjà ces erreurs, mais on peut les personnaliser
    - Utile pour formater les erreurs de validation de manière spécifique
    """
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": "Request validation failed",
            "detail": exc.errors()
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
    Endpoint de prédiction avec gestion d'erreurs complète
    
    Explication :
    - Try/except pour capturer toutes les erreurs possibles
    - Validation des features avant prédiction
    - Messages d'erreur clairs et structurés
    """
    try:
        # Vérifier que le modèle est chargé
        if model is None:
            raise ModelNotLoadedError("Model is None")
        
        # Extraire et valider les features
        feature_values = [
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ]
        
        # Vérifier les valeurs NaN ou inf
        for i, val in enumerate(feature_values):
            if np.isnan(val) or np.isinf(val):
                raise InvalidFeaturesError(
                    f"Feature {i} contains NaN or Inf value: {val}"
                )
        
        # Créer l'array numpy
        try:
            feature_array = np.array([feature_values])
        except Exception as e:
            raise InvalidFeaturesError(f"Could not create feature array: {str(e)}")
        
        # Vérifier le shape
        if feature_array.shape != (1, 4):
            raise InvalidFeaturesError(
                f"Invalid feature shape: {feature_array.shape}, expected (1, 4)"
            )
        
        # Faire la prédiction
        try:
            prediction = model.predict(feature_array)[0]
            probabilities = model.predict_proba(feature_array)[0]
        except Exception as e:
            raise PredictionError(f"Model prediction failed: {str(e)}")
        
        # Vérifier que la prédiction est valide
        if prediction not in class_names:
            raise PredictionError(
                f"Invalid prediction: {prediction}, expected one of {list(class_names.keys())}"
            )
        
        # Calculer la probabilité
        prediction_probability = float(probabilities[prediction])
        
        # Mapper la classe
        class_name = class_names[prediction]
        
        return PredictionResponse(
            prediction=int(prediction),
            probability=prediction_probability,
            class_name=class_name,
            features=features
        )
        
    except (ModelNotLoadedError, PredictionError, InvalidFeaturesError):
        # Re-raise les exceptions personnalisées pour que les handlers les attrapent
        raise
    except Exception as e:
        # Capturer toute autre erreur inattendue
        raise PredictionError(f"Unexpected error during prediction: {str(e)}")

@app.get(
    "/test/error/{error_type}",
    summary="Tester les différents types d'erreurs",
    description="Endpoint de test pour vérifier la gestion d'erreurs",
    tags=["Testing"]
)
def test_error(error_type: str):
    """
    Endpoint pour tester différents types d'erreurs
    
    Explication :
    - Utile pour vérifier que les exception handlers fonctionnent
    - Types: "model", "prediction", "validation", "value"
    """
    if error_type == "model":
        raise ModelNotLoadedError("Test: Model not loaded")
    elif error_type == "prediction":
        raise PredictionError("Test: Prediction failed")
    elif error_type == "validation":
        raise InvalidFeaturesError("Test: Invalid features")
    elif error_type == "value":
        raise ValueError("Test: ValueError")
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown error type: {error_type}. Use: model, prediction, validation, value"
        )

@app.get("/health", tags=["Monitoring"])
def health_check(model = Depends(get_model)):
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }
```

## Points clés à retenir

### 1. Exception handlers

```python
@app.exception_handler(CustomError)
async def handler(request: Request, exc: CustomError):
    return JSONResponse(status_code=..., content={...})
```

**Ordre d'exécution :**
1. FastAPI essaie de résoudre la requête
2. Si une exception est levée, FastAPI cherche un handler
3. Si trouvé, le handler est exécuté
4. Sinon, erreur 500 par défaut

### 2. Codes HTTP appropriés

- **400** : Erreur client (données invalides)
- **422** : Erreur de validation (Pydantic)
- **500** : Erreur serveur (modèle, prédiction)

### 3. Messages d'erreur structurés

```python
{
    "error": "ErrorType",
    "message": "Message lisible",
    "detail": "Détails techniques"
}
```

**Avantages :**
- Facile à déboguer
- Format standardisé
- Messages clairs pour les utilisateurs

### 4. Try/except dans les endpoints

```python
try:
    # Code principal
    pass
except CustomError:
    raise  # Re-raise pour que le handler l'attrape
except Exception as e:
    raise CustomError(f"Unexpected: {str(e)}")
```

## Interface Docs - Gestion d'erreurs

Dans `/docs`, vous verrez :

1. **Réponses d'erreur documentées :**
   - FastAPI documente automatiquement les codes d'erreur possibles
   - vous pouvez voir les formats de réponse d'erreur

2. **Test des erreurs :**
   - Utilisez `/test/error/{error_type}` pour tester
   - Vérifiez que les messages d'erreur sont clairs

## Prochaines étapes

Maintenant que la gestion d'erreurs est robuste, nous allons ajouter du monitoring avec le **Module 7** !

