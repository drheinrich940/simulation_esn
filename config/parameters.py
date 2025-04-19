#!/usr/bin/env python3


"""
Configuration and default parameters for the simulation
"""


DEFAULT_PARAMS = {

    'nb_annees': 3,
    'taux_is_france': 0.25,
    'taux_is_senegal': 0.30,
    'taux_charges_patronales': 0.12,
    'marge_securite': 0.10,


    'tjm_dev': 300,
    'tjm_lead': 400,
    'tjm_cdp': 350,
    'taux_occupation_dev': 0.80,
    'taux_occupation_lead': 1.00,
    'taux_occupation_cdp': 1.00,
    'jours_facturable_mois': 20,


    'salaire_dev': 1000,
    'salaire_lead': 1500,
    'salaire_cdp': 1000,
    'salaire_rh': 700,


    'effectif_dev_initial': 4,
    'ajout_dev_par_trimestre': 2,
    'trimestre_ajout_support': 5,


    'frais_fixes_annee1': 1000,
    'frais_fixes_annee2': 1500,
    'frais_fixes_annee3': 2000,
}