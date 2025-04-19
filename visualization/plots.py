#!/usr/bin/env python3


"""
Visualization functions for the financial simulation
"""
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from utils.formatting import euro_formatter, percent_formatter, setup_style

colors = setup_style()

def plot_evolution_ca_resultats(resultats, params, nom_fichier=None):
    """
    Visualize the quarterly evolution of revenue and results

    Args:
        resultats (pandas.DataFrame): DataFrame of quarterly results
        params (dict): Simulation parameters
        nom_fichier (str, optional): Filename to save the chart
    """
    fig, ax = plt.subplots(figsize=(12, 6))


    ax.plot(resultats.index + 1, resultats['CA_SAS'],
            marker='o', label='Chiffre d\'affaires', color=colors[0], linewidth=2)
    ax.plot(resultats.index + 1, resultats['Transfert_SARL'],
            marker='s', label='Transfert vers SARL', color=colors[2], linewidth=2)
    ax.plot(resultats.index + 1, resultats['Resultat_Net_Consolide'],
            marker='^', label='Résultat net consolidé', color=colors[4], linewidth=2)


    ax2 = ax.twinx()
    ax2.bar(resultats.index + 1, resultats['Nb_Developpeurs'],
            alpha=0.2, color=colors[8], label='Nb de développeurs')
    ax2.set_ylabel('Nombre de développeurs', color=colors[8])
    ax2.tick_params(axis='y', labelcolor=colors[8])


    ax.set_xlabel('Trimestre')
    ax.set_ylabel('Montant (€)')
    ax.yaxis.set_major_formatter(euro_formatter)
    ax.set_xticks(resultats.index + 1)
    ax.set_xticklabels([f"T{i+1}" for i in resultats.index])


    for year in range(1, params['nb_annees']):
        ax.axvline(x=year*4 + 0.5, color='gray', linestyle='--', alpha=0.5)
        ax.text(year*4 + 0.5, ax.get_ylim()[1]*0.95, f'Année {year+1}',
               rotation=90, verticalalignment='top', alpha=0.7)


    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.title('Évolution trimestrielle du CA, des transferts et des résultats')
    plt.tight_layout()

    if nom_fichier:
        plt.savefig(nom_fichier, dpi=300, bbox_inches='tight')

    import streamlit as st
    st.pyplot(plt.gcf())

