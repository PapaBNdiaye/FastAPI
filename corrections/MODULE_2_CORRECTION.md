# Module 2 : Correction et explications détaillées

## Correction de l'exercice 2

Voici la solution complète avec explications :

```python
"""
Modèles Pydantic pour la validation des données ML
"""
from pydantic import BaseModel, validator
from typing import Optional, List

# Modèle pour les features d'entrée Iris
class IrisFeatures(BaseModel):
    """
    Modèle pour valider les 4 features d'une fleur Iris
    
    Explication :
    - Chaque champ est typé (float)
    - FastAPI valide automatiquement le type
    - Si vous envoyez "5.1" (string), Pydantic le convertit en 5.1 (float)
    """
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    
    @validator('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
    def validate_positive(cls, v):
        """
        Validator personnalisé qui vérifie que toutes les valeurs sont positives
        
        Explication :
        - @validator() s'applique aux champs listés
        - cls est la classe (IrisFeatures)
        - v est la valeur à valider
        - Si la validation échoue, on lève ValueError
        - Si la validation réussit, on retourne la valeur (éventuellement modifiée)
        """
        if v < 0:
            raise ValueError('All features must be positive')
        return v
    
    # Alternative : validator pour tous les champs en une fois
    @validator('*')
    def validate_all_positive(cls, v):
        """Valide que toutes les valeurs sont positives"""
        if v < 0:
            raise ValueError('All features must be positive')
        return v


# Modèle pour la réponse de prédiction
class PredictionResponse(BaseModel):
    """
    Modèle pour la réponse d'une prédiction
    
    Explication :
    - prediction: la classe prédite (0, 1, ou 2)
    - probability: la probabilité de confiance
    - class_name: le nom lisible de la classe
    - features: les features utilisées (référence au modèle IrisFeatures)
    """
    prediction: int
    probability: float
    class_name: str
    features: IrisFeatures
    
    @validator('prediction')
    def validate_prediction(cls, v):
        """Valide que la prédiction est entre 0 et 2"""
        if v not in [0, 1, 2]:
            raise ValueError('Prediction must be 0, 1, or 2')
        return v
    
    @validator('probability')
    def validate_probability(cls, v):
        """Valide que la probabilité est entre 0 et 1"""
        if not 0 <= v <= 1:
            raise ValueError('Probability must be between 0 and 1')
        return v


# Modèle pour les informations du modèle
class ModelInfo(BaseModel):
    """
    Modèle pour stocker les métadonnées du modèle ML
    
    Explication :
    - model_name: obligatoire
    - model_version: optionnel (peut être None)
    - accuracy: optionnel (peut être None)
    """
    model_name: str
    model_version: Optional[str] = None
    accuracy: Optional[float] = None
    
    @validator('accuracy')
    def validate_accuracy(cls, v):
        """Valide que l'accuracy est entre 0 et 1 si fournie"""
        if v is not None and not 0 <= v <= 1:
            raise ValueError('Accuracy must be between 0 and 1')
        return v
```

## Points clés à retenir

### 1. Validation automatique

Pydantic valide automatiquement :
- **Types** : `float` accepte int (5 → 5.0) mais pas string ("abc")
- **Conversion** : "5.1" → 5.1 automatiquement
- **Erreurs** : Retourne 422 si validation échoue

### 2. Validators personnalisés

**Syntaxe :**
```python
@validator('field_name')
def validate_field(cls, v):
    # v est la valeur à valider
    if condition:
        raise ValueError('message')
    return v  # Retourne la valeur (peut être modifiée)
```

**Validator pour plusieurs champs :**
```python
@validator('field1', 'field2', 'field3')
def validate_multiple(cls, v):
    # S'applique à tous les champs listés
    return v
```

**Validator pour tous les champs :**
```python
@validator('*')
def validate_all(cls, v):
    # S'applique à tous les champs
    return v
```

### 3. Types optionnels

```python
# Optionnel avec None par défaut
field: Optional[str] = None

# Optionnel avec valeur par défaut
field: int = 10

# Obligatoire
field: str  # Pas de valeur par défaut
```

### 4. Utilisation dans FastAPI

```python
from app.schemas import IrisFeatures

@app.post("/predict")
def predict(features: IrisFeatures):  # FastAPI valide automatiquement
    # features est déjà validé et typé
    return {"prediction": 1}
```

## Interface Docs - Impact de Pydantic

Dans `/docs`, vous verrez maintenant :

1. **Schémas automatiques** :
   - Section "Schemas" avec tous nos modèles
   - Types de chaque champ
   - Champs obligatoires vs optionnels
   - Exemples de valeurs

2. **Validation dans l'interface** :
   - Essayez d'envoyer des valeurs invalides
   - FastAPI montre les erreurs de validation
   - Messages d'erreur clairs

3. **Exemples interactifs** :
   - Cliquez sur "Schema" pour voir la structure
   - Utilisez "Example Value" pour tester

## Prochaines étapes

Maintenant que vous maîtrisez Pydantic, nous allons créer notre premier endpoint de prédiction ML dans le **Module 3** !

