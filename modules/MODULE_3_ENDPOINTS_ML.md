# Module 3 : Endpoints ML - Prédictions

## Explication théorique

### 1. POST pour les prédictions ML

En MLOps, on utilise généralement **POST** pour les prédictions car :
- On envoie des données (features) dans le body
- Les données peuvent être volumineuses
- C'est plus sécurisé que GET (pas dans l'URL)

### 2. Structure d'un endpoint de prédiction

```python
@app.post("/predict")
def predict(features: IrisFeatures):
    # 1. Recevoir les features (déjà validées par Pydantic)
    # 2. Preprocessing si nécessaire
    # 3. Faire la prédiction
    # 4. Retourner le résultat
    pass
```

### 3. Preprocessing des données

Avant de faire une prédiction, on doit souvent :
- Convertir en numpy array
- Reshaper si nécessaire
- Normaliser/standardiser
- Gérer les valeurs manquantes

### 4. Format de réponse standardisé

Pour MLOps, on standardise nos réponses :
```python
{
    "prediction": 1,
    "probability": 0.95,
    "class_name": "versicolor",
    "features": {...},
    "model_version": "1.0"
}
```

### 5. Gestion des erreurs

```python
from fastapi import HTTPException

if model is None:
    raise HTTPException(status_code=500, detail="Model not loaded")
```

## Exercice 3 : Implémenter un endpoint `/predict`

**Objectif :** Créer un endpoint POST pour faire des prédictions avec notre modèle Iris.

**Instructions :**

1. Créez un endpoint `POST /predict` qui :
   - Accepte un `IrisFeatures` dans le body
   - Charge les features dans un numpy array
   - Fait la prédiction avec le modèle
   - Calcule les probabilités
   - Retourne un `PredictionResponse`

2. Mappez les classes prédites aux noms :
   - 0 → "setosa"
   - 1 → "versicolor"
   - 2 → "virginica"

3. Gérer le cas où le modèle n'est pas chargé (HTTPException 500)

4. Le format de réponse doit utiliser nos modèles Pydantic

**Fichier à modifier :** `app/main.py`

**Indices :**
- Utilisez `model.predict()` pour la prédiction
- Utilisez `model.predict_proba()` pour les probabilités
- Convertissez les features en numpy array : `np.array([[sepal_length, sepal_width, petal_length, petal_width]])`
- Utilisez `model.classes_` ou créez un mapping manuel pour les noms de classes

**Exemple de requête :**
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

