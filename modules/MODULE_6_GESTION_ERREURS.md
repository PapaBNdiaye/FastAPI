# Module 6 : Gestion d'erreurs et exceptions

## Explication théorique

### 1. HTTPException - Erreurs HTTP standard

```python
from fastapi import HTTPException

raise HTTPException(
    status_code=400,
    detail="Message d'erreur"
)
```

**Codes HTTP courants :**
- `200` : Succès
- `400` : Bad Request (données invalides)
- `401` : Unauthorized (non authentifié)
- `403` : Forbidden (pas les permissions)
- `404` : Not Found (ressource introuvable)
- `422` : Unprocessable Entity (validation Pydantic)
- `500` : Internal Server Error (erreur serveur)

### 2. Exception handlers personnalisés

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)}
    )
```

### 3. Gestion des erreurs de validation Pydantic

FastAPI gère automatiquement les erreurs de validation, mais vous pouvez les personnaliser :

```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

### 4. Erreurs spécifiques ML

Pour les APIs ML, vous aurez souvent :
- Erreurs de format de données
- Erreurs de prédiction
- Erreurs de modèle non chargé
- Erreurs de preprocessing

### 5. Messages d'erreur utiles

```python
raise HTTPException(
    status_code=400,
    detail={
        "error": "Invalid input",
        "message": "Features must be positive numbers",
        "received": features.dict()
    }
)
```

## Exercice 6 : Implémenter gestion d'erreurs

**Objectif :** Créer une gestion d'erreurs robuste pour notre API ML.

**Instructions :**

1. **Créer des exceptions personnalisées** dans `app/exceptions.py` :
   - `ModelNotLoadedError` : Exception personnalisée
   - `PredictionError` : Exception pour erreurs de prédiction
   - `InvalidFeaturesError` : Exception pour features invalides

2. **Créer des exception handlers** dans `app/main.py` :
   - Handler pour `ModelNotLoadedError` → 500
   - Handler pour `PredictionError` → 500
   - Handler pour `InvalidFeaturesError` → 400
   - Handler pour `ValueError` → 400

3. **Améliorer l'endpoint `/predict`** :
   - Gérer les erreurs de numpy (valeurs NaN, inf)
   - Gérer les erreurs de prédiction (shape incorrect)
   - Retourner des messages d'erreur clairs

4. **Créer un endpoint de test d'erreurs** :
   - `GET /test/error/{error_type}` pour tester différents types d'erreurs
   - Types : "model", "prediction", "validation", "value"

**Fichiers à modifier :**
- `app/exceptions.py` : Créer les exceptions
- `app/main.py` : Ajouter les handlers et améliorer `/predict`

**Indices :**
- Utilisez `@app.exception_handler()` pour les handlers
- Utilisez `try/except` dans `/predict` pour capturer les erreurs
- Retournez des messages d'erreur structurés avec détails

---

