#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 16:35:09 2022

@author: jackkellett
"""

# LIBRARIES #
import pandas as pd
import plotly
import plotly.express as px

# DATAFRAME # 
df_sources = pd.read_excel('Lighting_Source.xlsx')

# EXTRACT DATA FROM SPREADSHEET #
light_sources    = df_sources['Light Source']
households = df_sources['Households']
survey     = df_sources['Survey']

# TEST LAST SECTION #
print(light_sources)
print(households)
print(survey)

fig_sources = px.bar(
    df_sources,
    title = 'Light Sources used in the Household',
    x = light_sources,
    y = households,
    animation_frame = survey,
    animation_group = light_sources,
    range_y = [0,55])

plotly.offline.plot(fig_sources, filename = 'light_source.html')