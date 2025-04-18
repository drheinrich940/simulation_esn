#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fonctions de visualisation adaptées pour Streamlit
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
from utils.formatting import euro_formatter, percent_formatter, setup_style

def streamlit_evolution_ca_resultats(simulation):
    """
    Visualise l'évolution trimestrielle du CA et des résultats pour Streamlit

    Args:
        simulation (SimulationFinanciere): Instance de simulation
    """
    if simulation.resultats is None:
        simulation.run_simulation()

    resultats = simulation.resultats
    params = simulation.params

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = setup_style()

    # Tracé des lignes
    ax.plot(resultats.index + 1, resultats['CA_SAS'],
            marker='o', label='Chiffre d\'affaires', color=colors[0], linewidth=2)
    ax.plot(resultats.index + 1, resultats['Transfert_SARL'],
            marker='s', label='Transfert vers SARL', color=colors[2], linewidth=2)
    ax.plot(resultats.index + 1, resultats['Resultat_Net_Consolide'],
            marker='^', label='Résultat net consolidé', color=colors[4], linewidth=2)

    # Barres pour le nombre de développeurs
    ax2 = ax.twinx()
    ax2.bar(resultats.index + 1, resultats['Nb_Developpeurs'],
            alpha=0.2, color=colors[8], label='Nb de développeurs')
    ax2.set_ylabel('Nombre de développeurs', color=colors[8])
    ax2.tick_params(axis='y', labelcolor=colors[8])

    # Configuration
    ax.set_xlabel('Trimestre')
    ax.set_ylabel('Montant (€)')
    ax.yaxis.set_major_formatter(euro_formatter)
    ax.set_xticks(resultats.index + 1)
    ax.set_xticklabels([f"T{i+1}" for i in resultats.index])

    # Lignes de séparation des années
    for year in range(1, params['nb_annees']):
        ax.axvline(x=year*4 + 0.5, color='gray', linestyle='--', alpha=0.5)
        ax.text(year*4 + 0.5, ax.get_ylim()[1]*0.95, f'Année {year+1}',
               rotation=90, verticalalignment='top', alpha=0.7)

    # Légende
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.title('Évolution trimestrielle du CA, des transferts et des résultats')
    plt.tight_layout()

    return fig

def streamlit_repartition_benefices(simulation):
    """
    Visualise la répartition des bénéfices entre SAS et SARL pour Streamlit

    Args:
        simulation (SimulationFinanciere): Instance de simulation
    """
    if simulation.resultats_annuels is None:
        simulation.run_simulation()

    resultats_annuels = simulation.resultats_annuels

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    colors = setup_style()

    # Répartition en pourcentage
    resultats_annuels[['Part_SAS', 'Part_SARL']].plot(
        kind='bar', stacked=True, ax=ax1, color=[colors[1], colors[5]])

    ax1.set_title('Répartition des bénéfices (en %)')
    ax1.set_xlabel('Année')
    ax1.set_ylabel('Part du résultat consolidé')
    ax1.set_ylim(0, 1)
    ax1.set_yticks(np.arange(0, 1.1, 0.1))
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0%}'))

    # Valeurs sur les barres
    for i, row in enumerate(resultats_annuels.iterrows()):
        ax1.text(i, 0.5, f"{row[1]['Part_SAS']:.1%}", ha='center', color='white', fontweight='bold')
        ax1.text(i, 0.95, f"{row[1]['Part_SARL']:.1%}", ha='center', color='white', fontweight='bold')

    # Ratio SAS/SARL
    bar_plot = ax2.bar(resultats_annuels.index, resultats_annuels['Ratio_SAS_SARL'], color=colors[3])
    ax2.set_title('Ratio SAS/SARL (déséquilibre fiscal)')
    ax2.set_xlabel('Année')
    ax2.set_ylabel('Ratio')

    # Zone de risque fiscal
    ax2.axhspan(15, ax2.get_ylim()[1], color='red', alpha=0.2, label='Zone à risque fiscal')

    # Valeurs sur les barres
    for bar in bar_plot:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
               f'{height:.1f}', ha='center', va='bottom')

    ax2.legend()
    plt.tight_layout()

    return fig