def plot_repartition_benefices(resultats_annuels, nom_fichier=None):
    """
    Visualize the distribution of profits between SAS and SARL

    Args:
        resultats_annuels (pandas.DataFrame): DataFrame of annual results
        nom_fichier (str, optional): Filename to save the chart
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))


    resultats_annuels[['Part_SAS', 'Part_SARL']].plot(
        kind='bar', stacked=True, ax=ax1, color=[colors[1], colors[5]])

    ax1.set_title('Répartition des bénéfices (en %)')
    ax1.set_xlabel('Année')
    ax1.set_ylabel('Part du résultat consolidé')
    ax1.set_ylim(0, 1)
    ax1.set_yticks(np.arange(0, 1.1, 0.1))
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0%}'))


    for i, row in enumerate(resultats_annuels.iterrows()):
        ax1.text(i, 0.5, f"{row[1]['Part_SAS']:.1%}", ha='center', color='white', fontweight='bold')
        ax1.text(i, 0.95, f"{row[1]['Part_SARL']:.1%}", ha='center', color='white', fontweight='bold')


    bar_plot = ax2.bar(resultats_annuels.index, resultats_annuels['Ratio_SAS_SARL'], color=colors[3])
    ax2.set_title('Ratio SAS/SARL (déséquilibre fiscal)')
    ax2.set_xlabel('Année')
    ax2.set_ylabel('Ratio')


    ax2.axhspan(15, ax2.get_ylim()[1], color='red', alpha=0.2, label='Zone à risque fiscal')


    for bar in bar_plot:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
               f'{height:.1f}', ha='center', va='bottom')

    ax2.legend()
    plt.tight_layout()

    if nom_fichier:
        plt.savefig(nom_fichier, dpi=300, bbox_inches='tight')

    import streamlit as st
    st.pyplot(plt.gcf())

def plot_analyse_sensibilite(simulation, nom_fichier=None):
    """
    Perform a sensitivity analysis of the main parameters

    Args:
        simulation (SimulationFinanciere): Simulation instance
        nom_fichier (str, optional): Filename to save the chart
    """

    params_to_analyze = {
        'salaire_dev': [800, 900, 1000, 1100, 1200, 1300, 1400, 1500],
        'tjm_dev': [250, 275, 300, 325, 350, 375, 400],
        'taux_occupation_dev': [0.70, 0.75, 0.80, 0.85, 0.90, 0.95]
    }

    param_labels = {
        'salaire_dev': 'Salaire mensuel développeur (€)',
        'tjm_dev': 'Tarif journalier développeur (€)',
        'taux_occupation_dev': 'Taux d\'occupation développeur'
    }


    fig, axes = plt.subplots(len(params_to_analyze), 1, figsize=(10, 12))

    base_params = simulation.params.copy()
    base_result = simulation.resultats['Resultat_Net_Consolide'].sum()

    for i, (param, values) in enumerate(params_to_analyze.items()):
        _plot_param_sensitivity(param, values, base_params, axes[i], param_labels, i)

    plt.suptitle('Analyse de sensibilité - Impact sur le résultat net consolidé sur 3 ans', fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.97])

    if nom_fichier:
        plt.savefig(nom_fichier, dpi=300, bbox_inches='tight')

    import streamlit as st
    st.pyplot(plt.gcf())

def _plot_param_sensitivity(param, values, base_params, ax, param_labels, color_index):
    """Helper function to plot parameter sensitivity"""
    from model.simulation import SimulationFinanciere

    results = []
    base_value = base_params[param]

    for value in values:

        temp_params = base_params.copy()
        temp_params[param] = value
        sim = SimulationFinanciere(temp_params)
        sim.run_simulation()
        total_result = sim.resultats['Resultat_Net_Consolide'].sum()
        results.append(total_result)


    base_index = values.index(base_value) if base_value in values else -1
    relative_results = [(r / results[base_index] - 1) * 100 for r in results] if base_index >= 0 else []


    ax.plot(values, results, marker='o', color=colors[color_index*2], linewidth=2)


    if base_index >= 0:
        ax.scatter([base_value], [results[base_index]], s=100, color='red', zorder=5)
        ax.axvline(x=base_value, color='gray', linestyle='--', alpha=0.5)


    if relative_results:
        for j, (x, y, rel) in enumerate(zip(values, results, relative_results)):
            if j != base_index:
                ax.annotate(f"{rel:+.1f}%",
                          xy=(x, y),
                          xytext=(0, 10 if rel > 0 else -15),
                          textcoords="offset points",
                          ha='center')


    ax.set_xlabel(param_labels[param])
    ax.set_ylabel('Résultat net consolidé sur 3 ans (€)')
    ax.yaxis.set_major_formatter(euro_formatter)
    ax.grid(True, linestyle='--', alpha=0.7)


    if param == 'taux_occupation_dev':
        ax.xaxis.set_major_formatter(percent_formatter)

def plot_evolution_effectifs_couts(resultats, params, nom_fichier=None):
    """
    Visualize the evolution of staff numbers and average costs per employee

    Args:
        resultats (pandas.DataFrame): DataFrame of quarterly results
        params (dict): Simulation parameters
        nom_fichier (str, optional): Filename to save the chart
    """

    resultats = resultats.copy()
    resultats['Total_Employes'] = resultats['Nb_Developpeurs'] + resultats['Nb_Lead'] + \
                                  resultats['Nb_CDP'] + resultats['Nb_RH']
    resultats['Cout_Moyen_Mensuel'] = resultats['Cout_Salaires'] / resultats['Total_Employes'] / 3

    fig, ax1 = plt.subplots(figsize=(12, 6))


    width = 0.35
    index = np.arange(len(resultats))

    p1 = ax1.bar(index, resultats['Nb_Developpeurs'], width,
                label='Développeurs', color=colors[0])
    p2 = ax1.bar(index, resultats['Nb_Lead'], width,
                bottom=resultats['Nb_Developpeurs'],
                label='Lead Technique', color=colors[2])
    p3 = ax1.bar(index, resultats['Nb_CDP'], width,
                bottom=resultats['Nb_Developpeurs'] + resultats['Nb_Lead'],
                label='Chef de Projet', color=colors[4])
    p4 = ax1.bar(index, resultats['Nb_RH'], width,
                bottom=resultats['Nb_Developpeurs'] + resultats['Nb_Lead'] + resultats['Nb_CDP'],
                label='RH', color=colors[6])


    ax2 = ax1.twinx()
    p5 = ax2.plot(index, resultats['Cout_Moyen_Mensuel'], marker='o',
                color='red', label='Coût moyen mensuel par employé')


    ax1.set_xlabel('Trimestre')
    ax1.set_ylabel('Nombre d\'employés')
    ax2.set_ylabel('Coût moyen mensuel par employé (€)')
    ax2.yaxis.set_major_formatter(euro_formatter)

    ax1.set_xticks(index)
    ax1.set_xticklabels([f"T{i+1}" for i in resultats.index])


    for year in range(1, params['nb_annees']):
        ax1.axvline(x=year*4 - 0.5, color='gray', linestyle='--', alpha=0.5)
        ax1.text(year*4 - 0.5, ax1.get_ylim()[1]*0.95, f'Année {year+1}',
               rotation=90, verticalalignment='top', alpha=0.7)


    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title('Évolution des effectifs et du coût moyen par employé')
    plt.tight_layout()

    if nom_fichier:
        plt.savefig(nom_fichier, dpi=300, bbox_inches='tight')

    import streamlit as st
    st.pyplot(plt.gcf())

def plot_comparaison_scenarios(scenario1, scenario2, nom_fichier=None):
    """
    Compare two simulation scenarios

    Args:
        scenario1 (SimulationFinanciere): First scenario
        scenario2 (SimulationFinanciere): Second scenario
        nom_fichier (str, optional): Filename to save the chart
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))


    x = np.arange(len(scenario1.resultats_annuels))
    width = 0.35

    rects1 = ax1.bar(x - width/2, scenario1.resultats_annuels['Resultat_Net_Consolide'],
                    width, label='Scénario 1', color=colors[0])
    rects2 = ax1.bar(x + width/2, scenario2.resultats_annuels['Resultat_Net_Consolide'],
                    width, label='Scénario 2', color=colors[4])

    ax1.set_title('Résultat net consolidé par année')
    ax1.set_xlabel('Année')
    ax1.set_ylabel('Résultat net (€)')
    ax1.set_xticks(x)
    ax1.yaxis.set_major_formatter(euro_formatter)
    ax1.legend()


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


    rects3 = ax2.bar(x - width/2, scenario1.resultats_annuels['Taux_Marge_Nette'] * 100,
                    width, label='Scénario 1', color=colors[1])
    rects4 = ax2.bar(x + width/2, scenario2.resultats_annuels['Taux_Marge_Nette'] * 100,
                    width, label='Scénario 2', color=colors[5])

    ax2.set_title('Taux de marge nette par année')
    ax2.set_xlabel('Année')
    ax2.set_ylabel('Taux de marge (%)')
    ax2.set_xticks(x)
    ax2.set_ylim(0, 60)
    ax2.legend()


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

    if nom_fichier:
        plt.savefig(nom_fichier, dpi=300, bbox_inches='tight')

    import streamlit as st
    st.pyplot(plt.gcf())

