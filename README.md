# Programme d'apprentissage FastAPI pour MLOps
# Auteur : NDIAYE Papa - AI/ML ENGINEER

Bienvenue dans ce programme complet d'apprentissage de FastAPI pour le MLOps ! Ce programme vous guidera pas à pas pour maîtriser FastAPI et créer des APIs ML production-ready.

## Objectif pédagogique

**Important :** L'objectif principal de ce programme est d'apprendre **FastAPI** et les bonnes pratiques pour créer des APIs ML en production. Ce n'est **pas** un cours de modélisation machine learning.

Le modèle utilisé (classification Iris avec RandomForest) est un **exemple simple** choisi uniquement pour fournir un contexte MLOps réaliste. L'accent est mis sur :
- La maîtrise de FastAPI (routes, validation, dépendances, etc.)
- Les patterns MLOps (gestion de modèles, monitoring, déploiement)
- Les bonnes pratiques de développement d'APIs

Vous pouvez remplacer le modèle Iris par n'importe quel autre modèle ML selon vos besoins.

## Technologies et dépendances

Ce projet utilise les technologies suivantes :

### Framework et serveur
- **FastAPI** (>=0.121.2) : Framework web moderne pour construire des APIs
- **Uvicorn** (>=0.38.0) : Serveur ASGI haute performance

### Validation et configuration
- **Pydantic** (>=2.12.4) : Validation de données avec annotations de type Python
- **Pydantic Settings** : Gestion des variables d'environnement (Module 10)

### Machine Learning (exemple)
- **scikit-learn** (>=1.7.2) : Bibliothèque ML pour le modèle de classification Iris (RandomForest)
- **NumPy** (>=2.3.4) : Calculs numériques et manipulation de tableaux
- **joblib** (>=1.5.2) : Sauvegarde et chargement de modèles ML

### Tests
- **pytest** (>=7.4.0) : Framework de tests
- **pytest-asyncio** : Support asynchrone pour pytest

### Gestion des dépendances
- **uv** : Gestionnaire de paquets Python moderne utilisé dans ce projet
- **pip** : Alternative classique pour l'installation

> **Note :** Ce projet utilise `uv` pour la gestion des dépendances. Les fichiers de configuration `uv/pyproject.toml` et `uv/uv.lock` sont versionnés pour assurer la reproductibilité.

## Structure du programme

Ce programme est divisé en **10 modules progressifs**, chacun avec :
- **Explication théorique** : Concepts détaillés avec exemples
- **Exercice pratique** : Tâche à compléter
- **Correction détaillée** : Solution complète avec explications ligne par ligne
- **Interface Docs** : Explication de l'interface Swagger/ReDoc
- **Prochaines étapes** : Transition vers le module suivant

## Modules

### Module 1 : Fondamentaux FastAPI
**Fichiers :** `modules/MODULE_1_FONDAMENTAUX.md`, `corrections/MODULE_1_CORRECTION.md`

**Concepts :**
- Routes HTTP (GET, POST, PUT, DELETE)
- Path parameters vs Query parameters
- Types de retour
- Décorateurs de routes

**Exercice :** Créer 3 endpoints GET avec différents types de paramètres

---

### Module 2 : Pydantic et validation des données
**Fichiers :** `modules/MODULE_2_PYDANTIC.md`, `corrections/MODULE_2_CORRECTION.md`

**Concepts :**
- BaseModel et validation automatique
- Types optionnels et Union
- Validators personnalisés
- Modèles pour données ML

**Exercice :** Créer des modèles Pydantic pour l'API Iris (features, prédictions, métriques)

---

### Module 3 : Endpoints ML - Prédictions
**Fichiers :** `modules/MODULE_3_ENDPOINTS_ML.md`, `corrections/MODULE_3_CORRECTION.md`

**Concepts :**
- POST pour prédictions ML
- Preprocessing des données
- Format de réponse standardisé
- Gestion des erreurs de base

**Exercice :** Implémenter un endpoint `/predict` pour le modèle Iris

---

### Module 4 : Documentation automatique (Swagger/ReDoc)
**Fichiers :** `modules/MODULE_4_DOCUMENTATION.md`, `corrections/MODULE_4_CORRECTION.md`

**Concepts :**
- Interface `/docs` et `/redoc`
- Tags, descriptions, exemples
- Field() avec descriptions
- Métadonnées de l'API

**Exercice :** Améliorer la documentation avec descriptions, tags, exemples

---

### Module 5 : Dependencies et injection
**Fichiers :** `modules/MODULE_5_DEPENDENCIES.md`, `corrections/MODULE_5_CORRECTION.md`

**Concepts :**
- Depends() et injection de dépendances
- Pattern Singleton pour modèles ML
- Dépendances réutilisables
- Lifecycle management

**Exercice :** Refactoriser le chargement du modèle avec dependencies

---

### Module 6 : Gestion d'erreurs et exceptions
**Fichiers :** `modules/MODULE_6_GESTION_ERREURS.md`, `corrections/MODULE_6_CORRECTION.md`

**Concepts :**
- HTTPException
- Exception handlers personnalisés
- Validation errors
- Messages d'erreur structurés

**Exercice :** Implémenter gestion d'erreurs complète pour prédictions ML

---

### Module 7 : Middleware et logging
**Fichiers :** `modules/MODULE_7_MIDDLEWARE.md`, `corrections/MODULE_7_CORRECTION.md`

**Concepts :**
- Middleware HTTP
- Logging structuré
- Mesure de performance
- Métriques en temps réel