def streamlit_comparaison_scenarios(simulation1, simulation2):
    """
    Compare deux scénarios de simulation pour Streamlit

    Args:
        simulation1 (SimulationFinanciere): Premier scénario
        simulation2 (SimulationFinanciere): Second scénario
    """
    if simulation1.resultats_annuels is None:
        simulation1.run_simulation()

    if simulation2.resultats_annuels is None:
        simulation2.run_simulation()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    colors = setup_style()

    # Résultats nets consolidés par année
    x = np.arange(len(simulation1.resultats_annuels))
    width = 0.35

    rects1 = ax1.bar(x - width/2, simulation1.resultats_annuels['Resultat_Net_Consolide'],
                    width, label='Scénario 1', color=colors[0])
    rects2 = ax1.bar(x + width/2, simulation2.resultats_annuels['Resultat_Net_Consolide'],
                    width, label='Scénario 2', color=colors[4])

    ax1.set_title('Résultat net consolidé par année')
    ax1.set_xlabel('Année')
    ax1.set_ylabel('Résultat net (€)')
    ax1.set_xticks(x)
    ax1.yaxis.set_major_formatter(euro_formatter)
    ax1.legend()

    # Ajout des valeurs sur les barres
    for rect in rects1:
        height = rect.get_height()
        ax1.annotate(f'{height/1000:.0f}k€',
                    xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom')

    for rect in rects2:
        height = rect.get_height()
        ax1.annotate(f'{height/1000:.0f}k€',
                    xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom')

    # Taux de marge nette
    rects3 = ax2.bar(x - width/2, simulation1.resultats_annuels['Taux_Marge_Nette'] * 100,
                    width, label='Scénario 1', color=colors[1])
    rects4 = ax2.bar(x + width/2, simulation2.resultats_annuels['Taux_Marge_Nette'] * 100,
                    width, label='Scénario 2', color=colors[5])

    ax2.set_title('Taux de marge nette par année')
    ax2.set_xlabel('Année')
    ax2.set_ylabel('Taux de marge (%)')
    ax2.set_xticks(x)
    ax2.set_ylim(0, 60)
    ax2.legend()

    # Ajout des valeurs sur les barres
    for rect in rects3:
        height = rect.get_height()
        ax2.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom')

    for rect in rects4:
        height = rect.get_height()
        ax2.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width()/2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom')

    plt.tight_layout()

    return fig

def streamlit_repartition_couts(simulation):
    """
    Visualise la répartition des coûts et du résultat net par rapport au chiffre d'affaires

    Args:
        simulation (SimulationFinanciere): Instance de simulation
    """
    if simulation.resultats is None:
        simulation.run_simulation()

    resultats = simulation.resultats.copy()

    # Création d'un DataFrame pour la visualisation en aires empilées
    df_stacked = pd.DataFrame(index=resultats.index)

    # Ajout des différentes composantes de coûts
    df_stacked['Salaires et charges'] = resultats['Cout_Salaires']
    df_stacked['Frais fixes'] = resultats['Frais_Fixes']
    df_stacked['Marge de sécurité'] = resultats['Marge_Securite']
    df_stacked['Impôts Sénégal'] = resultats['IS_Senegal']
    df_stacked['Impôts France'] = resultats['IS_France']
    df_stacked['Résultat net'] = resultats['Resultat_Net_Consolide']

    # Vérification que la somme correspond bien au CA
    total = df_stacked.sum(axis=1)
    print("total:", total, type(total))
    print("resultats['CA_SAS']:", resultats['CA_SAS'], type(resultats['CA_SAS']))
    print("total dtype:", getattr(total, 'dtype', 'N/A'))
    print("CA_SAS dtype:", getattr(resultats.get('CA_SAS'), 'dtype', 'N/A'))
    # Ajustement si nécessaire pour que la somme soit exactement égale au CA
    if not np.allclose(total.astype(float), resultats['CA_SAS'].astype(float)):
        # Ajout d'une petite correction au résultat net pour que tout s'additionne parfaitement
        df_stacked['Résultat net'] = resultats['CA_SAS'] - df_stacked.drop('Résultat net', axis=1).sum(axis=1)

    # Création du graphique
    fig, ax = plt.subplots(figsize=(12, 8))
    colors = setup_style()

    # Tracé des aires empilées
    df_stacked.plot.area(ax=ax, stacked=True, alpha=0.7, linewidth=1,
                         colormap='viridis')

    # Ajout de la ligne de CA pour référence
    ax.plot(resultats.index, resultats['CA_SAS'], 'k--', linewidth=2,
            label='Chiffre d\'affaires')

    # Configuration
    ax.set_xlabel('Trimestre')
    ax.set_ylabel('Montant (€)')
    ax.yaxis.set_major_formatter(euro_formatter)
    ax.set_xticks(resultats.index)
    ax.set_xticklabels([f"T{i+1}" for i in resultats.index])

    # Lignes de séparation des années
    for year in range(1, simulation.params['nb_annees']):
        ax.axvline(x=year*4 - 0.5, color='gray', linestyle='--', alpha=0.5)
        ax.text(year*4 - 0.5, ax.get_ylim()[1]*0.95, f'Année {year+1}',
               rotation=90, verticalalignment='top', alpha=0.7)

    # Légende
    ax.legend(loc='upper left')

    plt.title('Répartition des coûts et du résultat net par rapport au chiffre d\'affaires')
    plt.tight_layout()

    return fig

def streamlit_repartition_couts_pourcentage(simulation):
    """
    Visualise la répartition des coûts et du résultat net en pourcentage du chiffre d'affaires

    Args:
        simulation (SimulationFinanciere): Instance de simulation
    """
    if simulation.resultats is None:
        simulation.run_simulation()

    resultats = simulation.resultats.copy()

    # Création d'un DataFrame pour la visualisation en aires empilées
    df_stacked = pd.DataFrame(index=resultats.index)

    # Calcul des pourcentages par rapport au CA
    ca = resultats['CA_SAS']
    df_stacked['Salaires et charges'] = resultats['Cout_Salaires'] / ca
    df_stacked['Frais fixes'] = resultats['Frais_Fixes'] / ca
    df_stacked['Marge de sécurité'] = resultats['Marge_Securite'] / ca
    df_stacked['Impôts Sénégal'] = resultats['IS_Senegal'] / ca
    df_stacked['Impôts France'] = resultats['IS_France'] / ca
    df_stacked['Résultat net'] = resultats['Resultat_Net_Consolide'] / ca

    # Vérification que la somme est proche de 1 (100%)
    total = df_stacked.sum(axis=1)
    # Ajustement si nécessaire pour que la somme soit exactement égale à 1
    if not np.allclose(total, 1.0):
        # Ajout d'une petite correction au résultat net pour que tout s'additionne à 100%
        df_stacked['Résultat net'] = 1.0 - df_stacked.drop('Résultat net', axis=1).sum(axis=1)

    # Création du graphique
    fig, ax = plt.subplots(figsize=(12, 8))
    colors = setup_style()

    # Tracé des aires empilées
    df_stacked.plot.area(ax=ax, stacked=True, alpha=0.7, linewidth=1,
                         colormap='viridis')

    # Configuration
    ax.set_xlabel('Trimestre')
    ax.set_ylabel('Pourcentage du chiffre d\'affaires')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0%}'))
    ax.set_xticks(resultats.index)
    ax.set_xticklabels([f"T{i+1}" for i in resultats.index])
    ax.set_ylim(0, 1)

    # Lignes de séparation des années
    for year in range(1, simulation.params['nb_annees']):
        ax.axvline(x=year*4 - 0.5, color='gray', linestyle='--', alpha=0.5)
        ax.text(year*4 - 0.5, ax.get_ylim()[1]*0.95, f'Année {year+1}',
               rotation=90, verticalalignment='top', alpha=0.7)

    # Légende
    ax.legend(loc='upper left')

    plt.title('Répartition des coûts et du résultat net en pourcentage du chiffre d\'affaires')
    plt.tight_layout()

    return fig