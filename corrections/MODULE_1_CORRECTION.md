# Module 1 : Correction et explications détaillées

## Correction de l'exercice 1

Voici la solution complète avec explications ligne par ligne :

```python
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Endpoint 1 : Path parameter uniquement
@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Explication :
    - {user_id} dans l'URL est automatiquement extrait
    - Le type int garantit la conversion et validation automatique
    - Si vous passez "abc" au lieu d'un nombre, FastAPI retourne une erreur 422
    """
    return {"user_id": user_id}

# Endpoint 2 : Query parameters uniquement
@app.get("/products/")
def get_products(category: Optional[str] = None, limit: int = 10):
    """
    Explication :
    - Pas de {param} dans l'URL, donc ce sont des query parameters
    - Optional[str] = None rend le paramètre optionnel
    - limit: int = 10 a une valeur par défaut
    - URL exemple : /products/?category=electronics&limit=20
    """
    return {
        "category": category,
        "limit": limit,
        "products": []  # Liste vide pour l'exemple
    }

# Endpoint 3 : Path + Query combinés
@app.get("/search/{query}")
def search(query: str, page: int = 1):
    """
    Explication :
    - {query} est un path parameter (obligatoire)
    - page est un query parameter avec valeur par défaut
    - URL exemple : /search/laptop?page=2
    """
    return {
        "query": query,
        "page": page,
        "results": []  # Liste vide pour l'exemple
    }
```

## Points clés à retenir

### 1. Path Parameters vs Query Parameters

**Path Parameters** (dans l'URL) :
- Définis avec `{nom}` dans le chemin
- Toujours obligatoires (sauf si vous utilisez des valeurs par défaut avec `Optional`)
- Exemple : `/users/{user_id}` → `user_id` est extrait de l'URL

**Query Parameters** (après `?`) :
- Définis comme paramètres de fonction avec valeurs par défaut
- Optionnels si vous utilisez `Optional` ou valeur par défaut
- Exemple : `/products/?category=electronics` → `category` vient de `?category=electronics`

### 2. Validation automatique des types

FastAPI valide automatiquement les types :
- `user_id: int` → Si vous passez "abc", erreur 422
- `limit: int = 10` → Convertit "20" en 20 automatiquement

### 3. Ordre des paramètres

**RÈGLE IMPORTANTE :**
1. Path parameters d'abord (dans l'ordre de l'URL)
2. Query parameters ensuite
3. Body parameters en dernier (pour POST/PUT)

```python
#  CORRECT
@app.get("/items/{item_id}")
def get_item(item_id: int, q: Optional[str] = None):
    pass

#  INCORRECT - l'ordre compte !
@app.get("/items/{item_id}")
def get_item(q: Optional[str] = None, item_id: int):  # Erreur !
    pass
```

## Interface Docs - Démonstration

Une fois notre serveur lancé avec `uvicorn app.main:app --reload`, accédez à :

1. **Swagger UI** : `http://localhost:8000/docs`
   - Interface interactive
   - Testez directement nos endpoints
   - Voir les schémas de requête/réponse

2. **ReDoc** : `http://localhost:8000/redoc`
   - Documentation alternative
   - Plus lisible pour la documentation

### Ce que vous verrez dans /docs :

- **GET /users/{user_id}**
  - Paramètre : `user_id` (path, required, integer)
  - Réponse : JSON avec `user_id`

- **GET /products/**
  - Paramètres : `category` (query, optional, string), `limit` (query, default: 10, integer)
  - Réponse : JSON avec category, limit, products

- **GET /search/{query}**
  - Paramètres : `query` (path, required, string), `page` (query, default: 1, integer)
  - Réponse : JSON avec query, page, results

### Tester dans l'interface :

1. Cliquez sur un endpoint
2. Cliquez sur "Try it out"
3. Entrez les paramètres
4. Cliquez sur "Execute"
5. Voyez la réponse en bas

## Prochaines étapes

Maintenant que vous maîtrisez les bases, nous allons passer au **Module 2 : Pydantic et validation des données** pour créer des modèles de données robustes pour nos APIs ML.