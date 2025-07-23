import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import shap
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64

def create_gauge_chart(value: float, title: str, color: str) -> go.Figure:
    """Crée un graphique en jauge pour afficher une métrique."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 25], 'color': "lightgray"},
                {'range': [25, 50], 'color': "gray"},
                {'range': [50, 75], 'color': "lightblue"},
                {'range': [75, 100], 'color': "blue"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_bmi_indicator(bmi: float) -> go.Figure:
    """Crée un indicateur visuel pour l'IMC."""
    # Déterminer la couleur basée sur l'IMC
    if bmi < 18.5:
        color = "#4CAF50"
        category = "Insuffisance pondérale"
    elif bmi < 25:
        color = "#8BC34A"
        category = "Poids normal"
    elif bmi < 30:
        color = "#FFC107"
        category = "Surpoids"
    else:
        color = "#F44336"
        category = "Obésité"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = bmi,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"IMC: {category}", 'font': {'size': 18}},
        number = {'suffix': " kg/m²", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [15, 40], 'tickwidth': 1},
            'bar': {'color': color, 'thickness': 0.3},
            'steps': [
                {'range': [15, 18.5], 'color': "#E3F2FD"},
                {'range': [18.5, 25], 'color': "#C8E6C9"},
                {'range': [25, 30], 'color': "#FFF3E0"},
                {'range': [30, 40], 'color': "#FFEBEE"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': bmi
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_prediction_chart(probabilities: np.ndarray, labels: Dict[int, str]) -> go.Figure:
    """Crée un graphique en barres pour les probabilités de prédiction."""
    df = pd.DataFrame({
        'Catégorie': [labels[i] for i in range(len(probabilities))],
        'Probabilité': probabilities * 100
    })
    
    # Trier par probabilité décroissante
    df = df.sort_values('Probabilité', ascending=True)
    
    # Couleurs dégradées
    colors = px.colors.sequential.Reds_r
    
    fig = go.Figure(data=[
        go.Bar(
            y=df['Catégorie'],
            x=df['Probabilité'],
            orientation='h',
            marker=dict(
                color=df['Probabilité'],
                colorscale='RdYlGn_r',
                showscale=False
            ),
            text=[f"{p:.1f}%" for p in df['Probabilité']],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Probabilités de classification",
        xaxis_title="Probabilité (%)",
        yaxis_title="Catégorie d'obésité",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def display_shap_explanation(model, input_data: pd.DataFrame, feature_names: List[str]):
    """Affiche l'explication SHAP pour la prédiction."""
    try:
        # Créer l'explainer SHAP
        explainer = shap.Explainer(model)
        shap_values = explainer(input_data)
        
        # Créer le graphique SHAP
        fig, ax = plt.subplots(figsize=(10, 6))
        shap.plots.waterfall(shap_values[0], max_display=10, show=False)
        
        # Convertir en image pour Streamlit
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        buf.seek(0)
        
        st.image(buf, caption="Explication SHAP - Impact des caractéristiques sur la prédiction")
        plt.close()
        
    except Exception as e:
        st.warning(f"Impossible d'afficher l'explication SHAP: {e}")
        # Afficher l'image SHAP pré-générée si disponible
        try:
            shap_image = Image.open("assets/shap_summary_named.png")
            st.image(shap_image, caption="Importance des caractéristiques (SHAP)")
        except:
            st.info("Explication SHAP non disponible")

def create_risk_assessment_card(risk_factors: List[str], protective_factors: List[str]):
    """Crée une carte d'évaluation des risques."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚨 Facteurs de risque")
        if risk_factors:
            for factor in risk_factors:
                st.markdown(f"• {factor}")
        else:
            st.markdown("✅ Aucun facteur de risque majeur identifié")
    
    with col2:
        st.markdown("### 🛡️ Facteurs protecteurs")
        if protective_factors:
            for factor in protective_factors:
                st.markdown(f"• {factor}")
        else:
            st.markdown("⚠️ Peu de facteurs protecteurs identifiés")

def create_advice_cards(advice: Dict[str, List[str]]):
    """Crée des cartes de conseils organisées par catégorie."""
    tabs = st.tabs(["🥗 Nutrition", "🏃‍♂️ Activité Physique", "🌟 Mode de Vie"])
    
    categories = ["nutrition", "activite_physique", "mode_de_vie"]
    
    for i, (tab, category) in enumerate(zip(tabs, categories)):
        with tab:
            if category in advice and advice[category]:
                for tip in advice[category]:
                    st.markdown(f"**{tip}**")
                    st.markdown("---")
            else:
                st.info("Aucun conseil spécifique pour cette catégorie")

def create_progress_tracker():
    """Crée un tracker de progression (placeholder pour futures fonctionnalités)."""
    st.markdown("### 📈 Suivi de progression")
    st.info("Fonctionnalité de suivi à venir - enregistrez vos mesures régulièrement!")
    
    # Placeholder pour un graphique de progression
    dates = pd.date_range('2024-01-01', periods=10, freq='W')
    weights = np.random.normal(70, 2, 10)  # Données d'exemple
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=weights,
        mode='lines+markers',
        name='Poids (kg)',
        line=dict(color='#FF6B6B', width=3)
    ))
    
    fig.update_layout(
        title="Évolution du poids (exemple)",
        xaxis_title="Date",
        yaxis_title="Poids (kg)",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_model_info():
    """Affiche les informations sur le modèle."""
    with st.expander("ℹ️ À propos du modèle"):
        st.markdown("""
        **Modèle utilisé:** LightGBM avec pipeline de préprocessing
        
        **Caractéristiques du modèle:**
        - Algorithme: LightGBM (Gradient Boosting)
        - Préprocessing: StandardScaler + OneHotEncoder
        - Équilibrage: SMOTE pour gérer les classes déséquilibrées
        - Explicabilité: Intégration SHAP pour l'interprétation
        
        **Performance:**
        - Entraîné sur un dataset de 20,000+ échantillons
        - Validation croisée stratifiée
        - Métriques d'évaluation disponibles via MLflow
        
        **Avertissement:**
        Cette application est à des fins éducatives et ne remplace pas un avis médical professionnel.
        """)

def create_input_form() -> Dict[str, Any]:
    """Crée le formulaire de saisie des données utilisateur."""
    st.markdown("### 📝 Vos informations")
    
    # Informations de base
    col1, col2 = st.columns(2)
    
    with col1:
        genre = st.selectbox("Genre", ["Femme", "Homme"])
        age = st.number_input("Âge", min_value=10, max_value=100, value=30)
        taille_m = st.number_input("Taille (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01)
        poids_kg = st.number_input("Poids (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
    
    with col2:
        antecedents_familiaux = st.selectbox("Antécédents familiaux d'obésité", ["Non", "Oui"])
        fumeur = st.selectbox("Fumeur", ["Non", "Oui"])
        surveillance_calories = st.selectbox("Surveillez-vous vos calories?", ["Non", "Oui"])
    
    # Habitudes alimentaires
    st.markdown("#### 🍽️ Habitudes alimentaires")
    col3, col4 = st.columns(2)
    
    with col3:
        consommation_legumes = st.slider("Consommation de légumes (portions/jour)", 0, 5, 2)
        nombre_repas_principaux = st.slider("Nombre de repas principaux/jour", 1, 5, 3)
        consommation_eau = st.slider("Consommation d'eau (L/jour)", 0, 5, 2)
    
    with col4:
        grignotage = st.selectbox("Fréquence de grignotage", ["Jamais", "Parfois", "Souvent", "Toujours"])
        alcool = st.selectbox("Consommation d'alcool", ["Jamais", "Parfois", "Souvent", "Toujours"])
    
    # Mode de vie
    st.markdown("#### 🏃‍♂️ Mode de vie")
    col5, col6 = st.columns(2)
    
    with col5:
        frequence_activite_physique = st.slider("Fréquence d'activité physique (jours/semaine)", 0, 7, 2)
        temps_technologie = st.slider("Temps passé sur la technologie (heures/jour)", 0, 12, 4)
    
    with col6:
        transport = st.selectbox("Mode de transport principal", 
                                ["Marche", "Vélo", "Transport_Public", "Automobile"])
    
    return {
        'genre': genre,
        'age': age,
        'taille_m': taille_m,
        'poids_kg': poids_kg,
        'antecedents_familiaux': antecedents_familiaux,
        'consommation_legumes': consommation_legumes,
        'nombre_repas_principaux': nombre_repas_principaux,
        'grignotage': grignotage,
        'fumeur': fumeur,
        'consommation_eau': consommation_eau,
        'surveillance_calories': surveillance_calories,
        'frequence_activite_physique': frequence_activite_physique,
        'temps_technologie': temps_technologie,
        'alcool': alcool,
        'transport': transport
    }