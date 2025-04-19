#!/usr/bin/env python3


"""
Main script for the financial simulation of SAS France & SARL Senegal
"""

from model.simulation import SimulationFinanciere
from config.parameters import DEFAULT_PARAMS

def main():
    """Main function to run the simulation and its visualizations"""
    print("Simulation financière SAS France & SARL Sénégal")
    print("-" * 50)


    scenario1 = SimulationFinanciere()


    params_scenario2 = DEFAULT_PARAMS.copy()
    params_scenario2['salaire_dev'] = 1500
    params_scenario2['salaire_lead'] = 2000
    scenario2 = SimulationFinanciere(params_scenario2)


    print("Exécution du scénario 1...")
    scenario1.run_simulation()
    print("Exécution du scénario 2...")
    scenario2.run_simulation()


    print("\nRésultats annuels - Scénario 1 (salaires modérés):")
    print(scenario1.resultats_annuels[['CA_SAS', 'Resultat_Net_Consolide', 'Taux_Marge_Nette']])

    print("\nRésultats annuels - Scénario 2 (salaires élevés):")
    print(scenario2.resultats_annuels[['CA_SAS', 'Resultat_Net_Consolide', 'Taux_Marge_Nette']])


    print("\nComparaison des scénarios:")
    from pandas import DataFrame
    comparaison = DataFrame({
        'Scénario 1': [scenario1.resultats_annuels['Resultat_Net_Consolide'].sum(),
                      scenario1.resultats_annuels['Taux_Marge_Nette'].mean()],
        'Scénario 2': [scenario2.resultats_annuels['Resultat_Net_Consolide'].sum(),
                      scenario2.resultats_annuels['Taux_Marge_Nette'].mean()]
    }, index=['Résultat total sur 3 ans', 'Taux de marge moyen'])
    print(comparaison)


    print("\nGénération des visualisations...")
    scenario1.run_all_visualizations(scenario2)

    print("\nSimulation terminée avec succès!")


if __name__ == "__main__":
    main()