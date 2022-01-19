#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 10:58:45 2022

@author: jackkellett
"""

# LIBRARIES #
import pandas as pd
import plotly
import plotly.express as px

# DATAFRAME # 
df_satisfaction = pd.read_excel('Cost_Satisfaction.xlsx')

survey  = df_satisfaction['Survey']

v_unhap = df_satisfaction['Very Unhappy']
q_unhap = df_satisfaction['Quite Unhappy']
neutral = df_satisfaction['Neutral']
q_hap   = df_satisfaction['Quite Happy']
v_hap   = df_satisfaction['Very Happy']

fig_satisfaction = px.bar(
    df_satisfaction,
    title = 'Cost Satisfaction',
    x = survey,
    y = [v_unhap,q_unhap,neutral,q_hap,v_hap],
    color_discrete_map = {
        'Very Unhappy':'red',
        'Quite Unhappy':'orange',
        'Neutral':'yellow',
        'Quite Happy':'limegreen',
        'Very Happy':'green'},
    range_y = [0,55],
    )

plotly.offline.plot(fig_satisfaction, filename = 'CostSatisfaction.html')