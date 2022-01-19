#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 10:01:02 2022

@author: jackkellett
"""

# LIBRARIES #
import pandas as pd
import plotly
import plotly.express as px

# DATAFRAME # 
df_income = pd.read_excel('Monthly_Income.xlsx')

# EXTRACT DATA FROM SPREADSHEET #
income = df_income['Mean Income (MWK)']
limit  = df_income['Range']
survey = df_income['Survey']

# TEST LAST SECTION #
print(income)
print(limit)
print(survey)

fig_sources = px.line(
    df_income,
    title = 'Monthly Income (MWK)',
    x = survey,
    y = income,
    color = limit,
    )

plotly.offline.plot(fig_sources, filename = 'monthly_income.html')