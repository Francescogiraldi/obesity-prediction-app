# 🏥 Application de Prédiction d'Obésité avec Streamlit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://localhost:8501)

Cette application utilise un modèle LightGBM pour prédire le niveau d'obésité basé sur les habitudes alimentaires et le mode de vie, avec des recommandations personnalisées de santé.

## ✅ État du Projet

**🎉 APPLICATION COMPLÈTE ET FONCTIONNELLE!**

- ✅ Modèle LightGBM entraîné et optimisé
- ✅ Interface Streamlit moderne et responsive
- ✅ Moteur de recommandations personnalisées
- ✅ Explicabilité SHAP intégrée
- ✅ Architecture modulaire et maintenable
- ✅ Configuration et dépendances complètes

## 🚀 Démarrage Rapide

### Prérequis
- Python 3.9+
- pip ou conda

### Installation et Lancement

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'application
streamlit run src/app_obesite.py
```

**🌐 L'application sera accessible à:** http://localhost:8501

## 📁 Structure du Projet (Complète)

```
app_obesite/
├── 📂 src/                     # Code source principal
│   ├── 🎯 app_obesite.py       # Application Streamlit principale
│   ├── 🔧 utils.py             # Fonctions utilitaires
│   ├── 🤖 advice_engine.py     # Moteur de recommandations
│   └── 🎨 ui_components.py     # Composants UI réutilisables
├── 📂 models/                  # Modèles entraînés
│   ├── 🧠 modele_lgbm.pkl      # Modèle LightGBM principal
│   └── 📊 modele_base.pkl      # Modèle de référence
├── 📂 data/                    # Données du projet
│   ├── 📋 obesite_clean_fr.csv # Dataset nettoyé (20K+ échantillons)
│   ├── 🔢 X_train.csv          # Features d'entraînement
│   ├── 🔢 X_test.csv           # Features de test
│   ├── 🎯 y_train.csv          # Labels d'entraînement
│   ├── 🎯 y_test.csv           # Labels de test
│   └── 📄 BDDobesity_level_V2.csv # Dataset original
├── 📂 assets/                  # Ressources statiques
│   ├── 📊 shap_summary.png     # Graphique SHAP standard
│   └── 📈 shap_summary_named.png # Graphique SHAP avec noms
├── 📂 .streamlit/              # Configuration Streamlit
│   └── ⚙️ config.toml          # Thème et paramètres
├── 📂 mlruns/                  # Expériences MLflow
├── 📂 .ipynb_checkpoints/      # Checkpoints Jupyter
├── 📄 requirements.txt         # Dépendances Python
├── 📖 readme.md               # Documentation (ce fichier)
└── 📓 app_obesite.ipynb       # Notebook de développement
```

## 🎯 Fonctionnalités Principales

### 🔮 Prédiction Intelligente
- **Modèle LightGBM** avec pipeline de preprocessing complet
- **Prédiction en temps réel** avec 7 classes d'obésité
- **Calcul automatique de l'IMC** et évaluation du risque
- **Validation des données** d'entrée

### 🎨 Interface Utilisateur Moderne
- **Design responsive** avec thème personnalisé
- **Navigation par onglets** (Prédiction, Analyse, Conseils, À propos)
- **Composants interactifs** (sliders, graphiques, métriques)
- **Visualisations Plotly** interactives

### 🧠 Explicabilité Avancée
- **Intégration SHAP** pour l'interprétation des prédictions
- **Graphiques d'importance** des caractéristiques
- **Explication locale** de chaque prédiction
- **Visualisations intuitives** des facteurs d'influence

### 💡 Recommandations Personnalisées
- **Conseils nutritionnels** adaptés au profil
- **Suggestions d'activité physique** personnalisées
- **Recommandations de mode de vie** ciblées
- **Analyse des facteurs** de risque et protecteurs

## 🏗️ Architecture Technique

### 📦 Modules Principaux

#### `src/app_obesite.py` - Application Principale
- Point d'entrée Streamlit
- Gestion de la navigation multi-pages
- Orchestration des composants
- Interface utilisateur principale

#### `src/utils.py` - Utilitaires
- Chargement et mise en cache des modèles
- Préparation et validation des données
- Calculs d'IMC et métriques santé
- Fonctions de formatage

#### `src/advice_engine.py` - Moteur de Conseils
- Base de données de recommandations
- Logique de personnalisation
- Analyse des facteurs de risque
- Génération de conseils contextuels

#### `src/ui_components.py` - Composants UI
- Graphiques et visualisations
- Formulaires interactifs
- Cartes de métriques
- Composants réutilisables

### 🔄 Flux de Données

1. **📝 Saisie** → Formulaire utilisateur interactif
2. **✅ Validation** → Vérification des données d'entrée
3. **🔧 Preprocessing** → Standardisation et encodage
4. **🤖 Prédiction** → Modèle LightGBM
5. **📊 Explication** → Analyse SHAP
6. **💡 Recommandations** → Conseils personnalisés
7. **📈 Visualisation** → Graphiques interactifs

## 🤖 Modèle et Données

### 📊 Dataset
- **20,759 échantillons** nettoyés et traduits en français
- **17 caractéristiques** (démographiques, alimentaires, mode de vie)
- **7 classes d'obésité** équilibrées avec SMOTE
- **Données de qualité** avec preprocessing complet

### 🧠 Modèle LightGBM
- **Pipeline complet** avec StandardScaler et OneHotEncoder
- **Équilibrage SMOTE** pour les classes minoritaires
- **Optimisation des hyperparamètres** via validation croisée
- **Performance élevée** sur données de test

### 🔍 Caractéristiques Utilisées
- Genre, âge, taille, poids
- Antécédents familiaux
- Habitudes alimentaires (légumes, repas, grignotage)
- Consommation (eau, alcool)
- Activité physique et transport
- Mode de vie (stress, technologie, sommeil)

## 🎮 Guide d'Utilisation

### 1. 🔍 Page Prédiction
- Remplir le formulaire avec vos informations
- Cliquer sur "🔮 Analyser mon profil"
- Consulter les résultats et explications
- Lire les recommandations personnalisées

### 2. 📈 Page Analyse
- Explorer les statistiques du dataset
- Visualiser la distribution des classes
- Comprendre les données d'entraînement

### 3. 💡 Page Conseils
- Consulter les conseils généraux de santé
- Explorer les recommandations par catégorie
- Utiliser le tracker de progression

### 4. ℹ️ Page À Propos
- Comprendre le fonctionnement de l'application
- Consulter les informations techniques
- Lire les avertissements importants

## 🛠️ Développement

### 🔧 Configuration de l'Environnement

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 🚀 Lancement en Mode Développement

```bash
# Avec rechargement automatique
streamlit run src/app_obesite.py --server.runOnSave true

