# Module 8 : Endpoints avancés ML

## Explication théorique

### 1. Batch Predictions

Au lieu de prédire une fleur à la fois, prédire plusieurs en une seule requête :

```python
@app.post("/predict/batch")
def predict_batch(features_list: List[IrisFeatures]):
    predictions = []
    for features in features_list:
        pred = model.predict(...)
        predictions.append(pred)
    return predictions
```

**Avantages :**
- Plus efficace (une seule requête HTTP)
- Meilleure utilisation du modèle
- Réduction de la latence réseau

### 2. Health Checks avancés

```python
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "loaded",
        "database": "connected",
        "version": "1.0.0"
    }
```

### 3. Métriques du modèle

```python
@app.get("/model/metrics")
def model_metrics():
    return {
        "accuracy": 0.95,
        "precision": 0.94,
        "recall": 0.96
    }
```

### 4. Versioning de l'API

```python
@app.post("/v1/predict")
@app.post("/v2/predict")  # Nouvelle version
```

### 5. Endpoints de diagnostic

```python
@app.get("/diagnostics")
def diagnostics():
    return {
        "model_info": {...},
        "system_info": {...},
        "performance": {...}
    }
```

## Exercice 8 : Créer endpoints avancés

**Objectif :** Créer des endpoints avancés pour une API ML production-ready.

**Instructions :**

1. **Créer un endpoint `/predict/batch`** :
   - POST endpoint qui accepte une liste de `IrisFeatures`
   - Retourne une liste de `PredictionResponse`
   - Gérer les erreurs (si une prédiction échoue, continuer avec les autres)
   - Tag: "ML Predictions"

2. **Améliorer `/health`** :
   - Vérifier que le modèle est chargé
   - Vérifier que le fichier de modèle existe
   - Retourner la version de l'API
   - Retourner l'uptime (temps depuis le démarrage)

3. **Créer `/model/info` amélioré** :
   - Retourner plus d'informations sur le modèle
   - Type de modèle, nombre de features, classes, etc.
   - Tag: "ML Predictions"

4. **Créer `/model/classes`** :
   - GET endpoint qui retourne toutes les classes disponibles
   - Format: `{"classes": [{"id": 0, "name": "setosa"}, ...]}`
   - Tag: "ML Predictions"

**Fichiers à modifier :**
- `app/main.py` : Ajouter les nouveaux endpoints
- `app/schemas.py` : Ajouter `BatchPredictionRequest` et `BatchPredictionResponse` si nécessaire

**Indices :**
- Utilisez `List[IrisFeatures]` pour le batch
- Utilisez `time.time()` pour calculer l'uptime
- Stockez `start_time` au démarrage de l'app

---

