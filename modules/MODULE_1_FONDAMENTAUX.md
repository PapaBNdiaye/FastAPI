# Module 1 : Fondamentaux FastAPI

## Explication théorique

### 1. Qu'est-ce que FastAPI ?

FastAPI est un framework web moderne et rapide pour construire des APIs avec Python, basé sur les standards modernes (OpenAPI, JSON Schema).

**Avantages pour MLOps :**
- Documentation automatique (Swagger/ReDoc)
- Validation automatique des données
- Performance élevée
- Type hints natifs Python

### 2. Structure de base d'une application FastAPI

```python
from fastapi import FastAPI

app = FastAPI()  # Instance de l'application

@app.get("/")  # Décorateur pour définir une route GET
def read_root():
    return {"message": "Hello World"}
```

### 3. Méthodes HTTP dans FastAPI

FastAPI supporte toutes les méthodes HTTP standard :

- **GET** : Récupérer des données (lecture seule)
- **POST** : Créer/envoyer des données (prédictions ML)
- **PUT** : Mettre à jour complètement une ressource
- **DELETE** : Supprimer une ressource
- **PATCH** : Mettre à jour partiellement

### 4. Types de paramètres

#### a) Path Parameters (paramètres de chemin)
```python
@app.get("/items/{item_id}")
def get_item(item_id: int):  # item_id est dans l'URL
    return {"item_id": item_id}
```
**URL exemple :** `http://localhost:8000/items/42`

#### b) Query Parameters (paramètres de requête)
```python
@app.get("/items/")
def get_items(skip: int = 0, limit: int = 10):  # skip et limit sont dans ?skip=0&limit=10
    return {"skip": skip, "limit": limit}
```
**URL exemple :** `http://localhost:8000/items/?skip=0&limit=10`

#### c) Path + Query combinés
```python
@app.get("/items/{item_id}")
def get_item(item_id: int, q: str = None):  # item_id dans path, q dans query
    return {"item_id": item_id, "q": q}
```
**URL exemple :** `http://localhost:8000/items/42?q=test`

### 5. Types de retour

FastAPI peut retourner :
- **Dict** : `{"key": "value"}`
- **List** : `[1, 2, 3]`
- **Pydantic Models** : Objets validés
- **Response** : Réponses HTTP personnalisées

### 6. Décorateurs de routes

```python
@app.get("/")      # GET request
@app.post("/")     # POST request
@app.put("/")      # PUT request
@app.delete("/")   # DELETE request
```

## Exercice 1 : Créer 3 endpoints GET

**Objectif :** Créer 3 endpoints GET avec différents types de paramètres pour comprendre les concepts de base.

**Instructions :**

1. Créez un endpoint `GET /users/{user_id}` qui retourne l'ID de l'utilisateur
2. Créez un endpoint `GET /products/` qui accepte des query parameters `category` (optionnel) et `limit` (défaut: 10)
3. Créez un endpoint `GET /search/{query}` qui accepte un path parameter `query` et un query parameter `page` (défaut: 1)

**Format de réponse attendu :**
- Endpoint 1 : `{"user_id": 123}`
- Endpoint 2 : `{"category": "electronics", "limit": 10, "products": []}`
- Endpoint 3 : `{"query": "laptop", "page": 1, "results": []}`

**Fichier à modifier :** `app/main.py`

**Indices :**
- Utilisez `@app.get()` pour chaque endpoint
- Les path parameters sont définis dans la fonction avec le même nom que dans l'URL
- Les query parameters sont définis avec des valeurs par défaut
- Utilisez `Optional[str]` pour les paramètres optionnels (import depuis `typing`)

---
