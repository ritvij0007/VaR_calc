# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 05:25:13 2024

@author: HP
"""

# Define model specifications with supported distributions
model = [
    {'vol': 'Garch', 'dist': 'normal', 'o': 0},
    {'vol': 'Garch', 'dist': 'ged', 'o': 0},
    {'vol': 'Garch', 'dist': 'normal', 'o': 1},  # GJR-GARCH
    {'vol': 'Garch', 'dist': 'ged', 'o': 1}     # GJR-GARCH
]
