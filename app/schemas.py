"""
Modèles Pydantic pour la validation des données ML
"""
from pydantic import BaseModel, validator
from typing import Optional

#===================================================
# Modèle pour les features d'entrée Iris
#===================================================

class IrisFeatures(BaseModel):
    """
    Modèle pour valider les 4 features d'une fleur Iris
    """
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    
    @validator('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
    def validate_positive(cls, v):
        """Valide que toutes les valeurs sont positives"""
        if v < 0:
            raise ValueError('All features must be positive')
        return v

#===================================================
# Modèle pour la réponse de prédiction
#===================================================

class PredictionResponse(BaseModel):
    """
    Modèle pour la réponse d'une prédiction
    """
    prediction: int
    probability: float
    class_name: str
    features: IrisFeatures

#===================================================
# Modèle pour les informations du modèle
#===================================================

class ModelInfo(BaseModel):
    """
    Modèle pour stocker les métadonnées du modèle ML
    """
    model_name: str
    model_version: Optional[str] = None
    accuracy: Optional[float] = None