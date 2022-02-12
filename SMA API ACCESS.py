import requests
from requests.structures import CaseInsensitiveDict

# Above exclusively for requests, bottom is normal program
import datetime as dt
import dash
import dash_core_components as dcc # from dash import dcc 
import dash_html_components as html # from dash import html
from dash.dependencies import Input, Output
import requests
import pandas as pd
import plotly.express as px
from datetime import date
import time
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SPACELAB]) # Themes for Dash Bootstrap themes CSS DARKLY https://www.bootstrapcdn.com/bootswatch/

def success(status):
       if status == 200 or status == 201:
              return True
       else:
              return False

# GET API DATA USING FUNCTION EXAMPLE
def stateofCharge(): # Ordinary functions are app callbacks not needed (for time being), non-differing inputs, excel values read in are constant
    date = []
    for i in range(1,30):
           if i < 10:
              date.append('2022-02-0{0}'.format(i))
           else:
              date.append('2022-02-{0}'.format(i))   
    fig = go.Figure()
    fig.add_trace(go.Scatter(
                    x = date,
                    y = stateOfCharge,
                    mode = 'lines+markers', 
                    name = 'State of Charge'
                ))

    fig.update_layout(
                    title ='Battery State of Charge (Plant {0}):'.format(data_initial['plants'][0]['plantId']),
                    xaxis_title='Last 30 days',
                    yaxis_title='State of Charge (%)',
                    autotypenumbers='convert types',
                    )
    
    return fig 

def totalConsumption(): # Ordinary functions are app callbacks not needed (for time being), non-differing inputs, excel values read in are constant
    date = []
    for i in range(1,30):
           if i < 10:
              date.append('2022-02-0{0}'.format(i))
           else:
              date.append('2022-02-{0}'.format(i))   
    fig = go.Figure()
    fig.add_trace(go.Scatter(
                    x = date,
                    y = Totalconsumption,
                    mode = 'lines+markers',
                                    
                ))
    fig.update_layout(
                    title ='Total Consumption (Plant {0}):'.format(data_initial['plants'][0]['plantId']),
                    xaxis_title='Last 30 days',
                    yaxis_title='Total Consumption (Wh)',
                    autotypenumbers='convert types',
                    )
    
    return fig 


session = requests.session() # Reusable persistent connection

# STEP 1
STEPONEURL = "https://auth.smaapis.de/oauth2/token"
step1payload = "POST%20sandbox.smaapis.de%2Foauth2%2Ftoken=&HTTP%2F1.1=&Host%3A%20smaapis.de=&Content-Type%3A%20application%2Fx-www-form-urlencoded=&client_id=strathclyde_api&client_secret=1f773505-616b-49a0-a462-5889fa690384&grant_type=client_credentials&="
headers1 = CaseInsensitiveDict()
headers1["Content-Type"] = "application/x-www-form-urlencoded"

r1 = requests.post(STEPONEURL, data=step1payload,headers=headers1)
print("\n(STEP ONE) Status Code: {0}. Successful: {1}\n".format(r1.status_code,success(r1.status_code)))
TOKEN = r1.json()['access_token']
print("{0}\n".format(TOKEN)) # (PRINT TOKEN)

# STEP 2
STEPTWOURL = "https://async-auth.smaapis.de/oauth2/v2/bc-authorize"
headers2 = {'Content-Type': 'application/json','Authorization':'Bearer {0}'.format(TOKEN)}
step2payload = {'loginHint':'aaron.shek.2020@uni.strath.ac.uk'}

r2 = requests.post(STEPTWOURL, json=step2payload,headers=headers2)
print("\n(STEP TWO) Status Code: {0}. Successful: {1}\n".format(r2.status_code,success(r2.status_code)))
print(r2.json())


# STEP 3 - GET DATA VIA API FOR EXAMPLE
r = "https://async-auth.smaapis.de/monitoring/v1/plants"
headers2 = {'Host':'smaapis.de','Content-Type': 'application/json','Authorization':'Bearer {0}'.format(TOKEN)}

r = session.get(r,headers=headers2)
print("\nStatus Code: {0}. Successful: {1}\n".format(r.status_code,success(r.status_code)))
data_initial = r.json()
print(data_initial)

# GET DATA VIA LOOP
stateOfCharge = []
batteryDischarging = []
Totalconsumption = []
start = time.time()
for i in range(1,30):
       if i < 10: # If date less than 10 to suit YYYY-MM-DD Format
              r = "https://async-auth.smaapis.de/monitoring/v1/plants/5340310/measurements/sets/EnergyBalance/Day?Date=2022-01-0{0}&WithTotal=true".format(i)
       else:
              r = "https://async-auth.smaapis.de/monitoring/v1/plants/5340310/measurements/sets/EnergyBalance/Day?Date=2022-01-{0}&WithTotal=true".format(i)

       headers2 = {'Host':'smaapis.de','Content-Type': 'application/json','Authorization':'Bearer {0}'.format(TOKEN)}
       r = session.get(r,headers=headers2)
       data = r.json()
       stateOfCharge.append(data['set'][i]['batteryStateOfCharge'])
       batteryDischarging.append(data['set'][i]['batteryDischarging'])
       Totalconsumption.append(data['set'][i]['totalConsumption'])
       # print(data['set'][i]['batteryStateOfCharge'])
end = time.time()

print("\nIt took ",end-start, " seconds to do ", i, " API GET requests. ")

app.layout = html.Div([ # SHOW GRAPH IN HTML
       dcc.Graph(id = 'holder_graph_1', figure = stateofCharge()),
       dcc.Graph(id = 'holder_graph_2', figure = totalConsumption()),
])

# ALL DATA YOU CAN RETRIEVE
r = "https://async-auth.smaapis.de/monitoring/v1/plants/5340310/measurements/sets/EnergyBalance/Recent?WithTotal=true"
headers2 = {'Host':'smaapis.de','Content-Type': 'application/json','Authorization':'Bearer {0}'.format(TOKEN)}
r = session.get(r,headers=headers2)
print("\nStatus Code: {0}. Successful: {1}\n".format(r.status_code,success(r.status_code)))
data_test = r.json()
print(data_test)

# https://sandbox.smaapis.de/monitoring/index.html
if __name__ == '__main__': # Protects users from accidentally invoking the script when they didn't intend to. Based on Flask framework
    app.run_server(debug=True) # Ctrl+C in terminal to terminate