**Exercice :** Ajouter middleware pour logger prédictions et mesurer performances

---

### Module 8 : Endpoints avancés ML
**Fichiers :** `modules/MODULE_8_ENDPOINTS_AVANCES.md`, `corrections/MODULE_8_CORRECTION.md`

**Concepts :**
- Batch predictions
- Health checks avancés
- Métriques du modèle
- Endpoints de diagnostic

**Exercice :** Créer endpoints `/predict/batch`, `/health` amélioré, `/model/info`, `/model/classes`

---

### Module 9 : Tests et validation
**Fichiers :** `modules/MODULE_9_TESTS.md`, `corrections/MODULE_9_CORRECTION.md`

**Concepts :**
- TestClient de FastAPI
- Tests unitaires et d'intégration
- Mock des dépendances
- Fixtures pytest

**Exercice :** Écrire suite de tests complète pour tous les endpoints

---

### Module 10 : Déploiement et production
**Fichiers :** `modules/MODULE_10_DEPLOIEMENT.md`, `corrections/MODULE_10_CORRECTION.md`

**Concepts :**
- Variables d'environnement
- Configuration avec Pydantic Settings
- Docker et containerisation
- Uvicorn/Gunicorn pour production

**Exercice :** Configurer l'application pour le déploiement en production

---

## Comment utiliser ce programme

### 1. Ordre recommandé
On suit les modules dans l'ordre (1 -> 10). Chaque module construit sur les précédents.

### 2. Pour chaque module

1. **On lit l'explication théorique** (`modules/MODULE_X_*.md`)
2. **On fait l'exercice**
3. **Quand on a terminé**,
4. **On lit la correction** (`corrections/MODULE_X_CORRECTION.md`)
5. **On compare** notre solution avec la correction
6. **On teste dans l'interface docs** (`http://localhost:8000/docs`)

### 3. Structure des fichiers

```
cours_fastapi/
├── app/
│   ├── main.py          # Application principale
│   ├── schemas.py       # Modèles Pydantic
│   ├── dependencies.py # Dépendances réutilisables
│   ├── exceptions.py   # Exceptions personnalisées
│   ├── middleware.py   # Middleware (optionnel)
│   └── config.py        # Configuration (Module 10)
├── modules/            # Documentation des modules
│   └── MODULE_*.md     # Fichiers d'explication théorique
├── corrections/        # Corrections des exercices
│   └── MODULE_*_CORRECTION.md  # Fichiers de correction
├── uv/                 # Configuration uv (gestionnaire de paquets)
|   ├── uv\.python-version             
│   ├── pyproject.toml  # Configuration du projet et dépendances
│   └── uv.lock         # Verrouillage des versions (reproductibilité)
└── README_APPRENTISSAGE.md  # Ce fichier
```

## Prérequis

- Python 3.11 ou supérieur
- pip ou uv (gestionnaire de paquets)

## Démarrage rapide

### 1. Installation des dépendances

**Option 1 : Avec uv (recommandé)**

```bash
cd uv
uv sync
```

**Option 2 : Avec pip**

```bash
pip install fastapi>=0.121.2 uvicorn[standard]>=0.38.0 pydantic>=2.12.4 numpy>=2.3.4 scikit-learn>=1.7.2 joblib>=1.5.2 pytest>=7.4.0
```

Ou créez un fichier `requirements.txt` avec le contenu suivant :

```txt
fastapi>=0.121.2
uvicorn[standard]>=0.38.0
pydantic>=2.12.4
pydantic-settings>=2.0.0
numpy>=2.3.4
scikit-learn>=1.7.2
joblib>=1.5.2
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

Puis installez avec :

```bash
pip install -r requirements.txt
```

### 2. Lancer l'application

```bash
# Développement (avec reload)
uvicorn app.main:app --reload

# Ou depuis le dossier uv
cd uv
uv run uvicorn app.main:app --reload
```

### 3. Accéder à la documentation

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **OpenAPI Schema** : http://localhost:8000/openapi.json

## Notes importantes

### Interface Docs (/docs)

L'interface Swagger est **essentielle** pour comprendre FastAPI :
- On teste nos endpoints directement
- On voit les schémas automatiquement générés
- On comprend la validation des données
- On explore les exemples

**On l'utilise régulièrement pendant notre apprentissage !**

### Progression

- **On prend son temps** : Chaque concept est important
- **On pratique** : On fait les exercices avant de regarder la correction
- **On expérimente** : On modifie le code, on teste différentes choses
- **Documentation** : On consulte la doc FastAPI officielle si besoin

## Ressources supplémentaires

- [Documentation FastAPI officielle](https://fastapi.tiangolo.com/)
- [Documentation Pydantic](https://docs.pydantic.dev/)
- [Uvicorn documentation](https://www.uvicorn.org/)

## Checklist de progression

- [ ] Module 1 : Fondamentaux FastAPI
- [ ] Module 2 : Pydantic et validation
- [ ] Module 3 : Endpoints ML
- [ ] Module 4 : Documentation
- [ ] Module 5 : Dependencies
- [ ] Module 6 : Gestion d'erreurs
- [ ] Module 7 : Middleware et logging
- [ ] Module 8 : Endpoints avancés
- [ ] Module 9 : Tests
- [ ] Module 10 : Déploiement

## Félicitations !

Une fois tous les modules complétés, on aura :
- Une API FastAPI complète et production-ready
- Une compréhension approfondie de FastAPI
- Les compétences pour créer des APIs ML robustes
- Les bonnes pratiques pour le MLOps

**Bon apprentissage !**

