#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 16:56:48 2022

@author: jackkellett
"""

# LIBRARIES #
import pandas as pd
import plotly
import plotly.express as px

# DATAFRAME # 
df_sources = pd.read_excel('Household_Appliances.xlsx')

# EXTRACT DATA FROM SPREADSHEET #
appliance    = df_sources['Appliance']
households = df_sources['Households']
survey     = df_sources['Survey']

# TEST LAST SECTION #
print(appliance)
print(households)
print(survey)

fig_sources = px.bar(
    df_sources,
    title = 'Appliances used in the Household',
    x = appliance,
    y = households,
    animation_frame = survey,
    animation_group = appliance,
    range_y = [0,55])

plotly.offline.plot(fig_sources, filename = 'household_appliances.html')