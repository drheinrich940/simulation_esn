#!/usr/bin/env python3


"""
Streamlit application for financial simulation of SAS France & SARL Senegal
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from config.parameters import DEFAULT_PARAMS
from model.simulation import SimulationFinanciere
from visualization.streamlit_plots import (
    streamlit_evolution_ca_resultats,
    streamlit_repartition_benefices,
    streamlit_comparaison_scenarios,
    streamlit_repartition_couts,
    streamlit_repartition_couts_pourcentage
)


st.set_page_config(
    page_title="Simulation Financière ESN",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("Simulation Financière SAS France & SARL Sénégal")
st.markdown("Cette application permet de simuler et visualiser les résultats financiers d'un modèle SAS France / SARL Sénégal.")


with st.expander("Instructions d'utilisation", expanded=True):
    st.markdown("""
    ### Comment utiliser cette application

    1. **Ajustez les paramètres** dans la barre latérale à gauche selon vos besoins
    2. **Personnalisez le scénario 2** pour comparer différentes configurations
    3. **Cliquez sur 'Exécuter la simulation'** pour lancer les calculs
    4. **Explorez les résultats** dans les différents onglets:
       - **Résultats**: Tableaux de données et métriques clés
       - **Visualisations**: Graphiques d'analyse des résultats
       - **Comparaison**: Comparaison entre les deux scénarios
    5. **Téléchargez les données** au format CSV pour une analyse plus approfondie

    Vous pouvez à tout moment réinitialiser les paramètres en cliquant sur le bouton "Réinitialiser les paramètres" dans la barre latérale.
    """)


if 'params' not in st.session_state:
    st.session_state.params = DEFAULT_PARAMS.copy()


st.sidebar.title("Paramètres de simulation")


def param_widget(label, key, min_value=None, max_value=None, step=None, format=None, help=None):
    value = st.session_state.params[key]


    if isinstance(value, bool):
        return st.sidebar.checkbox(label, value, key=key, help=help)
    elif isinstance(value, int):
        return st.sidebar.number_input(label, min_value=min_value, max_value=max_value, value=value, step=step or 1, key=key, help=help)
    elif isinstance(value, float):
        if key.startswith('taux_'):

            value_percent = value * 100
            min_value_percent = (min_value or 0.0) * 100
            max_value_percent = (max_value or 1.0) * 100
            step_percent = (step or 0.01) * 100

            result_percent = st.sidebar.slider(label,
                                     min_value=min_value_percent,
                                     max_value=max_value_percent,
                                     value=value_percent,
                                     step=step_percent,
                                     format="%g%%",
                                     key=key,
                                     help=help)


            return result_percent / 100
        else:
            return st.sidebar.number_input(label, min_value=min_value, max_value=max_value, value=value, step=step or 0.1, format=format, key=key, help=help)
    else:
        return st.sidebar.text_input(label, value, key=key, help=help)

with st.sidebar.expander("Paramètres généraux", expanded=True):
    st.session_state.params['nb_annees'] = param_widget("Nombre d'années de simulation", 'nb_annees', min_value=1, max_value=10, help="Durée de la simulation en années")
    st.session_state.params['taux_is_france'] = param_widget("Taux d'imposition en France", 'taux_is_france', min_value=0.0, max_value=0.5, help="Taux d'impôt sur les sociétés en France")
    st.session_state.params['taux_is_senegal'] = param_widget("Taux d'imposition au Sénégal", 'taux_is_senegal', min_value=0.0, max_value=0.5, help="Taux d'impôt sur les sociétés au Sénégal")
    st.session_state.params['taux_charges_patronales'] = param_widget("Taux de charges patronales", 'taux_charges_patronales', min_value=0.0, max_value=0.5, help="Taux de charges patronales au Sénégal")
    st.session_state.params['marge_securite'] = param_widget("Marge de sécurité", 'marge_securite', min_value=0.0, max_value=0.5, help="Marge de sécurité pour la SARL (%)")


with st.sidebar.expander("Paramètres de facturation", expanded=False):
    st.session_state.params['tjm_dev'] = param_widget("Tarif journalier développeur (€)", 'tjm_dev', min_value=100, max_value=800, help="Tarif journalier moyen facturé pour un développeur")
    st.session_state.params['tjm_lead'] = param_widget("Tarif journalier lead technique (€)", 'tjm_lead', min_value=100, max_value=1000, help="Tarif journalier moyen facturé pour un lead technique")
    st.session_state.params['tjm_cdp'] = param_widget("Tarif journalier chef de projet (€)", 'tjm_cdp', min_value=100, max_value=1000, help="Tarif journalier moyen facturé pour un chef de projet")
    st.session_state.params['taux_occupation_dev'] = param_widget("Taux d'occupation des développeurs", 'taux_occupation_dev', min_value=0.0, max_value=1.0, help="Pourcentage du temps facturable pour les développeurs")
    st.session_state.params['taux_occupation_lead'] = param_widget("Taux d'occupation du lead", 'taux_occupation_lead', min_value=0.0, max_value=1.0, help="Pourcentage du temps facturable pour le lead technique")
    st.session_state.params['taux_occupation_cdp'] = param_widget("Taux d'occupation du chef de projet", 'taux_occupation_cdp', min_value=0.0, max_value=1.0, help="Pourcentage du temps facturable pour le chef de projet")
    st.session_state.params['jours_facturable_mois'] = param_widget("Jours facturables par mois", 'jours_facturable_mois', min_value=1, max_value=23, help="Nombre de jours facturables par mois")


with st.sidebar.expander("Paramètres de salaires", expanded=False):
    st.session_state.params['salaire_dev'] = param_widget("Salaire mensuel développeur (€)", 'salaire_dev', min_value=500, max_value=3000, help="Salaire mensuel moyen d'un développeur")
    st.session_state.params['salaire_lead'] = param_widget("Salaire mensuel lead technique (€)", 'salaire_lead', min_value=500, max_value=4000, help="Salaire mensuel du lead technique")
    st.session_state.params['salaire_cdp'] = param_widget("Salaire mensuel chef de projet (€)", 'salaire_cdp', min_value=500, max_value=3000, help="Salaire mensuel du chef de projet")
    st.session_state.params['salaire_rh'] = param_widget("Salaire mensuel RH (€)", 'salaire_rh', min_value=500, max_value=2000, help="Salaire mensuel du responsable RH")


with st.sidebar.expander("Paramètres d'évolution des effectifs", expanded=False):
    st.session_state.params['effectif_dev_initial'] = param_widget("Nombre initial de développeurs", 'effectif_dev_initial', min_value=1, max_value=20, help="Nombre de développeurs au démarrage")
    st.session_state.params['ajout_dev_par_trimestre'] = param_widget("Ajout de développeurs par trimestre", 'ajout_dev_par_trimestre', min_value=0, max_value=10, help="Nombre de développeurs ajoutés chaque trimestre")
    st.session_state.params['trimestre_ajout_support'] = param_widget("Trimestre d'ajout des postes support", 'trimestre_ajout_support', min_value=1, max_value=12, help="Trimestre à partir duquel les postes support sont ajoutés")


with st.sidebar.expander("Paramètres de frais fixes", expanded=False):
    st.session_state.params['frais_fixes_annee1'] = param_widget("Frais fixes mensuels année 1 (€)", 'frais_fixes_annee1', min_value=0, max_value=10000, help="Frais fixes mensuels pour la première année")
    st.session_state.params['frais_fixes_annee2'] = param_widget("Frais fixes mensuels année 2 (€)", 'frais_fixes_annee2', min_value=0, max_value=15000, help="Frais fixes mensuels pour la deuxième année")
    st.session_state.params['frais_fixes_annee3'] = param_widget("Frais fixes mensuels année 3 (€)", 'frais_fixes_annee3', min_value=0, max_value=20000, help="Frais fixes mensuels pour la troisième année")


if st.sidebar.button("Réinitialiser les paramètres"):
    st.session_state.params = DEFAULT_PARAMS.copy()
    st.experimental_rerun()


simulation = SimulationFinanciere(st.session_state.params)


if 'scenario2_params' not in st.session_state:
    st.session_state.scenario2_params = DEFAULT_PARAMS.copy()

    st.session_state.scenario2_params['salaire_dev'] = 1500   # +50%
    st.session_state.scenario2_params['salaire_lead'] = 2000  # +33%


with st.sidebar.expander("Paramètres du scénario 2", expanded=False):
    st.markdown("**Personnalisation du scénario de comparaison**")


    def param_widget_scenario2(label, key, min_value=None, max_value=None, step=None, format=None, help=None):
        value = st.session_state.scenario2_params[key]


        if isinstance(value, bool):
            return st.checkbox(label, value, key=f"s2_{key}", help=help)
        elif isinstance(value, int):
            return st.number_input(label, min_value=min_value, max_value=max_value, value=value, step=step or 1, key=f"s2_{key}", help=help)
        elif isinstance(value, float):
            if key.startswith('taux_'):

                return st.slider(label, min_value=min_value or 0.0, max_value=max_value or 1.0, value=value, step=step or 0.01, format=format or "%.0f%%", key=f"s2_{key}", help=help)
            else:
                return st.number_input(label, min_value=min_value, max_value=max_value, value=value, step=step or 0.1, format=format, key=f"s2_{key}", help=help)
        else:
            return st.text_input(label, value, key=f"s2_{key}", help=help)


    st.session_state.scenario2_params['salaire_dev'] = param_widget_scenario2("Salaire mensuel développeur (€)", 'salaire_dev', min_value=500, max_value=3000)
    st.session_state.scenario2_params['salaire_lead'] = param_widget_scenario2("Salaire mensuel lead technique (€)", 'salaire_lead', min_value=500, max_value=4000)
    st.session_state.scenario2_params['tjm_dev'] = param_widget_scenario2("Tarif journalier développeur (€)", 'tjm_dev', min_value=100, max_value=800)
    st.session_state.scenario2_params['taux_occupation_dev'] = param_widget_scenario2("Taux d'occupation des développeurs", 'taux_occupation_dev', min_value=0.0, max_value=1.0)


    if st.button("Copier les paramètres du scénario 1"):
        st.session_state.scenario2_params = st.session_state.params.copy()
        st.experimental_rerun()

simulation2 = SimulationFinanciere(st.session_state.scenario2_params)


if st.button("Exécuter la simulation"):
    with st.spinner("Calcul des résultats en cours..."):
        simulation.run_simulation()
        simulation2.run_simulation()


        tab1, tab2, tab3 = st.tabs(["Résultats", "Visualisations", "Comparaison"])

        with tab1:
            st.subheader("Résultats annuels")
            st.dataframe(simulation.resultats_annuels)


            csv_annuels = simulation.resultats_annuels.to_csv(index=True)
            st.download_button(
                label="Télécharger les résultats annuels (CSV)",
                data=csv_annuels,
                file_name="resultats_annuels.csv",
                mime="text/csv",
            )

            st.subheader("Résultats trimestriels")
            st.dataframe(simulation.resultats)


            csv_trimestriels = simulation.resultats.to_csv(index=True)
            st.download_button(
                label="Télécharger les résultats trimestriels (CSV)",
                data=csv_trimestriels,
                file_name="resultats_trimestriels.csv",
                mime="text/csv",
            )


            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Résultat net total", f"{simulation.resultats_annuels['Resultat_Net_Consolide'].sum():,.0f} €")
            with col2:
                st.metric("Taux de marge moyen", f"{simulation.resultats_annuels['Taux_Marge_Nette'].mean():.1%}")
            with col3:
                st.metric("Effectif final", f"{simulation.resultats['Nb_Developpeurs'].iloc[-1] + simulation.resultats['Nb_Lead'].iloc[-1] + simulation.resultats['Nb_CDP'].iloc[-1] + simulation.resultats['Nb_RH'].iloc[-1]}")

        with tab2:

            viz_tab1, viz_tab2, viz_tab3, viz_tab4, viz_tab5, viz_tab6 = st.tabs([
                "Évolution CA et résultats",
                "Répartition bénéfices",
                "Répartition des coûts",
                "Analyse sensibilité",
                "Évolution effectifs",
                "Point mort et ROI"
            ])

            with viz_tab1:
                st.subheader("Évolution trimestrielle du CA et des résultats")
                fig_ca = streamlit_evolution_ca_resultats(simulation)
                st.pyplot(fig_ca)

            with viz_tab2:
                st.subheader("Répartition des bénéfices entre SAS et SARL")
                fig_benef = streamlit_repartition_benefices(simulation)
                st.pyplot(fig_benef)

            with viz_tab3:
                st.subheader("Répartition des coûts par rapport au chiffre d'affaires")


                view_type = st.radio(
                    "Afficher les coûts en:",
                    ["Valeurs absolues (€)", "Pourcentages (%)"],
                    horizontal=True
                )

                if view_type == "Valeurs absolues (€)":
                    fig_couts = streamlit_repartition_couts(simulation)
                else:
                    fig_couts = streamlit_repartition_couts_pourcentage(simulation)

                st.pyplot(fig_couts)


                with st.expander("Comprendre ce graphique"):
                    st.markdown("""
                    Ce graphique montre comment le chiffre d'affaires est réparti entre les différentes catégories de coûts et le résultat net:

                    - **Salaires et charges**: Coûts salariaux incluant les charges patronales
                    - **Frais fixes**: Loyers, équipements, services, etc.
                    - **Marge de sécurité**: Marge ajoutée pour sécuriser les opérations de la SARL
                    - **Impôts Sénégal**: Impôts sur les sociétés payés au Sénégal
                    - **Impôts France**: Impôts sur les sociétés payés en France
                    - **Résultat net**: Bénéfice net après tous les coûts et impôts

                    La ligne pointillée noire représente le chiffre d'affaires total.
                    La somme de toutes les aires correspond exactement au chiffre d'affaires.
                    """)

            with viz_tab4:
                st.subheader("Analyse de sensibilité des principaux paramètres")
                with st.spinner("Génération de l'analyse de sensibilité..."):
                    fig_sens = plt.figure(figsize=(10, 12))
                    simulation.plot_analyse_sensibilite()
                    st.pyplot(fig_sens)

            with viz_tab5:
                st.subheader("Évolution des effectifs et des coûts moyens")
                fig_eff = plt.figure(figsize=(10, 6))
                simulation.plot_evolution_effectifs_couts()
                st.pyplot(fig_eff)

            with viz_tab6:
                st.subheader("Analyse du point mort et du ROI")
                with st.spinner("Génération de l'analyse du point mort et du ROI..."):
                    fig_roi = plt.figure(figsize=(12, 6))
                    simulation.plot_point_mort_roi()
                    st.pyplot(fig_roi)

        with tab3:
            st.subheader("Comparaison des scénarios")


            st.markdown("**Scénario 1:** Paramètres définis dans l'interface")
            st.markdown("**Scénario 2:** Salaires plus élevés (Développeur: 1500€, Lead: 2000€)")


            fig_comp = streamlit_comparaison_scenarios(simulation, simulation2)
            st.pyplot(fig_comp)


            comparaison = pd.DataFrame({
                'Scénario 1': [simulation.resultats_annuels['Resultat_Net_Consolide'].sum(),
                              simulation.resultats_annuels['Taux_Marge_Nette'].mean()],
                'Scénario 2': [simulation2.resultats_annuels['Resultat_Net_Consolide'].sum(),
                              simulation2.resultats_annuels['Taux_Marge_Nette'].mean()]
            }, index=['Résultat total sur 3 ans', 'Taux de marge moyen'])

            st.dataframe(comparaison)
