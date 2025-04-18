#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilitaires de formatage pour les visualisations
"""
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Configuration du style
def setup_style():
    """Configure le style des visualisations"""
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("viridis")
    return sns.color_palette("viridis", 10)

# Formateur pour les montants en euros
euro_formatter = FuncFormatter(lambda x, p: f'{x:,.0f} €')

# Formateur pour les pourcentages
percent_formatter = FuncFormatter(lambda y, _: f'{y:.0%}')  