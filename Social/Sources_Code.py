#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 20:58:39 2022

@author: jackkellett
"""

# LIBRARIES #
import pandas as pd
import plotly
import plotly.express as px

# DATAFRAME # 
df_sources = pd.read_excel('Electricity_Source.xlsx')

# EXTRACT DATA FROM SPREADSHEET #
sources    = df_sources['Source']
households = df_sources['Households']
survey     = df_sources['Survey']

# TEST LAST SECTION #
print(sources)
print(households)
print(survey)

fig_sources = px.bar(
    df_sources,
    title = 'Source of Electricity Used (Household)',
    x = sources,
    y = households,
    animation_frame = survey,
    animation_group = sources,
    range_y = [0,55])

plotly.offline.plot(fig_sources, filename = 'source.html')