#!/usr/bin/env python3


"""
Formatting utilities for visualizations
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter


def setup_style():
    """Configure the style for visualizations"""
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("viridis")
    return sns.color_palette("viridis", 10)


euro_formatter = FuncFormatter(lambda x, p: f'{x:,.0f} €')


percent_formatter = FuncFormatter(lambda y, _: f'{y:.0%}')