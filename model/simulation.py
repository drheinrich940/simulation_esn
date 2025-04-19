#!/usr/bin/env python3


"""
Main financial simulation class for the SAS France & SARL Senegal model
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
    Class for simulating the financial results of a SAS France / SARL Senegal model
    over multiple years, by adjusting various economic parameters.
    """

    def __init__(self, params=None):
        """
        Initialize the simulation with provided parameters or defaults

        Args:
            params (dict): Dictionary of simulation parameters
        """
        self.params = DEFAULT_PARAMS.copy()
        if params:
            self.params.update(params)

        self.resultats = None
        self.resultats_annuels = None

    def run_simulation(self):
        """
        Run the complete financial simulation

        Returns:
            pandas.DataFrame: DataFrame containing quarterly results
        """

        self.resultats = calculate_quarterly_results(self.params)


        self.resultats_annuels = calculate_annual_results(self.resultats)

        return self.resultats

    def plot_evolution_ca_resultats(self, nom_fichier=None):
        """Visualize the quarterly evolution of revenue and results"""
        if self.resultats is None:
            self.run_simulation()

        plot_evolution_ca_resultats(self.resultats, self.params, nom_fichier)

    def plot_repartition_benefices(self, nom_fichier=None):
        """Visualize the distribution of profits between SAS and SARL"""
        if self.resultats_annuels is None:
            self.run_simulation()

        plot_repartition_benefices(self.resultats_annuels, nom_fichier)

    def plot_analyse_sensibilite(self, nom_fichier=None):
        """Perform a sensitivity analysis of the main parameters"""
        if self.resultats is None:
            self.run_simulation()

        plot_analyse_sensibilite(self, nom_fichier)

    def plot_evolution_effectifs_couts(self, nom_fichier=None):
        """Visualize the evolution of staff numbers and average costs"""
        if self.resultats is None:
            self.run_simulation()

        plot_evolution_effectifs_couts(self.resultats, self.params, nom_fichier)

    def plot_comparaison_scenarios(self, autre_simulation, nom_fichier=None):
        """Compare with another simulation scenario"""
        if self.resultats_annuels is None:
            self.run_simulation()

        if autre_simulation.resultats_annuels is None:
            autre_simulation.run_simulation()

        plot_comparaison_scenarios(self, autre_simulation, nom_fichier)

    def plot_point_mort_roi(self, nom_fichier=None):
        """Analyze the break-even point and ROI according to different parameters"""
        if self.resultats is None:
            self.run_simulation()

        plot_point_mort_roi(self, nom_fichier)

    def run_all_visualizations(self, autre_simulation=None, prefix=''):
        """
        Run all available visualizations

        Args:
            autre_simulation (SimulationFinanciere, optional): Another simulation for comparison
            prefix (str, optional): Prefix for file names
        """
        self.plot_evolution_ca_resultats(f"{prefix}evolution_ca_resultats.png" if prefix else None)
        self.plot_repartition_benefices(f"{prefix}repartition_benefices.png" if prefix else None)
        self.plot_analyse_sensibilite(f"{prefix}analyse_sensibilite.png" if prefix else None)
        self.plot_evolution_effectifs_couts(f"{prefix}evolution_effectifs_couts.png" if prefix else None)
        self.plot_point_mort_roi(f"{prefix}point_mort_roi.png" if prefix else None)

        if autre_simulation:
            self.plot_comparaison_scenarios(autre_simulation, f"{prefix}comparaison_scenarios.png" if prefix else None)