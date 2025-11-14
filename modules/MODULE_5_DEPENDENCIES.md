# Module 5 : Dependencies et injection

## Explication théorique

### 1. Qu'est-ce que Depends() ?

`Depends()` permet d'injecter des dépendances dans nos endpoints. C'est très utile pour :
- Réutiliser du code
- Gérer l'état (comme le chargement de modèles ML)
- Tester facilement (mock des dépendances)

### 2. Dépendances simples

```python
from fastapi import Depends

def get_db():
    db = connect_to_db()
    return db

@app.get("/items")
def get_items(db = Depends(get_db)):
    return db.query(...)
```

### 3. Dépendances pour modèles ML

**Problème actuel :** Le modèle est chargé au niveau global, ce qui pose des problèmes :
- Difficile à tester
- Pas de gestion d'erreur au chargement
- Pas de lifecycle management

**Solution :** Utiliser une dépendance

```python
def get_model():
    if model_cache is None:
        model_cache = load_model()
    return model_cache

@app.post("/predict")
def predict(features: IrisFeatures, model = Depends(get_model)):
    # Utiliser model
    pass
```

### 4. Singleton pattern pour modèles

```python
_model = None

def get_model():
    global _model
    if _model is None:
        _model = joblib.load("model.pkl")
    return _model
```

### 5. Dépendances avec paramètres

```python
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/users/{user_id}")
def read_user(user = Depends(get_user)):
    return user
```

### 6. Dépendances réutilisables

```python
from fastapi import Depends, Header

def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401)
    return authorization

@app.post("/predict")
def predict(
    features: IrisFeatures,
    token = Depends(verify_token),
    model = Depends(get_model)
):
    pass
```

## Exercice 5 : Refactoriser avec dependencies

**Objectif :** Refactoriser le chargement du modèle avec une dépendance réutilisable.

**Instructions :**

1. **Créer une dépendance `get_model()`** dans `app/dependencies.py` :
   - Utilisez un pattern singleton (variable globale)
   - Chargez le modèle une seule fois
   - Gérez les erreurs de chargement
   - Retournez le modèle ou lève une HTTPException

2. **Créer une dépendance `get_class_names()`** :
   - Retourne le mapping des classes
   - Peut être réutilisé dans plusieurs endpoints

3. **Modifier `app/main.py`** :
   - Supprimez le chargement global du modèle
   - Utilisez `Depends(get_model)` dans l'endpoint `/predict`
   - Utilisez `Depends(get_class_names)` dans `/predict`

4. **Créer un endpoint `/model/info`** :
   - GET endpoint qui retourne des infos sur le modèle
   - Utilise la dépendance `get_model()`
   - Tag: "ML Predictions"

**Fichiers à modifier :**
- `app/dependencies.py` : Créer les dépendances
- `app/main.py` : Utiliser les dépendances

**Indices :**
- Utilisez une variable globale `_model = None` pour le singleton
- Utilisez `try/except` pour gérer les erreurs de chargement
- Le chemin du modèle peut être dans une variable ou constante

---

