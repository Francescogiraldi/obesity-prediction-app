import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Ajouter le répertoire parent au path pour les imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(current_dir))

# Imports avec gestion d'erreur
try:
    from utils import (
        load_model, load_data, prepare_input_data, 
        get_obesity_labels, get_obesity_labels_numeric, get_risk_color, validate_inputs,
        calculate_bmi, get_bmi_category
    )
    from advice_engine import AdviceEngine
    from ui_components import (
        create_gauge_chart, create_bmi_indicator, create_prediction_chart,
        display_shap_explanation, create_risk_assessment_card, create_advice_cards,
        create_progress_tracker, display_model_info, create_input_form
    )
except ImportError:
    # Fallback pour les imports avec préfixe src
    from src.utils import (
        load_model, load_data, prepare_input_data, 
        get_obesity_labels, get_obesity_labels_numeric, get_risk_color, validate_inputs,
        calculate_bmi, get_bmi_category
    )
    from src.advice_engine import AdviceEngine
    from src.ui_components import (
        create_gauge_chart, create_bmi_indicator, create_prediction_chart,
        display_shap_explanation, create_risk_assessment_card, create_advice_cards,
        create_progress_tracker, display_model_info, create_input_form
    )

# Configuration de la page
st.set_page_config(
    page_title="Prédiction d'Obésité - IA Santé",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4ECDC4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FF6B6B;
        margin: 1rem 0;
    }
    .advice-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stButton > button {
        background-color: #FF6B6B;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #FF5252;
        transform: translateY(-2px);
        transition: all 0.3s;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Fonction principale de l'application Streamlit."""
    
    # En-tête principal
    st.markdown('<h1 class="main-header">🏥 Prédicteur d\'Obésité IA</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">'
                'Évaluation personnalisée du risque d\'obésité avec recommandations santé</p>', 
                unsafe_allow_html=True)
    
    # Sidebar pour les informations
    with st.sidebar:
        st.markdown("## 📊 Navigation")
        page = st.radio("Choisir une section:", 
                        ["🔍 Prédiction", "📈 Analyse", "💡 Conseils", "ℹ️ À propos"])
        
        st.markdown("---")
        st.markdown("### 🎯 Objectifs")
        st.markdown("""
        - Prédire le risque d'obésité
        - Fournir des conseils personnalisés
        - Analyser les facteurs de risque
        - Promouvoir un mode de vie sain
        """)
    
    # Chargement des ressources
    @st.cache_resource
    def load_resources():
        # Chemin relatif au répertoire parent depuis src/
        model_path = os.path.join(parent_dir, "models", "modele_lgbm.pkl")
        model = load_model(model_path)
        advice_engine = AdviceEngine()
        return model, advice_engine
    
    try:
        model, advice_engine = load_resources()
        
        if model is None:
            st.error("❌ Impossible de charger le modèle. Vérifiez que le fichier 'models/modele_lgbm.pkl' existe.")
            return
        
        # Navigation par pages
        if page == "🔍 Prédiction":
            prediction_page(model, advice_engine)
        elif page == "📈 Analyse":
            analysis_page(model)
        elif page == "💡 Conseils":
            advice_page(advice_engine)
        elif page == "ℹ️ À propos":
            about_page()
            
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement de l'application: {e}")
        st.info("Vérifiez que tous les fichiers nécessaires sont présents dans le répertoire.")

def prediction_page(model, advice_engine):
    """Page principale de prédiction."""
    st.markdown('<h2 class="sub-header">🔍 Évaluation du Risque d\'Obésité</h2>', unsafe_allow_html=True)
    
    # Formulaire de saisie
    user_inputs = create_input_form()
    
    # Bouton de prédiction
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("🔮 Analyser mon profil", use_container_width=True)
    
    if predict_button:
        # Validation des entrées
        is_valid, error_message = validate_inputs(user_inputs)
        
        if not is_valid:
            st.error(f"❌ {error_message}")
            return
        
        # Prédiction
        with st.spinner("🔄 Analyse en cours..."):
            try:
                # Préparer les données
                input_data = prepare_input_data(user_inputs)
                
                # Faire la prédiction
                prediction = model.predict(input_data)[0]
                probabilities = model.predict_proba(input_data)[0]
                
                # Obtenir les labels
                obesity_labels = get_obesity_labels()
                
                # Gérer les prédictions string ou numériques
                if isinstance(prediction, str):
                    predicted_label = obesity_labels.get(prediction, prediction)
                    # Convertir la prédiction string en index pour les couleurs et métriques
                    model_classes = list(model.classes_) if hasattr(model, 'classes_') else []
                    prediction_index = model_classes.index(prediction) if prediction in model_classes else 0
                else:
                    # Prédiction numérique (fallback)
                    numeric_labels = get_obesity_labels_numeric()
                    predicted_label = numeric_labels.get(prediction, f"Classe {prediction}")
                    prediction_index = prediction
                
                risk_color = get_risk_color(prediction_index)
                
                # Calculer l'IMC
                bmi = calculate_bmi(user_inputs['poids_kg'], user_inputs['taille_m'])
                bmi_category = get_bmi_category(bmi)
                
                # Affichage des résultats
                st.success("✅ Analyse terminée!")
                
                # Métriques principales
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        label="🎯 Prédiction",
                        value=predicted_label,
                        delta=f"Confiance: {probabilities[prediction_index]*100:.1f}%"
                    )
                
                with col2:
                    st.metric(
                        label="📊 IMC",
                        value=f"{bmi:.1f} kg/m²",
                        delta=bmi_category
                    )
                
                with col3:
                    risk_level = "Faible" if prediction_index <= 1 else "Modéré" if prediction_index <= 3 else "Élevé"
                    st.metric(
                        label="⚠️ Niveau de risque",
                        value=risk_level,
                        delta=f"Classe {prediction_index}"
                    )
                
                # Graphiques
                col1, col2 = st.columns(2)
                
                with col1:
                    # Graphique IMC
                    bmi_fig = create_bmi_indicator(bmi)
                    st.plotly_chart(bmi_fig, use_container_width=True)
                
                with col2:
                    # Graphique des probabilités - utiliser les labels numériques
                    numeric_labels = get_obesity_labels_numeric()
                    prob_fig = create_prediction_chart(probabilities, numeric_labels)
                    st.plotly_chart(prob_fig, use_container_width=True)
                
                # Facteurs de risque et conseils
                st.markdown("### 📋 Évaluation des facteurs")
                risk_factors = advice_engine.get_risk_factors(user_inputs)
                protective_factors = advice_engine.get_protective_factors(user_inputs)
                create_risk_assessment_card(risk_factors, protective_factors)
                
                # Conseils personnalisés
                st.markdown("### 💡 Recommandations personnalisées")
                advice = advice_engine.get_personalized_advice(prediction_index, user_inputs)
                create_advice_cards(advice)
                
                # Sauvegarde des résultats (optionnel)
                if st.button("💾 Sauvegarder les résultats"):
                    save_results(user_inputs, prediction_index, predicted_label, bmi)
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la prédiction: {e}")
                st.info("Vérifiez vos données et réessayez.")