def plot_point_mort_roi(simulation, nom_fichier=None):
    """
    Analyze the break-even point and ROI according to different parameters

    Args:
        simulation (SimulationFinanciere): Simulation instance
        nom_fichier (str, optional): Filename to save the chart
    """
    from model.simulation import SimulationFinanciere


    simulation.resultats['ROI'] = simulation.resultats['Resultat_Net_Consolide'] / simulation.resultats['Transfert_SARL']


    tjm_values = np.linspace(200, 400, 20)  # 200€ à 400€
    occupation_values = np.linspace(0.5, 1.0, 10)  # 50% à 100%


    point_mort_matrix = np.zeros((len(occupation_values), len(tjm_values)))
    roi_matrix = np.zeros((len(occupation_values), len(tjm_values)))


    for i, taux_occupation in enumerate(occupation_values):
        for j, tjm in enumerate(tjm_values):
            temp_params = simulation.params.copy()
            temp_params['tjm_dev'] = tjm
            temp_params['taux_occupation_dev'] = taux_occupation

            sim = SimulationFinanciere(temp_params)
            sim.run_simulation()

            ca_annuel = sim.resultats_annuels.loc[1, 'CA_SAS']
            resultat_annuel = sim.resultats_annuels.loc[1, 'Resultat_Net_Consolide']
            transfert_annuel = sim.resultats_annuels.loc[1, 'Transfert_SARL']

            point_mort_matrix[i, j] = 1 if resultat_annuel > 0 else 0
            roi_matrix[i, j] = resultat_annuel / transfert_annuel if transfert_annuel > 0 else 0

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))


    im1 = ax1.imshow(point_mort_matrix, cmap='RdYlGn', aspect='auto', origin='lower',
                  extent=[tjm_values[0], tjm_values[-1], occupation_values[0], occupation_values[-1]])

    ax1.set_title('Analyse du point mort - Année 1')
    ax1.set_xlabel('Tarif journalier (€)')
    ax1.set_ylabel('Taux d\'occupation')
    ax1.yaxis.set_major_formatter(percent_formatter)


    ax1.axvline(x=simulation.params['tjm_dev'], color='blue', linestyle='--',
               label=f"TJM actuel: {simulation.params['tjm_dev']}€")
    ax1.axhline(y=simulation.params['taux_occupation_dev'], color='red', linestyle='--',
               label=f"Taux actuel: {simulation.params['taux_occupation_dev']:.0%}")

    ax1.legend(loc='lower right')
    plt.colorbar(im1, ax=ax1, label='Rentabilité')


    im2 = ax2.imshow(roi_matrix, cmap='viridis', aspect='auto', origin='lower',
                  extent=[tjm_values[0], tjm_values[-1], occupation_values[0], occupation_values[-1]])

    ax2.set_title('Analyse du ROI - Année 1')
    ax2.set_xlabel('Tarif journalier (€)')
    ax2.set_ylabel('Taux d\'occupation')
    ax2.yaxis.set_major_formatter(percent_formatter)


    ax2.axvline(x=simulation.params['tjm_dev'], color='blue', linestyle='--')
    ax2.axhline(y=simulation.params['taux_occupation_dev'], color='red', linestyle='--')

    plt.colorbar(im2, ax=ax2, label='ROI')

    plt.tight_layout()

    if nom_fichier:
        plt.savefig(nom_fichier, dpi=300, bbox_inches='tight')

    import streamlit as st
    st.pyplot(plt.gcf())