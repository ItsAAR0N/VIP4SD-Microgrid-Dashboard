#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 11:13:28 2022

@author: jackkellett
"""

# LIBRARIES #
import pandas as pd
import plotly
import plotly.express as px

# DATAFRAME # 
df_satisfaction = pd.read_excel('Recommendation_Likelihood.xlsx')

survey  = df_satisfaction['Survey']

v_unhap = df_satisfaction['Very Unlikely']
q_unhap = df_satisfaction['Unlikely']
neutral = df_satisfaction['May Recommend']
q_hap   = df_satisfaction['Likely']
v_hap   = df_satisfaction['Very Likely']

fig_satisfaction = px.bar(
    df_satisfaction,
    title = 'Recommendation Likelihood',
    x = survey,
    y = [v_unhap,q_unhap,neutral,q_hap,v_hap],
    color_discrete_map = {
        'Very Unlikely':'red',
        'Unlikely':'orange',
        'May Recommend':'yellow',
        'Likely':'limegreen',
        'Very Likely':'green'},
    range_y = [0,55],
    )

plotly.offline.plot(fig_satisfaction, filename = 'RecommendationLikelihood.html')