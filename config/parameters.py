#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration et paramètres par défaut pour la simulation
"""

# Paramètres par défaut du modèle
DEFAULT_PARAMS = {
    # Paramètres généraux
    'nb_annees': 3,                   # Nombre d'années de simulation
    'taux_is_france': 0.25,           # Taux d'imposition en France
    'taux_is_senegal': 0.30,          # Taux d'imposition au Sénégal
    'taux_charges_patronales': 0.12,  # Taux de charges patronales au Sénégal
    'marge_securite': 0.10,           # Marge de sécurité pour la SARL (%)
    
    # Paramètres de facturation
    'tjm_dev': 300,                   # Tarif journalier développeur (€)
    'tjm_lead': 400,                  # Tarif journalier lead technique (€)
    'tjm_cdp': 350,                   # Tarif journalier chef de projet (€)
    'taux_occupation_dev': 0.80,      # Taux d'occupation des développeurs (%)
    'taux_occupation_lead': 1.00,     # Taux d'occupation du lead (%)
    'taux_occupation_cdp': 1.00,      # Taux d'occupation du chef de projet (%)
    'jours_facturable_mois': 20,      # Nombre de jours facturables par mois
    
    # Paramètres de salaires
    'salaire_dev': 1000,              # Salaire mensuel développeur (€)
    'salaire_lead': 1500,             # Salaire mensuel lead technique (€)
    'salaire_cdp': 1000,              # Salaire mensuel chef de projet (€)
    'salaire_rh': 700,                # Salaire mensuel RH (€)
    
    # Paramètres d'évolution des effectifs
    'effectif_dev_initial': 4,        # Nombre initial de développeurs
    'ajout_dev_par_trimestre': 2,     # Ajout de développeurs par trimestre
    'trimestre_ajout_support': 5,     # Trimestre d'ajout des postes support
    
    # Paramètres de frais fixes
    'frais_fixes_annee1': 1000,       # Frais fixes mensuels année 1 (€)
    'frais_fixes_annee2': 1500,       # Frais fixes mensuels année 2 (€)
    'frais_fixes_annee3': 2000,       # Frais fixes mensuels année 3 (€)
}