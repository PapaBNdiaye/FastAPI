# Module 9 : Correction et explications détaillées

## Correction de l'exercice 9

### 1. Structure des tests

Créez la structure suivante :

```
tests/
  __init__.py
  conftest.py
  test_main.py
```

### 2. Configuration pytest (tests/conftest.py)

```python
"""
Configuration partagée pour les tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """
    Fixture pour créer un TestClient
    
    Explication :
    - Crée un client de test pour chaque test
    - Pas besoin de démarrer un serveur réel
    """
    return TestClient(app)

@pytest.fixture
def sample_features():
    """
    Fixture pour des features de test valides
    
    Explication :
    - Réutilisable dans plusieurs tests
    - Données de test standardisées
    """
    return {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

@pytest.fixture
def batch_features():
    """
    Fixture pour des features batch de test
    """
    return {
        "features_list": [
            {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            },
            {
                "sepal_length": 6.2,
                "sepal_width": 3.4,
                "petal_length": 5.4,
                "petal_width": 2.3
            }
        ]
    }
```

### 3. Tests principaux (tests/test_main.py)

```python
"""
Tests pour l'API Iris Classification
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import numpy as np
from app.main import app

# ==================== Tests de base ====================

def test_homepage(client: TestClient):
    """
    Test de la page d'accueil
    
    Explication :
    - Arrange : client est fourni par la fixture
    - Act : GET request sur /
    - Assert : Vérifier le status code et le contenu
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# ==================== Tests de prédiction ====================

def test_predict_valid(client: TestClient, sample_features):
    """
    Test de prédiction avec données valides
    
    Explication :
    - Envoie des features valides
    - Vérifie que la prédiction réussit
    - Vérifie le format de la réponse
    """
    response = client.post("/predict", json=sample_features)
    
    assert response.status_code == 200
    data = response.json()
    
    # Vérifier la structure de la réponse
    assert "prediction" in data
    assert "probability" in data
    assert "class_name" in data
    assert "features" in data
    
    # Vérifier les types
    assert isinstance(data["prediction"], int)
    assert isinstance(data["probability"], float)
    assert isinstance(data["class_name"], str)
    assert data["prediction"] in [0, 1, 2]
    assert 0 <= data["probability"] <= 1

def test_predict_invalid_missing_field(client: TestClient):
    """
    Test avec champ manquant
    
    Explication :
    - Envoie des données incomplètes
    - Vérifie que FastAPI retourne 422 (validation error)
    """
    invalid_data = {
        "sepal_length": 5.1,
        "sepal_width": 3.5
        # petal_length et petal_width manquants
    }
    
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422  # Validation error

def test_predict_invalid_negative_value(client: TestClient):
    """
    Test avec valeur négative
    
    Explication :
    - Envoie une valeur négative (devrait être rejetée par le validator)
    - Vérifie que l'erreur est retournée
    """
    invalid_data = {
        "sepal_length": -5.1,  # Valeur négative
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    
    response = client.post("/predict", json=invalid_data)
    # Soit 422 (validation Pydantic) soit 400 (notre handler)
    assert response.status_code in [400, 422]

def test_predict_invalid_type(client: TestClient):
    """
    Test avec type incorrect
    
    Explication :
    - Envoie une string au lieu d'un float
    - Vérifie que FastAPI retourne 422
    """
    invalid_data = {
        "sepal_length": "not a number",  # String au lieu de float
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422

# ==================== Tests batch ====================

def test_predict_batch_valid(client: TestClient, batch_features):
    """
    Test de prédiction batch avec données valides
    
    Explication :
    - Envoie une liste de features
    - Vérifie que toutes les prédictions sont retournées
    """
    response = client.post("/predict/batch", json=batch_features)
    
    assert response.status_code == 200
    data = response.json()
    
    # Vérifier la structure
    assert "predictions" in data
    assert "total" in data
    assert "successful" in data
    assert "failed" in data
    
    # Vérifier les valeurs
    assert data["total"] == len(batch_features["features_list"])
    assert data["successful"] == data["total"]
    assert data["failed"] == 0
    assert len(data["predictions"]) == data["total"]

def test_predict_batch_empty(client: TestClient):
    """
    Test batch avec liste vide
    
    Explication :
    - Devrait être rejeté par la validation (min_items=1)
    """
    response = client.post("/predict/batch", json={"features_list": []})
    assert response.status_code == 422

def test_predict_batch_too_large(client: TestClient):
    """
    Test batch avec trop d'éléments
    
    Explication :
    - Devrait être rejeté (max_items=100)
    """
    large_list = {
        "features_list": [
            {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        ] * 101  # 101 éléments
    }
    
    response = client.post("/predict/batch", json=large_list)
    assert response.status_code == 422

# ==================== Tests health check ====================

def test_health_check(client: TestClient):
    """
    Test du health check
    
    Explication :
    - Vérifie que l'endpoint retourne les bonnes informations
    """
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    # Vérifier la structure
    assert "status" in data
    assert "model" in data
    assert "api" in data
    
    # Vérifier les sous-structures
    assert "loaded" in data["model"]
    assert "file_exists" in data["model"]
    assert "version" in data["api"]
    assert "uptime_seconds" in data["api"]

# ==================== Tests model info ====================

def test_model_info(client: TestClient):
    """
    Test des informations du modèle
    
    Explication :
    - Vérifie que les informations du modèle sont retournées
    """
    response = client.get("/model/info")
    
    assert response.status_code == 200
    data = response.json()
    
    # Vérifier les champs de base
    assert "model_type" in data
    assert "model_loaded" in data
    assert data["model_loaded"] is True

def test_model_classes(client: TestClient):
    """
    Test de la liste des classes
    
    Explication :
    - Vérifie que toutes les classes sont retournées
    """
    response = client.get("/model/classes")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "classes" in data
    assert "total" in data
    assert data["total"] == 3
    assert len(data["classes"]) == 3
    
    # Vérifier la structure de chaque classe
    for cls in data["classes"]:
        assert "id" in cls
        assert "name" in cls
        assert cls["id"] in [0, 1, 2]

# ==================== Tests métriques ====================

def test_metrics(client: TestClient):
    """
    Test des métriques
    
    Explication :
    - Vérifie que les métriques sont retournées
    """
    # Faire quelques prédictions pour générer des métriques
    features = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    client.post("/predict", json=features)
    
    # Vérifier les métriques
    response = client.get("/metrics")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "total_requests" in data
    assert "total_predictions" in data
    assert "average_prediction_time_seconds" in data
    assert "errors" in data

# ==================== Tests d'erreurs ====================

def test_error_endpoints(client: TestClient):
    """
    Test des endpoints d'erreur de test
    
    Explication :
    - Vérifie que les différents types d'erreurs sont gérés
    """
    # Test erreur modèle
    response = client.get("/test/error/model")
    assert response.status_code == 500
    assert "error" in response.json()
    
    # Test erreur prédiction
    response = client.get("/test/error/prediction")
    assert response.status_code == 500
    
    # Test erreur validation
    response = client.get("/test/error/validation")
    assert response.status_code == 400
    
    # Test erreur inconnue
    response = client.get("/test/error/unknown")
    assert response.status_code == 404
```

