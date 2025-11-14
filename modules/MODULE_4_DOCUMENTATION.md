# Module 4 : Documentation automatique (Swagger/ReDoc)

## Explication théorique

### 1. Documentation automatique dans FastAPI

FastAPI génère automatiquement :
- **Swagger UI** : `/docs` - Interface interactive
- **ReDoc** : `/redoc` - Documentation alternative
- **OpenAPI Schema** : `/openapi.json` - Schéma JSON

**Avantages :**
- Pas besoin d'écrire la documentation manuellement
- Toujours à jour avec le code
- Testable directement dans le navigateur

### 2. Améliorer la documentation

#### a) Descriptions et résumés

```python
@app.post(
    "/predict",
    summary="Faire une prédiction Iris",  # Titre court
    description="Cet endpoint prend les 4 features d'une fleur Iris et retourne la classe prédite avec sa probabilité",  # Description longue
    response_model=PredictionResponse
)
```

#### b) Tags pour organiser

```python
@app.post("/predict", tags=["ML Predictions"])
@app.get("/health", tags=["Monitoring"])
```

#### c) Exemples de requêtes

```python
from pydantic import BaseModel, Field

class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., example=5.1, description="Longueur du sépale en cm")
    sepal_width: float = Field(..., example=3.5, description="Largeur du sépale en cm")
    # ...
```

#### d) Exemples de réponses

```python
from fastapi.responses import JSONResponse

@app.post("/predict")
def predict(...):
    return PredictionResponse(...)
    # FastAPI utilise response_model pour générer l'exemple
```

#### e) Métadonnées de l'API

```python
app = FastAPI(
    title="Iris Classification API",
    description="API pour classifier des fleurs Iris avec un modèle ML",
    version="1.0.0",
    contact={
        "name": "Notre nom",
        "email": "notre@email.com"
    }
)
```

## Exercice 4 : Améliorer la documentation

**Objectif :** Améliorer la documentation de notre API avec descriptions, tags, exemples.

**Instructions :**

1. **Métadonnées de l'application** :
   - Ajoutez `title`, `description`, `version` à `FastAPI()`
   - Ajoutez des informations de contact

2. **Améliorer les modèles Pydantic** :
   - Ajoutez `Field()` avec `description` et `example` pour chaque champ de `IrisFeatures`
   - Faites de même pour `PredictionResponse`

3. **Améliorer les endpoints** :
   - Ajoutez `summary` et `description` à chaque endpoint
   - Ajoutez des `tags` pour organiser (ex: "ML Predictions", "Monitoring")

4. **Créer un endpoint `/health`** :
   - GET endpoint qui retourne `{"status": "healthy", "model_loaded": True/False}`
   - Tag: "Monitoring"
   - Description: "Vérifier l'état de l'API et du modèle"

**Fichiers à modifier :**
- `app/main.py` : Métadonnées et endpoints
- `app/schemas.py` : Field() avec descriptions

**Indices :**
- `Field(..., description="...", example=...)` pour les champs obligatoires
- `Field(default=..., description="...", example=...)` pour les champs optionnels
- Importez `Field` depuis `pydantic`

---