def analysis_page(model):
    """Page d'analyse des données."""
    st.markdown('<h2 class="sub-header">📈 Analyse des Données</h2>', unsafe_allow_html=True)
    
    # Charger les données d'entraînement si disponibles
    try:
        data_path = os.path.join(parent_dir, "data", "obesite_clean_fr.csv")
        data = load_data(data_path)
        
        if not data.empty:
            st.markdown("### 📊 Statistiques du dataset")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📝 Échantillons", len(data))
            with col2:
                st.metric("📋 Variables", len(data.columns))
            with col3:
                st.metric("👥 Genres", data['genre'].nunique() if 'genre' in data.columns else "N/A")
            with col4:
                st.metric("🎯 Classes", data['obesite_label'].nunique() if 'obesite_label' in data.columns else "N/A")
            
            # Distribution des classes
            if 'obesite_label' in data.columns:
                st.markdown("### 📊 Distribution des classes d'obésité")
                class_dist = data['obesite_label'].value_counts().sort_index()
                
                import plotly.express as px
                fig = px.bar(
                    x=class_dist.index,
                    y=class_dist.values,
                    labels={'x': 'Classe d\'obésité', 'y': 'Nombre d\'échantillons'},
                    title="Répartition des classes dans le dataset"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Affichage d'un échantillon des données
            st.markdown("### 👀 Aperçu des données")
            st.dataframe(data.head(10), use_container_width=True)
            
        else:
            st.warning("⚠️ Aucune donnée disponible pour l'analyse.")
            
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {e}")
    
    # Informations sur le modèle
    display_model_info()

def advice_page(advice_engine):
    """Page dédiée aux conseils généraux."""
    st.markdown('<h2 class="sub-header">💡 Conseils Santé Généraux</h2>', unsafe_allow_html=True)
    
    # Conseils par catégorie
    tab1, tab2, tab3 = st.tabs(["🥗 Nutrition", "🏃‍♂️ Activité Physique", "🌟 Mode de Vie"])
    
    with tab1:
        st.markdown("""
        ### 🥗 Conseils Nutritionnels
        
        **Principes de base:**
        - Consommez 5 portions de fruits et légumes par jour
        - Privilégiez les protéines maigres (poisson, volaille, légumineuses)
        - Choisissez des glucides complexes (céréales complètes)
        - Limitez les aliments transformés et riches en sucres ajoutés
        - Buvez suffisamment d'eau (1.5-2L par jour)
        
        **Répartition idéale d'une assiette:**
        - 50% de légumes
        - 25% de protéines
        - 25% de glucides complexes
        """)
    
    with tab2:
        st.markdown("""
        ### 🏃‍♂️ Recommandations d'Activité Physique
        
        **Objectifs hebdomadaires (OMS):**
        - 150 minutes d'activité modérée OU 75 minutes d'activité intense
        - 2 séances de renforcement musculaire
        - Activités d'équilibre et de flexibilité
        
        **Idées d'activités:**
        - Marche rapide, vélo, natation
        - Montée d'escaliers
        - Jardinage, ménage actif
        - Sports collectifs
        - Yoga, pilates
        """)
    
    with tab3:
        st.markdown("""
        ### 🌟 Mode de Vie Sain
        
        **Sommeil:**
        - 7-9 heures par nuit
        - Horaires réguliers
        - Éviter les écrans avant le coucher
        
        **Gestion du stress:**
        - Techniques de relaxation
        - Méditation, respiration profonde
        - Activités plaisantes
        - Soutien social
        
        **Habitudes quotidiennes:**
        - Repas à heures fixes
        - Limitation du temps d'écran
        - Pauses actives au travail
        """)
    
    # Tracker de progression
    create_progress_tracker()

def about_page():
    """Page d'informations sur l'application."""
    st.markdown('<h2 class="sub-header">ℹ️ À Propos de l\'Application</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 Objectif
    
    Cette application utilise l'intelligence artificielle pour évaluer le risque d'obésité 
    et fournir des recommandations personnalisées de santé.
    
    ### 🤖 Technologie
    
    - **Modèle:** LightGBM avec preprocessing avancé
    - **Explicabilité:** SHAP pour l'interprétation des prédictions
    - **Interface:** Streamlit pour une expérience utilisateur moderne
    - **Monitoring:** MLflow pour le suivi des performances
    
    ### 📊 Données
    
    Le modèle a été entraîné sur un dataset de plus de 20,000 échantillons 
    incluant des informations démographiques, des habitudes alimentaires, 
    et des données de mode de vie.
    
    ### ⚠️ Avertissement Important
    
    **Cette application est à des fins éducatives et de sensibilisation uniquement.**
    
    Elle ne remplace pas:
    - Une consultation médicale professionnelle
    - Un diagnostic médical
    - Un plan de traitement personnalisé
    
    Consultez toujours un professionnel de santé pour des conseils médicaux personnalisés.
    
    ### 👥 Équipe de Développement
    
    Développé avec ❤️ pour promouvoir la santé et le bien-être.
    
    ### 📞 Contact
    
    Pour toute question ou suggestion, n'hésitez pas à nous contacter.
    """)
    
    # Informations techniques
    display_model_info()

def save_results(user_inputs, prediction, predicted_label, bmi):
    """Sauvegarde les résultats de l'analyse (fonctionnalité future)."""
    st.success("💾 Résultats sauvegardés! (Fonctionnalité à venir)")
    st.info("Dans une version future, vous pourrez sauvegarder et suivre vos résultats dans le temps.")

if __name__ == "__main__":
    main()