#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fonctions de calcul pour la simulation financière
"""

import pandas as pd
import numpy as np

def calculate_quarterly_results(params):
    """
    Calcule les résultats financiers trimestriels
    
    Args:
        params (dict): Dictionnaire des paramètres de simulation
        
    Returns:
        pandas.DataFrame: DataFrame contenant les résultats trimestriels
    """
    nb_trimestres = params['nb_annees'] * 4
    
    # Création du DataFrame pour les résultats
    colonnes = [
        'Annee', 'Trimestre', 'Nb_Developpeurs', 'Nb_Lead', 'Nb_CDP', 'Nb_RH',
        'CA_SAS', 'Transfert_SARL', 'Cout_Salaires', 'Frais_Fixes',
        'Marge_Securite', 'IS_Senegal', 'Resultat_Net_SARL',
        'IS_France', 'Resultat_Net_SAS', 'Resultat_Net_Consolide',
        'Taux_Marge_Nette', 'Ratio_SAS_SARL'
    ]
    
    resultats = pd.DataFrame(index=range(nb_trimestres), columns=colonnes)
    
    # Calcul pour chaque trimestre
    for t in range(nb_trimestres):
        annee = t // 4 + 1
        trimestre = t % 4 + 1
        
        # Effectifs
        nb_dev = params['effectif_dev_initial'] + t * params['ajout_dev_par_trimestre']
        nb_lead = 1 if t >= (params['trimestre_ajout_support'] - 1) else 0
        nb_cdp = 1 if t >= (params['trimestre_ajout_support'] - 1) else 0
        nb_rh = 1 if t >= (params['trimestre_ajout_support'] - 1) else 0
        
        # Chiffre d'affaires
        ca_mensuel_dev = nb_dev * params['tjm_dev'] * params['jours_facturable_mois'] * params['taux_occupation_dev']
        ca_mensuel_lead = nb_lead * params['tjm_lead'] * params['jours_facturable_mois'] * params['taux_occupation_lead']
        ca_mensuel_cdp = nb_cdp * params['tjm_cdp'] * params['jours_facturable_mois'] * params['taux_occupation_cdp']
        ca_mensuel = ca_mensuel_dev + ca_mensuel_lead + ca_mensuel_cdp
        ca_trimestriel = ca_mensuel * 3
        
        # Coûts salariaux
        cout_mensuel_dev = nb_dev * params['salaire_dev']
        cout_mensuel_lead = nb_lead * params['salaire_lead']
        cout_mensuel_cdp = nb_cdp * params['salaire_cdp']
        cout_mensuel_rh = nb_rh * params['salaire_rh']
        cout_mensuel_salaires = cout_mensuel_dev + cout_mensuel_lead + cout_mensuel_cdp + cout_mensuel_rh
        
        # Charges patronales
        cout_mensuel_charges = cout_mensuel_salaires * params['taux_charges_patronales']
        cout_mensuel_total_salaires = cout_mensuel_salaires + cout_mensuel_charges
        cout_trimestriel_salaires = cout_mensuel_total_salaires * 3
        
        # Frais fixes selon l'année
        frais_fixes_mensuel = params[f'frais_fixes_annee{annee}']
        frais_fixes_trimestriel = frais_fixes_mensuel * 3
        
        # Sous-total des coûts
        sous_total = cout_trimestriel_salaires + frais_fixes_trimestriel
        
        # Marge de sécurité et transfert
        marge_securite = sous_total * params['marge_securite']
        transfert_sarl = sous_total + marge_securite
        
        # Résultat SARL
        resultat_avant_is_sarl = marge_securite
        is_senegal = resultat_avant_is_sarl * params['taux_is_senegal']
        resultat_net_sarl = resultat_avant_is_sarl - is_senegal
        
        # Résultat SAS
        resultat_avant_is_sas = ca_trimestriel - transfert_sarl
        is_france = resultat_avant_is_sas * params['taux_is_france']
        resultat_net_sas = resultat_avant_is_sas - is_france
        
        # Résultat consolidé et ratios
        resultat_net_consolide = resultat_net_sarl + resultat_net_sas
        taux_marge_nette = resultat_net_consolide / ca_trimestriel if ca_trimestriel > 0 else 0
        ratio_sas_sarl = resultat_net_sas / resultat_net_sarl if resultat_net_sarl > 0 else float('inf')
        
        # Stockage des résultats
        resultats.loc[t] = [
            annee, trimestre, nb_dev, nb_lead, nb_cdp, nb_rh,
            ca_trimestriel, transfert_sarl, cout_trimestriel_salaires, frais_fixes_trimestriel,
            marge_securite, is_senegal, resultat_net_sarl,
            is_france, resultat_net_sas, resultat_net_consolide,
            taux_marge_nette, ratio_sas_sarl
        ]
    
    return resultats

def calculate_annual_results(resultats_trimestriels):
    """
    Calcule les résultats annuels à partir des résultats trimestriels
    
    Args:
        resultats_trimestriels (pandas.DataFrame): DataFrame des résultats trimestriels
        
    Returns:
        pandas.DataFrame: DataFrame des résultats annuels
    """
    resultats_annuels = resultats_trimestriels.groupby('Annee').agg({
        'Nb_Developpeurs': 'last',
        'CA_SAS': 'sum',
        'Transfert_SARL': 'sum',
        'Resultat_Net_SARL': 'sum',
        'Resultat_Net_SAS': 'sum',
        'Resultat_Net_Consolide': 'sum'
    })
    
    # Calcul des ratios annuels
    resultats_annuels['Taux_Marge_Nette'] = resultats_annuels['Resultat_Net_Consolide'] / resultats_annuels['CA_SAS']
    resultats_annuels['Part_SARL'] = resultats_annuels['Resultat_Net_SARL'] / resultats_annuels['Resultat_Net_Consolide']
    resultats_annuels['Part_SAS'] = resultats_annuels['Resultat_Net_SAS'] / resultats_annuels['Resultat_Net_Consolide']
    resultats_annuels['Ratio_SAS_SARL'] = resultats_annuels['Resultat_Net_SAS'] / resultats_annuels['Resultat_Net_SARL']
    
    return resultats_annuels