# Module 2 : Pydantic et validation des données

## Explication théorique

### 1. Qu'est-ce que Pydantic ?

Pydantic est une bibliothèque de validation de données qui utilise les annotations de type Python. 
Elle est intégrée nativement dans `FastAPI`.

**Avantages pour MLOps :**
- Validation automatique des features ML
- Conversion de types automatique
- Documentation automatique des schémas
- Gestion des erreurs claire

### 2. BaseModel - Le cœur de Pydantic

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str
```

**Ce que fait Pydantic automatiquement :**
- Valide que `name` est une string
- Valide que `age` est un int (convertit "25" → 25)
- Valide que `email` est une string
- Génère une erreur si les types ne correspondent pas

### 3. Types optionnels et valeurs par défaut

```python
from typing import Optional

class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None  # Optionnel, défaut = None
    in_stock: bool = True  # Optionnel avec valeur par défaut
```

### 4. Types Union pour plusieurs possibilités

```python
from typing import Union

class Response(BaseModel):
    status: Union[str, int]  # Peut être string OU int
    message: str
```

### 5. Validators personnalisés

```python
from pydantic import BaseModel, validator

class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    
    @validator('sepal_length')
    def validate_sepal_length(cls, v):
        if v < 0 or v > 20:
            raise ValueError('sepal_length must be between 0 and 20')
        return v
```

### 6. Modèles pour MLOps

Pour les APIs ML, on aura typiquement :

**Input Model** (données d'entrée) :
```python
class PredictionInput(BaseModel):
    features: List[float]  # Les features du modèle
```

**Output Model** (données de sortie) :
```python
class PredictionOutput(BaseModel):
    prediction: int
    probability: float
    class_name: str
```

## Exercice 2 : Créer des modèles Pydantic pour données ML

**Objectif :** Créer des modèles Pydantic pour notre API de classification Iris.

**Instructions :**

1. Créez un modèle `IrisFeatures` dans `app/schemas.py` avec :
   - `sepal_length: float` (obligatoire)
   - `sepal_width: float` (obligatoire)
   - `petal_length: float` (obligatoire)
   - `petal_width: float` (obligatoire)
   - Ajoutez un validator pour vérifier que toutes les valeurs sont positives

2. Créez un modèle `PredictionResponse` avec :
   - `prediction: int` (la classe prédite : 0, 1, ou 2)
   - `probability: float` (probabilité de la prédiction)
   - `class_name: str` (nom de la classe : "setosa", "versicolor", "virginica")
   - `features: IrisFeatures` (les features utilisées)

3. Créez un modèle `ModelInfo` avec :
   - `model_name: str`
   - `model_version: Optional[str] = None`
   - `accuracy: Optional[float] = None`

**Fichier à modifier :** `app/schemas.py`

**Indices :**
- Utilisez `from pydantic import BaseModel, validator`
- Utilisez `from typing import Optional, List`
- Les noms de classes doivent être en PascalCase
- Les noms de champs doivent être en snake_case