### 4. Exécution des tests

Créez un fichier `pytest.ini` à la racine :

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

Pour exécuter les tests :

```bash
pytest
pytest -v  # Verbose
pytest tests/test_main.py::test_predict_valid  # Test spécifique
```

## Points clés à retenir

### 1. Structure AAA (Arrange-Act-Assert)

```python
def test_example():
    # Arrange : Préparer
    data = {...}
    
    # Act : Exécuter
    response = client.post("/endpoint", json=data)
    
    # Assert : Vérifier
    assert response.status_code == 200
```

### 2. Fixtures pytest

```python
@pytest.fixture
def client():
    return TestClient(app)

def test_something(client):
    # client est automatiquement injecté
    pass
```

### 3. Tests de validation

**Toujours tester :**
- Cas valides
- Cas invalides (types, valeurs, champs manquants)
- Cas limites (vides, trop grands, etc.)

### 4. Mock des dépendances

```python
with patch('module.function') as mock:
    mock.return_value = fake_value
    # Test avec la dépendance mockée
```

## Exécution et couverture

**Commandes utiles :**

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=app --cov-report=html

# Tests spécifiques
pytest tests/test_main.py::test_predict_valid

# Mode verbose
pytest -v

# Arrêter au premier échec
pytest -x
```

## Prochaines étapes

Maintenant que vous avez des tests, nous allons préparer le déploiement dans le **Module 10** !

