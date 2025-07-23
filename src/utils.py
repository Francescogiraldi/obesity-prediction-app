import pickle
import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, Any, Tuple
import os
import joblib

@st.cache_resource
def load_model(model_path: str):
    """Charge le modèle LightGBM avec mise en cache."""
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Erreur lors du chargement du modèle: {e}")
        return None

@st.cache_data
def load_data(data_path: str) -> pd.DataFrame:
    """Charge les données avec mise en cache."""
    try:
        return pd.read_csv(data_path)
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return pd.DataFrame()

def calculate_bmi(weight: float, height: float) -> float:
    """Calcule l'IMC (Indice de Masse Corporelle)."""
    if height <= 0:
        return 0
    return weight / (height ** 2)

def get_bmi_category(bmi: float) -> str:
    """Retourne la catégorie d'IMC."""
    if bmi < 18.5:
        return "Insuffisance pondérale"
    elif bmi < 25:
        return "Poids normal"
    elif bmi < 30:
        return "Surpoids"
    else:
        return "Obésité"

def prepare_input_data(user_inputs: Dict[str, Any]) -> pd.DataFrame:
    """Prépare les données d'entrée pour la prédiction."""
    # Convertir les valeurs catégorielles en valeurs numériques pour les colonnes qui l'exigent
    def convert_yes_no_to_numeric(value):
        if isinstance(value, str):
            return 1 if value.lower() in ['oui', 'yes', 'true'] else 0
        return int(bool(value))
    
    # Créer un DataFrame avec les colonnes attendues par le modèle
    data = pd.DataFrame({
        'identifiant': [0],  # Valeur par défaut
        'age': [user_inputs['age']],
        'taille_m': [user_inputs['taille_m']],
        'poids_kg': [user_inputs['poids_kg']],
        'antecedents_surpoids_famille': [convert_yes_no_to_numeric(user_inputs['antecedents_familiaux'])],
        'consommation_frequent_calorique': [1 if user_inputs['consommation_legumes'] >= 3 else 0],
        'frequence_legumes': [user_inputs['consommation_legumes']],
        'nombre_repas_jour': [user_inputs['nombre_repas_principaux']],
        'fumeur': [convert_yes_no_to_numeric(user_inputs['fumeur'])],
        'eau_litres_jour': [user_inputs['consommation_eau']],
        'suivi_calories': [convert_yes_no_to_numeric(user_inputs['surveillance_calories'])],
        'activite_physique_hebdo': [user_inputs['frequence_activite_physique']],
        'temps_ecran': [user_inputs['temps_technologie']],
        # Colonnes catégorielles (gardées comme strings pour OneHotEncoder)
        'genre': [user_inputs['genre']],
        'grignotage': [user_inputs['grignotage']],
        'alcool': [user_inputs['alcool']],
        'transport': [user_inputs['transport']]
    })
    
    return data

def get_obesity_labels() -> Dict[str, str]:
    """Retourne le mapping des labels d'obésité du modèle vers les labels d'affichage."""
    return {
        "Insuffisance_Ponderale": "Insuffisance pondérale",
        "Poids_Normal": "Poids normal",
        "Surpoids_Niveau_I": "Surpoids niveau I",
        "Surpoids_Niveau_II": "Surpoids niveau II",
        "Obesite_Type_I": "Obésité type I",
        "Obesite_Type_II": "Obésité type II",
        "Obesite_Type_III": "Obésité type III"
    }

def get_obesity_labels_numeric() -> Dict[int, str]:
    """Retourne le mapping numérique des labels d'obésité pour la compatibilité."""
    return {
        0: "Insuffisance pondérale",
        1: "Poids normal",
        2: "Surpoids niveau I",
        3: "Surpoids niveau II",
        4: "Obésité type I",
        5: "Obésité type II",
        6: "Obésité type III"
    }

def get_risk_color(prediction: int) -> str:
    """Retourne la couleur associée au niveau de risque."""
    colors = {
        0: "#4CAF50",  # Vert
        1: "#8BC34A",  # Vert clair
        2: "#FFC107",  # Jaune
        3: "#FF9800",  # Orange
        4: "#FF5722",  # Rouge-orange
        5: "#F44336",  # Rouge
        6: "#9C27B0"   # Violet
    }
    return colors.get(prediction, "#757575")

def format_percentage(value: float) -> str:
    """Formate un pourcentage avec 1 décimale."""
    return f"{value:.1f}%"

def validate_inputs(inputs: Dict[str, Any]) -> Tuple[bool, str]:
    """Valide les entrées utilisateur."""
    if inputs['age'] < 10 or inputs['age'] > 100:
        return False, "L'âge doit être entre 10 et 100 ans"
    
    if inputs['taille_m'] < 1.0 or inputs['taille_m'] > 2.5:
        return False, "La taille doit être entre 1.0 et 2.5 mètres"
    
    if inputs['poids_kg'] < 30 or inputs['poids_kg'] > 300:
        return False, "Le poids doit être entre 30 et 300 kg"
    
    return True, ""

def get_feature_names() -> list:
    """Retourne les noms des features en français pour SHAP."""
    return [
        'Genre', 'Âge', 'Taille (m)', 'Poids (kg)', 'Antécédents familiaux',
        'Consommation légumes', 'Nombre repas principaux', 'Grignotage',
        'Fumeur', 'Consommation eau', 'Surveillance calories',
        'Fréquence activité physique', 'Temps technologie', 'Alcool',
        'Transport', 'Stress', 'IMC'
    ]