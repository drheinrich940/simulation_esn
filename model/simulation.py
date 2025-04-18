#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classe principale de simulation financière pour le modèle SAS France & SARL Sénégal
"""

from config.parameters import DEFAULT_PARAMS
from model.calculation import calculate_quarterly_results, calculate_annual_results
from visualization.plots import (
    plot_evolution_ca_resultats, 
    plot_repartition_benefices,
    plot_analyse_sensibilite,
    plot_evolution_effectifs_couts,
    plot_comparaison_scenarios,
    plot_point_mort_roi
)

class SimulationFinanciere:
    """
    Classe permettant de simuler les résultats financiers d'un modèle SAS France / SARL Sénégal
    sur plusieurs années, en ajustant différents paramètres économiques.
    """
    
    def __init__(self, params=None):
        """
        Initialise la simulation avec les paramètres fournis ou par défaut
        
        Args:
            params (dict): Dictionnaire des paramètres de simulation
        """
        self.params = DEFAULT_PARAMS.copy()
        if params:
            self.params.update(params)
        
        self.resultats = None
        self.resultats_annuels = None
    
    def run_simulation(self):
        """
        Exécute la simulation financière complète
        
        Returns:
            pandas.DataFrame: DataFrame contenant les résultats trimestriels
        """
        # Calcul des résultats trimestriels
        self.resultats = calculate_quarterly_results(self.params)
        
        # Calcul des résultats annuels
        self.resultats_annuels = calculate_annual_results(self.resultats)
        
        return self.resultats
    
    def plot_evolution_ca_resultats(self, nom_fichier=None):
        """Visualise l'évolution trimestrielle du CA et des résultats"""
        if self.resultats is None:
            self.run_simulation()
        
        plot_evolution_ca_resultats(self.resultats, self.params, nom_fichier)
    
    def plot_repartition_benefices(self, nom_fichier=None):
        """Visualise la répartition des bénéfices entre SAS et SARL"""
        if self.resultats_annuels is None:
            self.run_simulation()
        
        plot_repartition_benefices(self.resultats_annuels, nom_fichier)
    
    def plot_analyse_sensibilite(self, nom_fichier=None):
        """Réalise une analyse de sensibilité des principaux paramètres"""
        if self.resultats is None:
            self.run_simulation()
        
        plot_analyse_sensibilite(self, nom_fichier)
    
    def plot_evolution_effectifs_couts(self, nom_fichier=None):
        """Visualise l'évolution des effectifs et des coûts moyens"""
        if self.resultats is None:
            self.run_simulation()
        
        plot_evolution_effectifs_couts(self.resultats, self.params, nom_fichier)
    
    def plot_comparaison_scenarios(self, autre_simulation, nom_fichier=None):
        """Compare avec un autre scénario de simulation"""
        if self.resultats_annuels is None:
            self.run_simulation()
        
        if autre_simulation.resultats_annuels is None:
            autre_simulation.run_simulation()
        
        plot_comparaison_scenarios(self, autre_simulation, nom_fichier)
    
    def plot_point_mort_roi(self, nom_fichier=None):
        """Analyse le point mort et le ROI selon différents paramètres"""
        if self.resultats is None:
            self.run_simulation()
        
        plot_point_mort_roi(self, nom_fichier)
    
    def run_all_visualizations(self, autre_simulation=None, prefix=''):
        """
        Exécute toutes les visualisations disponibles
        
        Args:
            autre_simulation (SimulationFinanciere, optional): Une autre simulation pour comparaison
            prefix (str, optional): Préfixe pour les noms de fichiers
        """
        self.plot_evolution_ca_resultats(f"{prefix}evolution_ca_resultats.png" if prefix else None)
        self.plot_repartition_benefices(f"{prefix}repartition_benefices.png" if prefix else None)
        self.plot_analyse_sensibilite(f"{prefix}analyse_sensibilite.png" if prefix else None)
        self.plot_evolution_effectifs_couts(f"{prefix}evolution_effectifs_couts.png" if prefix else None)
        self.plot_point_mort_roi(f"{prefix}point_mort_roi.png" if prefix else None)
        
        if autre_simulation:
            self.plot_comparaison_scenarios(autre_simulation, f"{prefix}comparaison_scenarios.png" if prefix else None)