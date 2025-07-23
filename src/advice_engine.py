import pandas as pd
from typing import Dict, List, Any
import streamlit as st

class AdviceEngine:
    """Moteur de recommandations personnalisées pour la santé."""
    
    def __init__(self):
        self.advice_database = self._initialize_advice_database()
    
    def _initialize_advice_database(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialise la base de données des conseils."""
        return {
            "nutrition": {
                "insuffisance_ponderale": [
                    "🥗 Augmentez votre apport calorique avec des aliments nutritifs",
                    "🥜 Consommez plus de protéines (viandes maigres, légumineuses, noix)",
                    "🍌 Ajoutez des collations saines entre les repas",
                    "🥛 Buvez des smoothies riches en calories et nutriments"
                ],
                "poids_normal": [
                    "🥬 Maintenez une alimentation équilibrée et variée",
                    "🍎 Consommez 5 portions de fruits et légumes par jour",
                    "🐟 Privilégiez les protéines maigres et les poissons gras",
                    "💧 Buvez suffisamment d'eau (1.5-2L par jour)"
                ],
                "surpoids": [
                    "🥗 Réduisez les portions et privilégiez les légumes",
                    "🚫 Limitez les aliments transformés et sucrés",
                    "🍽️ Mangez lentement et écoutez votre satiété",
                    "🥤 Remplacez les boissons sucrées par de l'eau"
                ],
                "obesite": [
                    "👨‍⚕️ Consultez un nutritionniste pour un plan personnalisé",
                    "📊 Tenez un journal alimentaire pour identifier les habitudes",
                    "🥬 Remplissez la moitié de votre assiette avec des légumes",
                    "⏰ Respectez des horaires de repas réguliers"
                ]
            },
            "activite_physique": {
                "insuffisance_ponderale": [
                    "💪 Privilégiez la musculation pour développer la masse musculaire",
                    "🏃‍♂️ Commencez par 20-30 minutes d'exercice modéré",
                    "🧘‍♀️ Intégrez des exercices de renforcement et d'étirement"
                ],
                "poids_normal": [
                    "🏃‍♂️ Maintenez 150 minutes d'activité modérée par semaine",
                    "💪 Ajoutez 2 séances de renforcement musculaire",
                    "🚶‍♀️ Intégrez plus de marche dans votre quotidien"
                ],
                "surpoids": [
                    "🏃‍♂️ Augmentez progressivement votre activité physique",
                    "🚴‍♀️ Privilégiez les activités cardio (vélo, natation, marche)",
                    "⏰ Visez 45-60 minutes d'exercice 5 fois par semaine"
                ],
                "obesite": [
                    "👨‍⚕️ Consultez un médecin avant de commencer un programme",
                    "🚶‍♀️ Commencez par la marche quotidienne (10-15 minutes)",
                    "🏊‍♀️ Privilégiez les activités à faible impact (natation, aquagym)"
                ]
            },
            "mode_de_vie": {
                "general": [
                    "😴 Dormez 7-9 heures par nuit pour réguler les hormones",
                    "🧘‍♀️ Pratiquez la gestion du stress (méditation, yoga)",
                    "📱 Limitez le temps d'écran, surtout avant le coucher",
                    "👥 Entourez-vous de soutien social pour vos objectifs santé"
                ]
            }
        }
    
    def get_personalized_advice(self, prediction: int, user_inputs: Dict[str, Any]) -> Dict[str, List[str]]:
        """Génère des conseils personnalisés basés sur la prédiction et les inputs utilisateur."""
        # Déterminer la catégorie de poids
        weight_category = self._get_weight_category(prediction)
        
        advice = {
            "nutrition": self.advice_database["nutrition"].get(weight_category, []),
            "activite_physique": self.advice_database["activite_physique"].get(weight_category, []),
            "mode_de_vie": self.advice_database["mode_de_vie"]["general"]
        }
        
        # Ajouter des conseils spécifiques basés sur les inputs
        advice = self._add_specific_advice(advice, user_inputs, weight_category)
        
        return advice
    
    def _get_weight_category(self, prediction: int) -> str:
        """Convertit la prédiction en catégorie de poids."""
        if prediction == 0:
            return "insuffisance_ponderale"
        elif prediction == 1:
            return "poids_normal"
        elif prediction in [2, 3]:
            return "surpoids"
        else:
            return "obesite"
    
    def _add_specific_advice(self, advice: Dict[str, List[str]], 
                           user_inputs: Dict[str, Any], 
                           weight_category: str) -> Dict[str, List[str]]:
        """Ajoute des conseils spécifiques basés sur les habitudes de l'utilisateur."""
        
        # Conseils basés sur la consommation de légumes
        if user_inputs.get('consommation_legumes', 0) < 2:
            advice["nutrition"].append("🥕 Augmentez votre consommation de légumes à chaque repas")
        
        # Conseils basés sur l'activité physique
        if user_inputs.get('frequence_activite_physique', 0) < 2:
            advice["activite_physique"].append("🏃‍♂️ Augmentez progressivement votre activité physique")
        
        # Conseils basés sur la consommation d'eau
        if user_inputs.get('consommation_eau', 0) < 2:
            advice["mode_de_vie"].append("💧 Buvez plus d'eau tout au long de la journée")
        
        # Conseils basés sur le grignotage
        if user_inputs.get('grignotage') == 'Toujours':
            advice["nutrition"].append("🚫 Remplacez le grignotage par des collations saines (fruits, noix)")
        
        # Conseils basés sur le stress
        if user_inputs.get('stress', 0) > 2:
            advice["mode_de_vie"].append("🧘‍♀️ Pratiquez des techniques de relaxation pour gérer le stress")
        
        # Conseils basés sur le temps passé sur la technologie
        if user_inputs.get('temps_technologie', 0) > 2:
            advice["mode_de_vie"].append("📱 Réduisez le temps d'écran et augmentez l'activité physique")
        
        # Conseils basés sur le transport
        if user_inputs.get('transport') in ['Automobile', 'Transport_Public']:
            advice["activite_physique"].append("🚶‍♀️ Intégrez plus de marche ou de vélo dans vos déplacements")
        
        return advice
    
    def get_risk_factors(self, user_inputs: Dict[str, Any]) -> List[str]:
        """Identifie les facteurs de risque principaux."""
        risk_factors = []
        
        # IMC
        bmi = user_inputs['poids_kg'] / (user_inputs['taille_m'] ** 2)
        if bmi >= 30:
            risk_factors.append("IMC élevé (≥30)")
        elif bmi >= 25:
            risk_factors.append("Surpoids (IMC 25-30)")
        
        # Antécédents familiaux
        if user_inputs.get('antecedents_familiaux') == 'Oui':
            risk_factors.append("Antécédents familiaux d'obésité")
        
        # Mode de vie sédentaire
        if user_inputs.get('frequence_activite_physique', 0) < 1:
            risk_factors.append("Mode de vie sédentaire")
        
        # Mauvaises habitudes alimentaires
        if user_inputs.get('grignotage') == 'Toujours':
            risk_factors.append("Grignotage fréquent")
        
        if user_inputs.get('consommation_legumes', 0) < 1:
            risk_factors.append("Faible consommation de légumes")
        
        # Stress élevé
        if user_inputs.get('stress', 0) > 2:
            risk_factors.append("Niveau de stress élevé")
        
        return risk_factors
    
    def get_protective_factors(self, user_inputs: Dict[str, Any]) -> List[str]:
        """Identifie les facteurs protecteurs."""
        protective_factors = []
        
        # Activité physique régulière
        if user_inputs.get('frequence_activite_physique', 0) >= 3:
            protective_factors.append("Activité physique régulière")
        
        # Bonne alimentation
        if user_inputs.get('consommation_legumes', 0) >= 3:
            protective_factors.append("Consommation élevée de légumes")
        
        if user_inputs.get('consommation_eau', 0) >= 2:
            protective_factors.append("Hydratation adéquate")
        
        # Surveillance du poids
        if user_inputs.get('surveillance_calories') == 'Oui':
            protective_factors.append("Surveillance des calories")
        
        # Non-fumeur
        if user_inputs.get('fumeur') == 'Non':
            protective_factors.append("Non-fumeur")
        
        # Transport actif
        if user_inputs.get('transport') in ['Marche', 'Vélo']:
            protective_factors.append("Transport actif")
        
        return protective_factors