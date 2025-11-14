# Module 9 : Tests et validation

## Explication théorique

### 1. TestClient de FastAPI

FastAPI fournit `TestClient` pour tester notre API sans serveur :

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
```

### 2. Types de tests

**Tests unitaires :**
- Tester une fonction isolée
- Mock des dépendances

**Tests d'intégration :**
- Tester un endpoint complet
- Vérifier le flux complet

**Tests end-to-end :**
- Tester l'API complète
- Scénarios réels

### 3. Structure des tests

```python
def test_endpoint_name():
    # Arrange : Préparer les données
    data = {...}
    
    # Act : Exécuter l'action
    response = client.post("/endpoint", json=data)
    
    # Assert : Vérifier le résultat
    assert response.status_code == 200
    assert response.json()["field"] == expected_value
```

### 4. Mock des dépendances

```python
from unittest.mock import patch

def test_predict_with_mock():
    with patch('app.dependencies.get_model') as mock_model:
        mock_model.return_value = fake_model
        response = client.post("/predict", json={...})
        assert response.status_code == 200
```

### 5. Fixtures avec pytest

```python
import pytest

@pytest.fixture
def client():
    return TestClient(app)

def test_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
```

## Exercice 9 : Écrire des tests

**Objectif :** Créer une suite de tests complète pour notre API.

**Instructions :**

1. **Installer pytest** :
   - Ajoutez `pytest` et `pytest-asyncio` aux dépendances

2. **Créer `tests/` directory** :
   - `tests/__init__.py`
   - `tests/test_main.py`

3. **Tests pour `/predict`** :
   - Test avec données valides
   - Test avec données invalides (NaN, valeurs négatives)
   - Test avec modèle non chargé (mock)

4. **Tests pour `/predict/batch`** :
   - Test avec liste valide
   - Test avec liste vide
   - Test avec mix de valides/invalides

5. **Tests pour `/health`** :
   - Vérifier le format de réponse
   - Vérifier que le modèle est chargé

6. **Tests pour `/model/info`** :
   - Vérifier les informations retournées

**Fichiers à créer :**
- `tests/__init__.py`
- `tests/test_main.py`
- `tests/conftest.py` (optionnel, pour fixtures partagées)

**Indices :**
- Utilisez `TestClient` de FastAPI
- Utilisez `assert` pour les vérifications
- Utilisez `pytest` pour exécuter les tests
- Mock les dépendances si nécessaire

---