# Avec debug
streamlit run src/app_obesite.py --logger.level debug
```

### 🐳 Docker (Optionnel)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "src/app_obesite.py"]
```

## 📋 Dépendances Principales

```txt
streamlit>=1.28.0           # Framework web
streamlit-extras>=0.3.0     # Composants additionnels
pandas>=2.0.0               # Manipulation de données
numpy>=1.24.0               # Calculs numériques
scikit-learn>=1.3.0         # Machine learning
imbalanced-learn>=0.11.0    # Équilibrage des classes
lightgbm>=4.0.0             # Modèle de gradient boosting
shap>=0.42.0                # Explicabilité
mlflow>=2.7.0               # Tracking des expériences
plotly>=5.15.0              # Visualisations interactives
```

## ⚠️ Avertissements Importants

**🏥 Usage Médical**
- Cette application est à des fins **éducatives uniquement**
- Ne remplace **jamais** un avis médical professionnel
- Consultez un médecin pour tout problème de santé

**📊 Limitations du Modèle**
- Basé sur des données d'entraînement spécifiques
- Peut ne pas couvrir tous les cas individuels
- Utilisez les résultats comme indication générale

## 🤝 Contribution

1. **Fork** le projet
2. **Créer** une branche feature
3. **Développer** et tester
4. **Soumettre** une Pull Request

## 📞 Support

- 🐛 **Issues**: Signaler des bugs ou demander des fonctionnalités
- 📖 **Documentation**: Consulter ce README
- 💬 **Contact**: Équipe de développement

## 📄 Licence

Ce projet est sous licence MIT. Voir `LICENSE` pour plus de détails.

---

**🎉 Félicitations! Votre application de prédiction d'obésité est maintenant complète et fonctionnelle!**

*Développé avec ❤️ pour promouvoir la santé et le bien-être*

