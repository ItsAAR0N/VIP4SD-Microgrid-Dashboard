#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 15:53:26 2021

@original author: heatherwaddell
@pre existing author(s): aaron,chris,jack
"""

import dash
import dash_core_components as dcc # from dash import dcc 
import dash_html_components as html # from dash import html
from dash.dependencies import Input, Output
import requests
import pandas as pd
import plotly.express as px
from datetime import date
import datetime
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB],suppress_callback_exceptions=True) 
server = app.server

"""
url = 'https://api.steama.co/get-token/' # https://api.steama.co/docs/#base-obtaining-a-token documentation
myobj = {'username': 'Christopher_Abi-Aad',
'password': 'JChhrvQ4mR'}
x = requests.post(url, data = myobj)
print(x.text) # Grab token via POST request 
"""

power = pd.read_csv(r'C:/Users/aaron/Desktop/Power.csv')
energy = pd.read_csv(r'C:/Users/aaron/Desktop/EnergyBalance.csv')
# ============================================================================================= WIP ================================================================================
# Temporary
def power_graph_PV(): # Ordinary functions are app callbacks not needed (for time being), non-differing inputs, excel values read in are constant

    fig = go.Figure()
    fig.add_trace(go.Scatter(
                    x = power.TimePeriod,
                    y = power.Power,
                    mode = 'lines+markers' 
                ))

    fig.update_layout(
                    title ='Power generation of PV system',
                    xaxis_title='',
                    yaxis_title='Power (kW)',
                    autotypenumbers='convert types',
                    )
    
    return fig 

def energy_graph_balance(): 

    fig = go.Figure()
    fig.add_trace(go.Scatter(
                    x = energy.TimePeriod,
                    y = energy.TotalConsumption,
                    mode = 'lines+markers' 
                ))

    fig.update_layout(
                    title ='Total Power Consumption',
                    xaxis_title='',
                    yaxis_title='Total consumption (W)',
                    autotypenumbers='convert types',
                    )
    
    return fig

def energy_graph_batterystatecharge(): 

    fig = go.Figure()
    fig.add_trace(go.Scatter(
                    x = energy.TimePeriod,
                    y = energy.BatteryStateOfCharge,
                    mode = 'lines+markers' 
                ))

    fig.update_layout(
                    title ='Battery State of Charge',
                    xaxis_title='',
                    yaxis_title='Battery State of Charge (%)',
                    autotypenumbers='convert types', # Automatically set number in order
                    )
    
    return fig

def energy_graph_totalgen(): 

    fig = go.Figure()
    fig.add_trace(go.Scatter(
                    x = energy.TimePeriod,
                    y = energy.TotalGeneration,
                    mode = 'lines+markers' 
                ))

    fig.update_layout(
                    title ='Total Generation',
                    xaxis_title='',
                    yaxis_title='Total generation (W)',
                    autotypenumbers='convert types',
                    )
    
    return fig

header = {'Authorization': 'Token 519802b968a55413f26964f53f99787cffaf11ac'}

url_ER = "https://api.steama.co/exchange-rates/?format=json"                   
r = requests.get(url=url_ER, headers = header)
s = r.content
df_ER = pd.read_json(s)

for index in range(len(df_ER['rate'])):
    if(df_ER['source'][index]=='MWK' and df_ER['target'][index]=='USD'):
        ER = df_ER['rate'][index]
        break
    else:
        continue
    
today = datetime.datetime.now()
past_date = str(today - datetime.timedelta(days=30))
start_time = past_date[0:10] + "T00:00:00"

C_date = str(today)

C_year = int(C_date[0:4])
C_month = int(C_date[5:7])
C_day = int(C_date[8:10])
     
url = "https://api.steama.co/sites/26385/revenue/" + "?start_time=" + start_time
r = requests.get(url=url, headers = header)
s = r.content
df = pd.read_json(s)

if(len(df)==0):
    print("There have been no transactions in the last 30 days.")
else:
    amountMK = 0
    
    for index in range(0,len(df['timestamp'])):
        amountMK += float((df['revenue'][index]))
        
    amountUSD = amountMK*ER
    
y_dont_care = []
x_dont_care = []
for index in range(1,24):
    y_dont_care.append(0)
    x_dont_care.append(index)
    
holder_fig = go.Figure()
holder_fig.add_trace(go.Scatter(x=x_dont_care, y=y_dont_care,
                    mode='lines+markers',
                    ))

holder_fig.update_layout(title = "Holder Graph",
               xaxis_title='Time',
               yaxis_title='Unknown')  

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
     "background-color": "#f2f2f2",
}

CONTENT_STYLE = {
    "margin-left": "17rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H1("Navigation"),

        html.Hr(),
        html.P(
            "Please use the below links to navigate the dashboard", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact", external_link=True),
                dbc.NavLink("Demand", href="/demand", active="exact", external_link=True),
                dbc.NavLink("Technical", href="/technical", active="exact", external_link=True),
                dbc.NavLink("Social Impact", href="/social", active="exact", external_link=True),
                dbc.NavLink("Maintenance", href="/maintenance", active="exact", external_link=True),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
        


content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])
# For YYYY-MM inputs
if C_month < 10: # To suit YY/MM format since C_month does not include the 0 in front of singular months i.e 01,03
    currentYYMM = '{0}-0{1}'.format(C_year,C_month) # C_ = Current 
else:
    currentYYMM = '{0}-{1}'.format(C_year,C_month) # Will update on a month by month basis

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
                html.Div(
                children = html.P("Mthembanji Microgrid Dashboard"),style={'backgroundColor': '#f2f2f2', 'textAlign': 'center','fontSize': 44}),
                html.Div([
                ], style={'textAlign': 'center'}),
                html.Hr(),
                html.Br(),
                html.Div([
                html.Img(src='https://www.sma-sunny.com/wp-content/uploads/2020/09/kv-micro-grids-malawi.jpg',style={'height':'70%', 'width':'70%'}),
                ], style={'textAlign': 'center'}),
                html.Br(),
                html.Hr(),
                html.Div(
                    html.H3("Background Information"),style={'backgroundColor': '#FFFFFF', 'text-decoration': 'underline'}),
                    html.P("This section is currently work in progress."),
                    html.P("Collecting and analysing data to understand microgrid performance is essential for informing effective maintenance schedules, business planning and technical designs for future microgrids. It can also inform policy interventions and help build a knowledgebase to accelerate the microgrid sector both nationally and globally. "),
                    html.P("Commissioned in July 2020, the Mthembanji solar microgrid has been collecting data through smart meters and remote monitoring devices for over a year. An objective of EASE is to utilise project learning to inform the microgrid sector in Malawi, specifically through analysis and sharing of data."),
                    html.H3("Why is Microgrid data important?"),
                    html.P("Many solar microgrid projects have faced sustainability challenges due to insufficient  maintenance or inefficient business models due to a lack of quality data collection and analysis. Microgrids that implement innovative smart metering and remote monitoring address these challenges, allowing developers to make informed decisions to ensure systems are operating  at optimum economic and technical efficiency in order to remain financially and practically viable. Analysing data also helps to fine-tune existing business models, by informing tariffs to ensure access to electricity is affordable for microgrid customers, while still maintaining sufficient income to be financially viable, offering confidence for potential investors. Perhaps most importantly, data analysis can help inform the technical design of other microgrids and therefore has the potential for impact on multiple sites."),
                    html.P("Data visualisation and sharing also enables funders, investors, researchers, and policymakers to monitor and understand microgrid performance, allowing use of the data to inform policy, investments, targeted research and other interventions in the microgrid enabling environment to accelerate their deployment.  In short, data analysis enables better informed and more efficient microgrid deployment, accelerating energy access and contributing to achieving SDG7."),
                    html.H3("What data are we monitoring?"),
                    html.P("Alongside information related to the wider EASE project monitoring and evaluation framework, data is being collected from the microgrid in themes of technical, economic, and social impact, summarised below:"),
                    html.P("Techincal Data:  relating the to the functionality of the generation and distribution systems, a variety of data on technical performance is being collected through remote monitoring of the PV, batteries and inverters, along with measurements and observations of the system collected through scheduled maintenance visits on site."),
                    html.P(""),
                    html.P("Demand and Economic data:  relating the to the functionality of the generation and distribution systems, a variety of data on technical performance is being collected through remote monitoring of the PV, batteries and inverters, along with measurements and observations of the system collected through scheduled maintenance visits on site."),
                    html.P(""),
                    html.P("Social Impact data:  A Key Performance Indicator framework is being used to track data relating to the impact the microgrid is having on the community, in themes such as health and education, employment and finance, and female empowerment. This data is collected through in person surveys and will be the subject of a separate blog. "),

                html.Div(
                    html.Dialog("This dashboard aims to provide information on a pilot microgrid project in Mthembanji in Malawi. The key data to be displayed through this dashboard is the demand, technical, and social impact data. All of these key parameters provide invaluable information about the functioning of the microgrid along with its long-term feasibility and the direct impact which it has on the inhabitants in Mthembanji."),
                    style={'fontSize':16}),
                html.Br(),
                html.Div(         
                    html.Dialog("The microgrid in Mthembanji was deployed in June of 2020 and is a pilot microgrid in Malawi and, hence, plays a critical role in providing insight and information for future deployments of microgrids in Malawi and other developing countries. This is critically important because, if successful, functionally and financially viable microgrid systems could offer a solution in the drive to provide clean and reliable energy for those in the most remote and underdeveloped areas and help to achieve the UN Sustainable Development Goal 7."),
                    style={'fontSize':16}),
                html.Hr(),
                ]
                
    elif pathname == "/demand":
        return [
                html.Div(
                children = html.H1("Demand Data"),style={'backgroundColor': '#f2f2f2', 'textAlign': 'center'}),
                html.Hr(),
                html.H3("The total revenue generated for the last 30 days is $" + str(round(amountUSD,2))),
                html.Br(),
                dcc.Tabs(id='tabs-example', value='tab-1', children=[
                dcc.Tab(label='Revenue Data', value='tab-1'),
                dcc.Tab(label='Microgrid Load Profiles', value='tab-2'),
                dcc.Tab(label='Peak Load Data', value='tab-3'),
                dcc.Tab(label='Connection Status', value='tab-4'),
                dcc.Tab(label='Individual Customer Data', value='tab-5'),
                dcc.Tab(label='Hourly Usage', value='tab-6'),
                dcc.Tab(label='Monthly Usage', value='tab-7'),
                dcc.Tab(label='Monthly Revenue', value='tab-8'),
                ],),
                html.Div(id='tabs-example-content'),
                ]
    elif pathname == "/technical":
        return [
                html.Div(
                children = html.H1("Technical Data"),style={'backgroundColor': '#f2f2f2', 'textAlign': 'center'}),                          
                html.Hr(),
                html.P("All data is currently being read from SMA Portal's spreadsheets readily available to download from the site, it is uploaded manually via CSV sheets."),
                html.P("Please note that this is only a temporary solution just to showcase what this techincal tab would appear, the team is currently working on implementing the SMA Sunny Portal API for a more reliant way of inputting data."),
                html.Br(),
                html.Hr(),
                dcc.Tabs(id='technical_tabs_1', value='tab-1', children=[
                dcc.Tab(label='Power', value='tab-1'),
                dcc.Tab(label='Consumption', value='tab-2'),
                ],),
                html.Div(id='technical_tabs_1_content'),
                dcc.Tabs(id='technical_tabs_2', value='tab-1', children=[
                dcc.Tab(label='State of Charge', value='tab-1'),
                dcc.Tab(label='Total Generation', value='tab-2'),
                dcc.Tab(label='Potential Energy Yield', value='tab-3'),
                ],),
                html.Div(id='technical_tabs_2_content'),
                ]
    elif pathname == "/social":
        return [
                html.Div(
                children = html.H1("Social Impact Data"),style={'backgroundColor': '#f2f2f2', 'textAlign': 'center'}),
                html.Hr(),
                html.P("Brief description goes here."),
                html.Br(),
                html.Hr(),
                dcc.Tabs(id='social_tabs', value='tab-1', children=[
                dcc.Tab(label='Health and Education', value='tab-1'),
                dcc.Tab(label='Employment and Finance', value='tab-2'),
                dcc.Tab(label='Energy Access', value='tab-3'),
                dcc.Tab(label='Tariff and Service', value='tab-4'),
                dcc.Tab(label='Women Empowerment', value='tab-5'),
                ],),              
                html.Div(id='social_tabs_content'),
                ]
    elif pathname == "/maintenance":
        return [
                html.Div(
                children = html.H1("Maintenance scheduling"),style={'backgroundColor': '#f2f2f2', 'textAlign': 'center'}),
                html.Hr(),
                html.P("Brief description goes here."),
                html.Br(),
                html.Hr(),
                dcc.Tabs(id='maintenance_tabs', value='tab-1', children=[
                dcc.Tab(label='Maintenance', value='tab-1'),
                dcc.Tab(label='Comments', value='tab-2'),
    
                ],),              
                html.Div(id='maintenance_content'),
                ]
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
    
@app.callback(
        Output('technical_tabs_1_content', 'children'),
        Input('technical_tabs_1', 'value'))

def render_tech_tabs_1(tab): # ======================================================================================================================= WIP ======================================================= #
    if tab == 'tab-1':
        return html.Div([
                html.Br(),
                html.Hr(),
                html.H2("Power of PV system"),
                dcc.Graph(id = 'holder_graph_1', figure = power_graph_PV()),
                html.P("This chart displays the current power from the PV (PhotoVoltaic) solar systems."),
                html.P("This is a key data indicator to track as it displays the maximas and minimas of the amount of power from the PV systems, allowing for one to visualize how much stress/load the system is under during peak times (around morning time), also it is interesting to inspect/see that from 23rd to 25th, the graph was display anomalous data, this is due to the fact that storm Ana struck the surrounding areas, hence the data."),
                html.Hr(),
                ])
    elif tab == 'tab-2':
        return html.Div([
                html.Br(),
                html.Hr(),
                html.H2("Total consumption"), # ======================================================================================================================= WIP ======================================================= #
                dcc.Graph(id='holder_graph_1', figure = energy_graph_balance()),
                html.P("This graph shows the total consumption of the solar microgrid as a whole."),
                html.P("This is another key data indicator to track as it shows when the system is being most consumed or when it is at its least used state. Typically trends indicate that the peak usage is around the evening presumably from cooking utilities being under load (social) and steady increase during the mornings. These trends & datacan then be extrapolated into the future to allow for maximum efficient use of the solar microgrid as to when to prioritise output power during peak times or not."),
                html.Hr(),
                ])
        
@app.callback(
        Output('social_tabs_content', 'children'),
        Input('social_tabs', 'value'))

def render_social_tabs(tab):
    if tab == 'tab-1':
        return html.Div([
                html.Br(),
                html.Hr(),
                html.H2("Health and Education Content To Go Here"),
                dcc.Graph(id='holder_graph_1', figure=holder_fig),
                html.Hr(),
                ])
    elif tab == 'tab-2':
        return html.Div([
                html.Br(),
                html.Hr(),
                html.H2("Employment and Finance Content To Go Here"),
                dcc.Graph(id='holder_graph_1', figure=holder_fig),
                html.Hr(),
                ])
    elif tab == 'tab-3':
        return html.Div([
                html.Br(),
                html.Hr(),
                html.H2("Energy Access Content To Go Here"),
                dcc.Graph(id='holder_graph_1', figure=holder_fig),
                html.Hr(),
                ])
    elif tab == 'tab-4':
        return html.Div([
                html.Br(),
                html.Hr(),
                html.H2("Tariff and Service Content To Go Here"),
                dcc.Graph(id='holder_graph_1', figure=holder_fig),
                html.Hr(),
                ])
    elif tab == 'tab-5':
        return html.Div([
                html.Br(),
                html.Hr(),
                html.H2("Women Empowerment Content To Go Here"),
                dcc.Graph(id='holder_graph_1', figure=holder_fig),
                html.Hr(),
                ])
        
@app.callback(
        Output('maintenance_content', 'children'),
        Input('maintenance_tabs', 'value'))

def render_maintenance_tabs(tab):
    if tab == 'tab-1':
        return html.Div([
                html.Br(),
                html.Hr(),
                html.H2("Maintenance content to go here"),
                html.P("This section is currently work in progress."),
                # Stuff to go here
                html.Hr(),
                ])
    elif tab == 'tab-2':
        return html.Div([
                html.Br(),
                html.Hr(),
                html.H2("Any additional remarks/comment to go here"),
                html.P("This section is currently work in progress."),
                # Stuff to go here
                html.Hr(),
                ])
@app.callback(
        Output('technical_tabs_2_content', 'children'),
        Input('technical_tabs_2', 'value'))

def render_tech_tabs_2(tab):
    if tab == 'tab-1':
        return html.Div([ 
                html.Br(),
                html.Hr(),
                html.H2("State of Charge (energy balance)"), # ======================================================================================================================= WIP ======================================================= #
                dcc.Graph(id='my_graph_4', figure=energy_graph_batterystatecharge()),
                html.P("This chart displays the current state of charge of the batteries."),
                html.P("This is another key data indicator to track as it allows for one to come to conclusions regarding when the charge of the batteries are charged, or depleted. Again, note the anomolous data display between 23rd to 25th. All data thus far is drawn from an Excel sheet locally from the past week, note that this is a temporary solution for the time being while the current development team is working on the SMA Sunny Portal API."),
                html.Hr(),
                ])
    elif tab == 'tab-2':
        return html.Div([
                html.Br(),
                html.Hr(),
                html.H2("Generation"), # ======================================================================================================================= WIP ======================================================= #
                dcc.Graph(id='my_graph_6', figure=energy_graph_totalgen()),
                html.P("This chart displays the total generation (energy balance)."),
                html.P("This key data indicator shows when the system is generating most power, and the least power respectively. As indicitive of this graph, it would suggest the peak generation is around the early mornings of 9am, before levelling off during the day."),
                ])
    elif tab == 'tab-3':
        return html.Div([
                html.Br(),
                html.Hr(),
                html.H2("Potential Energy Yield Graph To Go Here"), # ======================================================================================================================= WIP ======================================================= #
                dcc.Graph(id='holder_graph_1', figure=holder_fig),
                html.Hr(),
                ])
  
@app.callback(
        Output('tabs-example-content', 'children'),
        Input('tabs-example', 'value'))

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Br(),
            html.Hr(),
            html.H2("Monthly Revenue for Given Year"),
            html.H4("Please select a year from the dropdown: "), # New quality of life improvements
    
            dcc.Dropdown(id="slct_year",
                     options=[
                         {"label": "2020", "value": "2020"},
                         {"label": "2021", "value": "2021"},
                         {"label": "2022", "value": "2022"},
                         ],
                     placeholder="Select a year",
                     searchable = False,
                     multi=False,
                     value=C_year,
                     style={'width': "40%"}
                     ),
            html.Br(),
            html.Div([
            dcc.RadioItems(id = 'TorA',
                options=[
                    {'label': 'Total Revenue', 'value': 1},
                    {'label': 'ARPU', 'value': 60}
                ],
                value=1,
                inputStyle={"margin-left": "15px", "margin-right":"5px"}
            ),]),
            dcc.Graph(id='my_graph', figure={}),
            html.P("This bar chart displays either the total monthly revenue generated across a given year or the ARPU (average revenue per user) across a given year."),
            html.P("This is useful data to analyse as it provides information of how much monthly revenue the microgrid generated throughout the year or how much revenue the average customer generated. This data could be useful for developing a business plan as it enables evaluation of how much revenue the microgrid generates and how much an average customer generates. This format is also particularly useful as it enables easy visual analysis of how the total monthly revenue and ARPU vary month to month or seasonally throughout a given year, hence enabling trends to be established and analysed."),
            html.Br(),
            html.Hr(),
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Br(),
            html.Hr(),
            html.H2("Microgrid Load Profile for Given Day"),
            html.H4("Please select a date: "),
            
            dcc.DatePickerSingle(
                id='my-date-picker-single',
                min_date_allowed=date(2020, 6, 5),
                max_date_allowed=date(C_year, C_month, C_day),
                initial_visible_month=date(C_year, C_month, C_day),
                date=date(C_year, C_month, C_day) # Changed so it selects current day, previously it was set to June the 5th 2020
                # more user friendly
            ),
            html.Br(),
            html.Br(),
            dcc.RadioItems(id = 'TorU_1',
                options=[
                    {'label': 'Total    ', 'value': 1},
                    {'label': 'User', 'value': 60},
                ],
                value=1,
                inputStyle={"margin-left": "15px", "margin-right":"5px"}
            ),
            dcc.Graph(id = 'my_graph_2', figure = {}),   
            html.Br(),
            html.P("This chart displays the hourly usage of the entire microgrid or the hourly usage for the average customer on a given day."),
            html.P("This is useful in order to analyse how much power the system used in hourly intervals throughout a particular day for both the entire microgrid and for the average customer connected to the microgrid. This is also a beneficial format as it gives a more wholistic view of the entire system. This may be useful to analyse the impact of a particular event (e.g., a storm) on the entire system as we can zone in on any given day. It is also effective to see the total load of the system and, hence, may be useful to compare with battery charge state and other technical data."),
            html.Br(),
            html.Hr(),
            
            html.H2("Microgrid Load Profile for Given Month"),
            html.H4("Please input the month which you would like to view (YYYY-MM): "),
            dcc.Input(id="av_load_date_IP", type="text", value=currentYYMM, placeholder="YYYY-MM", debounce=True,style={'fontSize':16}),
            html.Br(),
            html.Br(),
            dcc.RadioItems(id = 'TorU',
                options=[
                    {'label': 'Total    ', 'value': 1},
                    {'label': 'User', 'value': 60},
                ],
                value=1,
                inputStyle={"margin-left": "15px", "margin-right":"5px"}
            ),
            dcc.Graph(id = 'my_av_load_graph', figure={}),
            html.Br(),
            html.P("This chart displays the average daily usage in hourly intervals for the entire microgrid or for the average customer. It does this by retrieving the data for each hour of each day of that given month. It then adds the usage amount for each hour for each day together (e.g., adds all the usage amount for 1AM for each day of the month together) and then divides that usage amount by the number of days in the month (this takes different months having different numbers of days and leap years into account and also takes into account whether or not there is a complete months’ worth of data – for example, if it is only the 15th of a month and that month and year is inputted, then the code will divide the usage amount by 15 not the full month worth of days). It does this for each hour and then displays the hourly data as shown below. For the average customer version, it then divides each point by the number of customers."),
            html.P("This is useful in order to analyse how much power the system used on average throughout the given month and what the microgrid’s load profile looked like for that month and what the average customer’s load profile looked like for that given month. This may also be useful for generating a business plan and also comparing monthly or seasonally to analyse whether or not the changing months or seasons has an impact on the average usage of the microgrid."),
            html.Br(),
            html.Hr(),
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.Br(),
            html.Hr(),
            html.H2("Peak Loads for Given Month"),
            html.H4("Please input the month which you would like to view (YYYY-MM): "),     
            dcc.Input(id="peak_date_IP", type="text", value=currentYYMM, placeholder="YYYY-MM", debounce=True,style={'fontSize':16}), 
            dcc.Graph(id = 'my_peak_graph', figure={}),
            html.P("This chart displays the daily peak loads for the whole system throughout a given month."),
            html.P("This is useful data in order to analyse what the daily peak load of the whole microgrid is each day. This enables easy analysis of how much the peak load amount varies throughout the given month. This could be useful for analysing the impact of an event (e.g., a storm) by observing how the daily peak load varies on the days of and around the event. Furthermore, this data could be useful for comparing with technical data in order to ensure the microgrid is able to supply the peak load of the system throughout the month. This data could also be useful to compare month to month or seasonally to see if the changing months or seasons has an impact on the peak loads of the system throughout the month."),
            html.Br(),
            html.Hr(),
        ])
    elif tab == 'tab-4':
            numOn = 0
            numOff = 0
            

            #grabbing the connection status data from the url
            url = "https://api.steama.co/customers/?fields=status,foo/?page=1&page_size=100"
            
            r = requests.get(url=url, headers = header)
            s = r.content
            #converting json string to a panda object
            dfC = pd.read_json(s)
            
            #in the range of 0 and the no of customers (items) in the object
            for index in range(0,len(dfC['count'])):
                holder = dfC['results'][index]
            #if the connection is on, add one to the on  counter
                if(holder['status'] == "on"):
                    numOn += 1
            #if the connection status if off, add one to the counter
                elif(holder['status'] == "off"):
                    numOff += 1
                elif(holder['status'] == "none"):
                    continue
                
            status = ['On', 'Off'] 
            data = [numOn, numOff]
            
            fig = px.pie(values=data, names=status)
            return html.Div([
                    html.Br(),
                    html.Hr(),
                    html.H2('Current Connection Status'),
                    dcc.Graph(id="pie-chart", figure = fig),
                    html.P("This pie chart displays the current percentage of customers who have an active connection (ON) or have their connection disabled (OFF)."),
                    html.P("This is useful data to have as it enables easy establishment of the percentage of customers who are actually using their connection at this given moment and hence, provides some insight into how useful the microgrid is and what percentage of customers are actually using it."),
                    html.Br(),
                    html.Hr(),
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.Br(),
            html.Hr(),
            html.H2("Customer Usage for a Given Day"),
            html.H4("Please select a customer from the dropdown: "),
            dcc.Dropdown(id="slct_customer",
                     options=[
                         {"label": "Zacharia Alfred", "value": "Zacharia Alfred"},
                         {"label": "Dalitso Bizweck", "value": "Dalitso Bizweck"},
                         {"label": "Bizzy Bizzy", "value": "Bizzy Bizzy"},
                         {"label": "Zipi Chadinga", "value": "Zipi Chadinga"},
                         {"label": "Clodio Chagona", "value": "Clodio Chagona"},
                         {"label": "Stephano Chagona", "value": "Stephano Chagona"},
                         {"label": "Matilda Chagontha", "value": "Matilda Chagontha"},
                         {"label": "Sainet Chemtila", "value": "Sainet Chemtila"},
                         {"label": "Layton Chidavu", "value": "Layton Chidavu"},
                         {"label": "Lucia Chikapa", "value": "Lucia Chikapa"},
                         {"label": "St John's Cathoric church", "value": "St John's Cathoric church"},
                         {"label": "Seba Eliko", "value": "Seba Eliko"},
                         {"label": "Vester Everson", "value": "Vester Everson"},
                         {"label": "Agatha Evesi", "value": "Agatha Evesi"},
                         {"label": "Wisdory Freizer", "value": "Wisdory Freizer"},
                         {"label": "Lameck Galion", "value": "Lameck Galion"},
                         {"label": "George Gilibati", "value": "George Gilibati"},
                         {"label": "Daudi Gondwa", "value": "Daudi Gondwa"},
                         {"label": "Eliko Gonthi", "value": "Eliko Gonthi"},
                         {"label": "Robert Gwafali", "value": "Robert Gwafali"},
                         {"label": "Chrisy Helemesi", "value": "Chrisy Helemesi"},
                         {"label": "Fedrick Jumbe", "value": "Fedrick Jumbe"},
                         {"label": "Jovelo Justin", "value": "Jovelo Justin"},
                         {"label": "Flescot R Kalambo", "value": "Flescot R Kalambo"},
                         {"label": "Davie Kamayaya", "value": "Davie Kamayaya"},
                         {"label": "James Kamkwamba", "value": "James Kamkwamba"},
                         {"label": "Stampa Kamkwamba", "value": "Stampa Kamkwamba"},
                         {"label": "Alex Kapingasa", "value": "Alex Kapingasa"},
                         {"label": "Yohane Lipenga", "value": "Yohane Lipenga"},
                         {"label": "Zakeyo Lipenga", "value": "Zakeyo Lipenga"},
                         {"label": "Kelita Luciano", "value": "Kelita Luciano"},
                         {"label": "Lameck Luka", "value": "Lameck Luka"},
                         {"label": "Richard Lyton", "value": "Richard Lyton"},
                         {"label": "Lameki Malota", "value": "Lameki Malota"},
                         {"label": "Noel Malota", "value": "Noel Malota"},
                         {"label": "Deborah Mangochi", "value": "Deborah Mangochi"},
                         {"label": "Sedonia Mangochi", "value": "Sedonia Mangochi"},
                         {"label": "Elenata Mike", "value": "Elenata Mike"},
                         {"label": "Agatha Miliano", "value": "Agatha Miliano"},
                         {"label": "Evinesi Miliano", "value": "Evinesi Miliano"},
                         {"label": "Chinasi Mofati", "value": "Chinasi Mofati"},
                         {"label": "Conrad Mpeketula", "value": "Conrad Mpeketula"},
                         {"label": "Alick Mphemvu", "value": "Alick Mphemvu"},
                         {"label": "Linda Msowa", "value": "Linda Msowa"},
                         {"label": "Maliko Mulanje", "value": "Maliko Mulanje"},
                         {"label": "Gibson Mvula", "value": "Gibson Mvula"},
                         {"label": "Aujenia Nicolus", "value": "Aujenia Nicolus"},
                         {"label": "Peter Justin Nyale", "value": "Peter Justin Nyale"},
                         {"label": "Bizweck Record", "value": "Bizweck Record"},
                         {"label": "Ntandamula primary school", "value": "Ntandamula primary school"},
                         {"label": "Lewis Semiyano", "value": "Lewis Semiyano"},
                         {"label": "Bizweck Shalifu", "value": "Bizweck Shalifu"},
                         {"label": "Rodreck Sipiliano", "value": "Rodreck Sipiliano"},
                         {"label": "Kinlos Spiliano", "value": "Kinlos Spiliano"},
                         {"label": "Nickson Spiliano", "value": "Nickson Spiliano"},
                         {"label": "Tobias Spiliano", "value": "Tobias Spiliano"},
                         {"label": "Patrick Sugar", "value": "Patrick Sugar"},
                         {"label": "Stephano Tobias", "value": "Stephano Tobias"},
                         {"label": "Luciano Veleliyano", "value": "Luciano Veleliyano"},
                         {"label": "Konoliyo Zipi", "value": "Konoliyo Zipi"},
                         ],    
                     placeholder="Select a customer",
                     searchable = False,
                     clearable=False,
                     multi=False,
                     value="Zacharia Alfred",
                     style={'width': "60%"}
                     ),
            html.Br(),
            html.H4("Please select a date: "),
            dcc.DatePickerSingle(
                id='my-date-picker-single_2',
                min_date_allowed=date(2020, 6, 5),
                max_date_allowed=date(C_year, C_month, C_day),
                initial_visible_month=date(C_year, C_month, C_day),
                date=date(C_year, C_month, C_day)
            ),
            dcc.Graph(id = 'cust_on_day_graph', figure={}),
            html.Br(),
            html.P("This chart displays the hourly usage of a single customer on a given day."),
            html.P("This is useful to analyse what any customer has used throughout a particular day and may be useful to analyse the impact of a particular event (e.g., a storm) on a customer’s usage as it is possible to zone in on any given day."),
            html.Br(),
            html.Hr(),
            
            html.H2("Customer’s Average Daily Usage for Given Month"),
            html.H4("Please select a customer from the dropdown: "),
            dcc.Dropdown(id="slct_customer_2",
                     options=[
                         {"label": "Zacharia Alfred", "value": "Zacharia Alfred"},
                         {"label": "Dalitso Bizweck", "value": "Dalitso Bizweck"},
                         {"label": "Bizzy Bizzy", "value": "Bizzy Bizzy"},
                         {"label": "Zipi Chadinga", "value": "Zipi Chadinga"},
                         {"label": "Clodio Chagona", "value": "Clodio Chagona"},
                         {"label": "Stephano Chagona", "value": "Stephano Chagona"},
                         {"label": "Matilda Chagontha", "value": "Matilda Chagontha"},
                         {"label": "Sainet Chemtila", "value": "Sainet Chemtila"},
                         {"label": "Layton Chidavu", "value": "Layton Chidavu"},
                         {"label": "Lucia Chikapa", "value": "Lucia Chikapa"},
                         {"label": "St John's Cathoric church", "value": "St John's Cathoric church"},
                         {"label": "Seba Eliko", "value": "Seba Eliko"},
                         {"label": "Vester Everson", "value": "Vester Everson"},
                         {"label": "Agatha Evesi", "value": "Agatha Evesi"},
                         {"label": "Wisdory Freizer", "value": "Wisdory Freizer"},
                         {"label": "Lameck Galion", "value": "Lameck Galion"},
                         {"label": "George Gilibati", "value": "George Gilibati"},
                         {"label": "Daudi Gondwa", "value": "Daudi Gondwa"},
                         {"label": "Eliko Gonthi", "value": "Eliko Gonthi"},
                         {"label": "Robert Gwafali", "value": "Robert Gwafali"},
                         {"label": "Chrisy Helemesi", "value": "Chrisy Helemesi"},
                         {"label": "Fedrick Jumbe", "value": "Fedrick Jumbe"},
                         {"label": "Jovelo Justin", "value": "Jovelo Justin"},
                         {"label": "Flescot R Kalambo", "value": "Flescot R Kalambo"},
                         {"label": "Davie Kamayaya", "value": "Davie Kamayaya"},
                         {"label": "James Kamkwamba", "value": "James Kamkwamba"},
                         {"label": "Stampa Kamkwamba", "value": "Stampa Kamkwamba"},
                         {"label": "Alex Kapingasa", "value": "Alex Kapingasa"},
                         {"label": "Yohane Lipenga", "value": "Yohane Lipenga"},
                         {"label": "Zakeyo Lipenga", "value": "Zakeyo Lipenga"},
                         {"label": "Kelita Luciano", "value": "Kelita Luciano"},
                         {"label": "Lameck Luka", "value": "Lameck Luka"},
                         {"label": "Richard Lyton", "value": "Richard Lyton"},
                         {"label": "Lameki Malota", "value": "Lameki Malota"},
                         {"label": "Noel Malota", "value": "Noel Malota"},
                         {"label": "Deborah Mangochi", "value": "Deborah Mangochi"},
                         {"label": "Sedonia Mangochi", "value": "Sedonia Mangochi"},
                         {"label": "Elenata Mike", "value": "Elenata Mike"},
                         {"label": "Agatha Miliano", "value": "Agatha Miliano"},
                         {"label": "Evinesi Miliano", "value": "Evinesi Miliano"},
                         {"label": "Chinasi Mofati", "value": "Chinasi Mofati"},
                         {"label": "Conrad Mpeketula", "value": "Conrad Mpeketula"},
                         {"label": "Alick Mphemvu", "value": "Alick Mphemvu"},
                         {"label": "Linda Msowa", "value": "Linda Msowa"},
                         {"label": "Maliko Mulanje", "value": "Maliko Mulanje"},
                         {"label": "Gibson Mvula", "value": "Gibson Mvula"},
                         {"label": "Aujenia Nicolus", "value": "Aujenia Nicolus"},
                         {"label": "Peter Justin Nyale", "value": "Peter Justin Nyale"},
                         {"label": "Bizweck Record", "value": "Bizweck Record"},
                         {"label": "Ntandamula primary school", "value": "Ntandamula primary school"},
                         {"label": "Lewis Semiyano", "value": "Lewis Semiyano"},
                         {"label": "Bizweck Shalifu", "value": "Bizweck Shalifu"},
                         {"label": "Rodreck Sipiliano", "value": "Rodreck Sipiliano"},
                         {"label": "Kinlos Spiliano", "value": "Kinlos Spiliano"},
                         {"label": "Nickson Spiliano", "value": "Nickson Spiliano"},
                         {"label": "Tobias Spiliano", "value": "Tobias Spiliano"},
                         {"label": "Patrick Sugar", "value": "Patrick Sugar"},
                         {"label": "Stephano Tobias", "value": "Stephano Tobias"},
                         {"label": "Luciano Veleliyano", "value": "Luciano Veleliyano"},
                         {"label": "Konoliyo Zipi", "value": "Konoliyo Zipi"},
                         ],  
                     placeholder="Select a customer",
                     searchable = False,
                     clearable=False,
                     multi=False,
                     value="Zacharia Alfred",
                     style={'width': "60%"}
                     ),
            html.Br(),
            html.H4("Please input the month which you would like to view (YYYY-MM): "),
            dcc.Input(id='cus_av_month_usage_date_IP', type="text", value=currentYYMM, placeholder="YYYY-MM", debounce=True,style={'fontSize':16}),
            dcc.Graph(id = 'cust_month_average_graph', figure={}),    
            html.Br(),
            html.P("This chart displays the average daily usage of a single given customer over a given month. It does this by retrieving the data for each hour of each day of that given month. It then adds the usage amount for each hour for each day together (e.g., adds all the usage amount for 1AM for each day of the month together) and then divides that usage amount by the number of days in the month (this has been coded to take different months having different numbers of days and leap years into account). It does this for each hour and then displays the hourly data."),
            html.P("This is useful in order to analyse what any customer’s average daily usage looked like for a given month, hence, enabling the determination of usage patterns and trends and enabling the comparison of month-to-month data to see if there are any significant changes (possibly resulting from changing seasons)."),
            html.Br(),
            html.Hr(),
        ])

          

          
    elif tab == 'tab-6':
        return html.Div([
            html.Br(),
            html.Hr(),
            html.H2("Usage by User Category"),
            html.P("Long loading times, please wait about 40 seconds for the data to appear."),
            html.H4("Please select a date: "),
            
            dcc.DatePickerSingle(
                id='my-date-picker-single',
                min_date_allowed=date(2020, 6, 5),
                max_date_allowed=date(C_year, C_month, C_day),
                initial_visible_month=date(C_year, C_month, C_day),
                date=date(C_year, C_month, C_day)
            ),
            html.Br(),
            html.Br(),
            dcc.RadioItems(id = 'TorU_2',
                options=[
                    {'label': 'Residential', 'value': 1},
                    {'label': 'Business', 'value': 2},
                    {'label': 'Institution', 'value': 3},
                ],
                value=1,
                inputStyle={"margin-left": "15px", "margin-right":"5px"}
            ),
            dcc.Graph(id = 'my_graph_3', figure = {}),   
            html.Br(),
            html.P("This chart displays the hourly usage of the entire microgrid or the hourly usage for the average customer on a given day."),
            html.P("It is similar to the one on tab 2 however, also gives you a chance to view usage data seperately for each user category"),
            html.Br(),
            html.Hr(),
            
            
        ])
    
    elif tab == 'tab-7':
        return html.Div([
            html.Br(),
            html.Hr(),
            html.H2("Usage by User Category"),
            html.P("Long loading times, please wait about 40 seconds for the data to appear."),
            html.H4("Please select a year: "),
            html.Br(),
            html.Br(),
            dcc.Dropdown(id="slct_year",
                     options=[
                         {"label": "2020", "value": "2020"},
                         {"label": "2021", "value": "2021"},
                         {"label": "2022", "value": "2022"}],
                     placeholder="Select a year",
                     searchable = False,
                     multi=False,
                     value=C_year,
                     style={'width': "40%"}
                     ),
            dcc.RadioItems(id = 'TorU_2',
                options=[
                    {'label': 'Residential', 'value': 1},
                    {'label': 'Business', 'value': 2},
                    {'label': 'Institution', 'value': 3},
                ],
                value=1,
                inputStyle={"margin-left": "15px", "margin-right":"5px"}
            ),
            dcc.RadioItems(id = 'TorU_3',
                options=[
                    {'label': 'Total', 'value': 1},
                    {'label': 'Average', 'value': 2},
                ],
                value=1,
                inputStyle={"margin-left": "15px", "margin-right":"5px"}
            ),
            dcc.Graph(id = 'my_graph_4', figure = {}),   
            html.Br(),
            html.P("This chart is used to display the total monthly usage of the selected user ccategory "),
            html.P("The data is displayed and has monthly intervals over the selected year"),
            html.Br(),
            html.Hr(),
            
            
        ])
    
    
    
    elif tab == 'tab-8':
        return html.Div([
            html.Br(),
            html.Hr(),
            html.H2("Revenue by User Category"),
            html.P("Long loading times, please wait about 40 seconds for the data to appear."),
            html.H4("Please select a year: "),
            html.Br(),
            html.Br(),
            dcc.Dropdown(id="slct_year",
                     options=[
                         {"label": "2020", "value": "2020"},
                         {"label": "2021", "value": "2021"},
                         {"label": "2022", "value": "2022"}],
                     placeholder="Select a year",
                     searchable = False,
                     multi=False,
                     value=C_year,
                     style={'width': "40%"}
                     ),
            dcc.RadioItems(id = 'TorU_2',
                options=[
                    {'label': 'Residential', 'value': 1},
                    {'label': 'Business', 'value': 2},
                    {'label': 'Institution', 'value': 3},
                ],
                value=1,
                inputStyle={"margin-left": "15px", "margin-right":"5px"}
            ),
            dcc.RadioItems(id = 'TorU_3',
                options=[
                    {'label': 'Total', 'value': 1},
                    {'label': 'Average', 'value': 2},
                ],
                value=1,
                inputStyle={"margin-left": "15px", "margin-right":"5px"}
            ),
            dcc.Graph(id = 'my_graph_5', figure = {}),   
            html.Br(),
            html.P("This chart is used to display the total monthly revenue of the selected user category "),
            html.P("The data is displayed and has monthly intervals over the selected year"),
            html.Br(),
            html.Hr(),
            
            
        ])

         
@app.callback(
    Output(component_id='cust_month_average_graph', component_property='figure'),
    [Input(component_id='cus_av_month_usage_date_IP', component_property='value'),
     Input('slct_customer_2', 'value')])

def update_cust_month_average_graph(date_value, cust_name):
    string = str(cust_name)
    words = string.split()
    surname = words[-1]
    holder = words[0:-1]
    first_name = words[0]
    #first_name = ""
    #for index in range(0, len(holder)):
    #    if(index==0):
    #        first_name += str(holder[index])
    #    else:
    #        first_name += " " + str(holder[index])
    date = str(date_value)
    month = str(date[5:7])
    
    if(month == "01"):
        M = "January"
    elif(month == "02"):
        M = "February"
    elif(month == "03"):
        M = "March"
    elif(month == "04"):
        M = "April"
    elif(month == "05"):
        M = "May"
    elif(month == "06"):
        M = "June"
    elif(month == "07"):
        M = "July"
    elif(month == "08"):
        M = "August"
    elif(month == "09"):
        M = "September"
    elif(month == "10"):
        M = "October"
    elif(month == "11"):
        M = "November"
    else:
        M = "December"
        
    if(len(date)!=7):   #These lines of code are just used in case of an invalid date input from the user
        y_dont_care = [] #If the date input size is not 7, it is in valid as YYYY-MM has 7 characters
        x_dont_care = []
        for index in range(1,24):
            y_dont_care.append(0)
            x_dont_care.append(index)
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_dont_care, y=y_dont_care,
                            mode='lines+markers',
                            ))
        
        fig.update_layout(title = "Invalid Input",
                       xaxis_title='Time',
                       yaxis_title='Usage Amount (kWh)')  
        return fig
    
    else:
    
        url = "https://api.steama.co/customers/?last_name=" + surname + "&first_name=" + first_name
    
        r = requests.get(url=url, headers = header)
        s = r.content
        df = pd.read_json(s)
        holder = df['results'][0]
        
        usage_url = holder['utilities_url'] + "1/usage/"
        
        start_time = str(date) + "-01T00:00:00"
        
        if(int(date[5:7])==12):
            if(int(date[0:4])<10):
                end_time = str(date[0:3]) + str(int(date[3])+1) + "-01-01T00:00:00"
            else:
                end_time = str(date[0:2]) + str(int(date[2:4])+1) + "-01-01T00:00:00"
        else:
            if(int(date[5:7])<10):
                end_time = str(date[0:6]) + str(int(date[6])+1) + "-01T00:00:00"
            else:
                end_time = str(date[0:5]) + str(int(date[5:7])+1) + "-01T00:00:00"
                      
        url2 = usage_url + "?start_time=" + start_time + "&end_time=" + end_time
        
        r2 = requests.get(url=url2, headers = header)
        s2 = r2.content
        df2 = pd.read_json(s2)
        
        if(len(df2))==0:
            x_dont_care = []
            y_dont_care = []
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_dont_care, y=y_dont_care,
                                    mode='lines+markers',
                                    ))
            fig.update_layout(title = "There are no meter readings for " + first_name + " " + surname + " for " + M + " " + str(date[0:4]),
                              )
            return fig
    
        else:
            timestamp = []
            usage_amount = []
            time = []
            usage = []
                
            if(month == "04" or month == "06" or month == "09" or month == "11"):
                num = 30
            elif(month == "02" and int(date[0:4])%4==0):
                num = 29
            elif(month == "02" and int(date[0:4])%4!=0):
                num = 28
            else:
                num = 31
            
            for index in range(0,len(df2['timestamp'])):
                timestamp.append(str(df2['timestamp'][index]))
                usage_amount.append(df2['usage'][index])
                    
            for index in range(0,24):
                if(index<10):
                    a = "0" + str(index)
                else:
                    a = str(index)
                temp = a + ":00:00+00:00"
                #temp = str(a[0]) + str(a[1]) + ":00:00+00:00"
                amount = 0
                temptime = str(a[0]) + str(a[1]) + ":00:00"
                for count in range(0,len(timestamp)):
                    holder = timestamp[count]
                    if(temp == holder[11:26]):
                        amount += float(usage_amount[count])
                        continue
                    else:
                        continue
                usage.append(amount/num)
                time.append(temptime)
                
            fig = go.Figure()
    
            fig.add_trace(go.Scatter(x=time, y=usage,
                                    mode='lines+markers',
                                    ))
                
            fig.update_layout(title = first_name + " " + surname + " Average Daily Load Profile Usage for " + M + " " + str(date[0:4]),
                               xaxis_title='Time',
                               yaxis_title='Usage Amount (kWh)',
                               yaxis_range=[-0.01,max(usage)+0.01])
            
            fig.update_xaxes(
                tickangle = 45)
            
            return fig
            
@app.callback(
    Output(component_id='cust_on_day_graph', component_property='figure'),
    [Input(component_id='my-date-picker-single_2', component_property='date'),
     Input('slct_customer', 'value')])

def update_cust_on_day_graph(date_value, cust_name): 
    
    string = str(cust_name) #These lines are used to split the customers name into first and surname
    words = string.split() #They need to be split so that the url will change based on what customer has been selected by the user
    surname = words[-1]
    holder = words[0:-1]
    first_name = ""
    for index in range(0, len(holder)):
        if(index==0):
            first_name += str(holder[index])
        else:
            first_name += " " + str(holder[index])
    date = date_value

    url = "https://api.steama.co/customers/?last_name=" + surname + "&first_name=" + first_name
    
    r = requests.get(url=url, headers = header)
    s = r.content
    df = pd.read_json(s)
    holder = df['results'][0]
    
    usage_url = holder['utilities_url'] + "1/usage/"
    
    start_time = date + "T00:00:00"
    
    if((int(date[5:7])==1 or int(date[5:7])==3 or int(date[5:7])==5 or int(date[5:7])==7 or
        int(date[5:7])==8 or int(date[5:7])==10) and int(date[8:10])==31):
        if(int(date[5:7])<9):
                end_time = date[0:6] + str(int(date[6])+1) + "-01T00:00:00"
        else:
                end_time = date[0:5] + str(int(date[5:7])+1) + "-01T00:00:00"
    elif((int(date[5:7])==4 or int(date[5:7])==6 or int(date[5:7])==9 or int(date[5:7])==11) and int(date[8:10])==30):    
        if(int(date[5:7])<9):
                end_time = date[0:6] + str(int(date[6])+1) + "-01T00:00:00"
        else:
                end_time = date[0:5] + str(int(date[5:7])+1) + "-01T00:00:00"
    elif(int(date[0:4])%4==0 and int(date[5:7])==2 and int(date[8:10])==29):
        end_time = date[0:6] + str(int(date[6])+1) + "-01T00:00:00"
    elif(int(date[0:4])%4!=0 and int(date[5:7])==2 and int(date[8:10])==28):
        end_time = date[0:6] + str(int(date[6])+1) + "-01T00:00:00"
    elif(int(date[5:7])==12 and int(date[8:10])==31):
        end_time = str(int(date[0:4])+1) + "-01-01T00:00:00"
    else:
        if(int(date[8:10])<9):
                end_time = date[0:9] + str(int(date[9])+1) + "T00:00:00"
        else:
                end_time = date[0:8] + str(int(date[8:10])+1) + "T00:00:00"
                  
    url2 = usage_url + "?start_time=" + start_time + "&end_time=" + end_time
    
    r2 = requests.get(url=url2, headers = header)
    s2 = r2.content
    df2 = pd.read_json(s2)
    
    timestamp = []
    usage_amount = []
    time = []
    
    if(len(df2)==0):
        x_dont_care = []
        y_dont_care = []
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_dont_care, y=y_dont_care,
                                mode='lines+markers',
                                ))
        fig.update_layout(title = "There are no meter readings for " + first_name + " " + surname + " on " + str(date),
                          )
        return fig
    else:
        for index in range(0,len(df2['timestamp'])):
            timestamp.append(str(df2['timestamp'][index]))
            usage_amount.append(df2['usage'][index])
            
        for index in range(0,len(timestamp)):
            temp = timestamp[index]
            time.append(temp[11:19])
        
        
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=time, y=usage_amount,
                            mode='lines+markers',
                            ))
        
    fig.update_layout(title = first_name + " " + surname + " Usage on " + date,
                       xaxis_title='Time',
                       yaxis_title='Usage Amount (kWh)',
                       yaxis_range=[-0.01,max(usage_amount)+0.01])
    
    fig.update_xaxes(
        tickangle = 45)
    
    return fig
    
@app.callback(
    Output(component_id='my_av_load_graph', component_property='figure'),
    [Input(component_id="av_load_date_IP", component_property='value'),
     Input('TorU','value')])

def update_av_load_graph(IP, bttn1):
    date = str(IP)
    month = str(date[5:7])
    div = bttn1
    
    if(div==1):
        T = "Total Microgrid "
    else:
        T = "Average User "
    
    if(month == "01"):
        M = "January"
    elif(month == "02"):
        M = "February"
    elif(month == "03"):
        M = "March"
    elif(month == "04"):
        M = "April"
    elif(month == "05"):
        M = "May"
    elif(month == "06"):
        M = "June"
    elif(month == "07"):
        M = "July"
    elif(month == "08"):
        M = "August"
    elif(month == "09"):
        M = "September"
    elif(month == "10"):
        M = "October"
    elif(month == "11"):
        M = "November"
    else:
        M = "December"
        
    if(len(date))!=7:
        y_dont_care = []
        x_dont_care = []
        for index in range(1,24):
            y_dont_care.append(0)
            x_dont_care.append(index)
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_dont_care, y=y_dont_care,
                            mode='lines+markers',
                            ))
        
        fig.update_layout(title = "Invalid Input",
                       xaxis_title='Time',
                       yaxis_title='Usage Amount (kWh)')  
        return fig
    
    else:
        start_time = str(date) + "-01T00:00:00"
        
        if(int(date[5:7])==12):
            end_time = str(int(date[0:4])+1) + "-01-01T00:00:00"
        else:
            if(int(date[5:7])<9):
                end_time = str(date[0:6]) + str(int(date[6])+1) + "-01T00:00:00"
            else:
                end_time = str(date[0:5]) + str(int(date[5:7])+1) + "-01T00:00:00"
                         
        url = "https://api.steama.co/sites/26385/utilities/1/usage/?start_time=" + start_time + "&end_time=" + end_time
        
        r = requests.get(url=url, headers = header)
        s = r.content
        df = pd.read_json(s)
        
        if(len(df))==0:
            y_dont_care = []
            x_dont_care = []
            for index in range(1,24):
                y_dont_care.append(0)
                x_dont_care.append(index)
                
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_dont_care, y=y_dont_care,
                                mode='lines+markers',
                                ))
            
            fig.update_layout(title = T + "Load Profile for " + M + " " + date[0:4],
                           xaxis_title='Time',
                           yaxis_title='Usage Amount (kWh)')  
            return fig
        
        else:
            timestamp = []
            usage_amount = []
            time = []
            usage = []
                
            if(month == "04" or month == "06" or month == "09" or month == "11"):
                num = 30
            elif(month == "02" and int(date[0:4])%4==0):
                num = 29
            elif(month == "02" and int(date[0:4])%4!=0):
                num = 28
            else:
                num = 31
            
            for index in range(0,len(df['timestamp'])):
                timestamp.append(str(df['timestamp'][index]))
                usage_amount.append(df['usage'][index])
                
            add = 0
            
            for i in range(1,num+1):
                for index in range(0,len(timestamp)):
                    hold = timestamp[index]
                    if(int(hold[8:10])==i):
                        add+=1
                        break
                    else:
                        continue
                                
            for index in range(0,24):
                if(index<10):
                    a = "0" + str(index)
                else:
                    a = str(index)
                temp = a + ":00:00+00:00"
                amount = 0
                for count in range(0,len(timestamp)):
                    holder = timestamp[count]
                    if(temp == holder[11:26]):
                        amount += float(usage_amount[count])
                        continue
                    else:
                        continue
                usage.append((amount/add)/div)
                time.append(temp[0:8])
                
            fig = go.Figure()
    
            fig.add_trace(go.Scatter(x=time, y=usage,
                                mode='lines+markers',
                                ))
            
            fig.update_layout(title = T + "Load Profile for " + M + " " + date[0:4],
                           xaxis_title='Time',
                           yaxis_title='Usage Amount (kWh)',
                           yaxis_range=[-0.02,max(usage)+0.02])
            
            return fig
            
@app.callback(
    Output(component_id='my_peak_graph', component_property='figure'),
    Input(component_id="peak_date_IP", component_property='value'),
)

def update_peak_graph(IP):
    
    date = str(IP)
    month = date[5:7]
    
    start_time = str(date) + "-01T00:00:00"
    
    if(len(date))!=7:
        y_dont_care = []
        x_dont_care = []
        for index in range(1,24):
            y_dont_care.append(0)
            x_dont_care.append(index)
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_dont_care, y=y_dont_care,
                            mode='lines+markers',
                            ))
        
        fig.update_layout(title = "Invalid Input",
                       xaxis_title='Time',
                       yaxis_title='Usage Amount (kWh)')  
        return fig
    
    else:
    
        if(int(date[5:7])==12):
            end_time = str(int(date[0:4])+1) + "-01-01T00:00:00"
        else:
            if(int(date[5:7])<9):
                end_time = str(date[0:6]) + str(int(date[6])+1) + "-01T00:00:00"
            else:
                end_time = str(date[0:5]) + str(int(date[5:7])+1) + "-01T00:00:00"
                                        
        url = "https://api.steama.co/sites/26385/utilities/1/usage/?start_time=" + start_time + "&end_time=" + end_time
        r = requests.get(url=url, headers = header)
        s = r.content
        df = pd.read_json(s)
        
        if(month == "01"):
            M = "January"
        elif(month == "02"):
            M = "February"
        elif(month == "03"):
            M = "March"
        elif(month == "04"):
            M = "April"
        elif(month == "05"):
            M = "May"
        elif(month == "06"):
            M = "June"
        elif(month == "07"):
            M = "July"
        elif(month == "08"):
            M = "August"
        elif(month == "09"):
            M = "September"
        elif(month == "10"):
            M = "October"
        elif(month == "11"):
            M = "November"
        else:
            M = "December"
            
        if(month == "04" or month == "06" or month == "09" or month == "11"):
            num = 30
        elif(month == "02" and int(date[0:4])%4==0):
            num = 29
        elif(month == "02" and int(date[0:4])%4!=0):
            num = 28
        else:
            num = 31
        
        if(len(df)==0):
            y_dont_care = []
            x_dont_care = []
            for index in range(1,num+1):
                y_dont_care.append(0)
                x_dont_care.append(index)
                
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_dont_care, y=y_dont_care,
                                mode='lines+markers',
                                ))
            
            fig.update_layout(title = "Peak Loads for " + str(M) + " " + str(date[0:4]),
                           xaxis_title='Date',
                           yaxis_title='Peak Usage Amount (kWh)')  
            return fig
            
        else:
            timestamp = []
            usage_amount = []
                
            for index in range(0,len(df['timestamp'])):
                timestamp.append(str(df['timestamp'][index]))
                usage_amount.append(df['usage'][index])
                
            temp = []
            peaks = []
            clock = []
            clock2 = []
            x = []
            temporary = str(timestamp[0])
            i = int(temporary[8:10])
            date_index = i
                
            for j in range(0,24):
                hold = str(j) + ":00:00"
                clock2.append(datetime.datetime.strptime(hold, '%H:%M:%S').time())
            
            while(i<=num):
                
                for index in range(0,len(timestamp)):
                    temptime = timestamp[index]
                    if(i==int(temptime[8:10])):
                        temp.append(usage_amount[index])
                    else:
                        continue
                
                if(len(temp)==0):
                    temp.clear()
                    i+=1
                    date_index+=1
                else:
                    peaks.append(max(temp))   
                    
                    for counter in range(0,len(timestamp)):
                        holder = str(timestamp[counter])
                        if(usage_amount[counter]==max(temp) and int(holder[8:10])==i):
                            date_time_obj = datetime.datetime.strptime(holder[11:19], '%H:%M:%S')
                            clock.append(date_time_obj.time())
                            x.append(date_index)
                            date_index+=1
                            break
                        else:
                            continue  
                    
                    i+=1
                    temp.clear()  
                    
            fig = go.Figure()
        
            fig.add_trace(go.Scatter(x=x, y=peaks,
                                mode='lines+markers',
                                ))
            
            fig.update_layout(title = "Peak Loads for " + str(M) + " " + str(date[0:4]),
                            xaxis_title='Date',
                            yaxis_title='Peak Usage Amount (kWh)', 
                            xaxis = dict(
                            tickmode = 'linear',
                            tick0 = 1,
                            dtick = 1),
                            xaxis_range=[0,num+1],
                            yaxis_range=[-0.02,max(peaks)+0.02])
            return fig

@app.callback(
    Output(component_id='my_graph', component_property='figure'),
    [Input(component_id='slct_year', component_property='value'),
     Input('TorA','value')])

def update_graph(option_slctd, bttn1):
    
    div = bttn1
    
    if(div==1):
        T = "Total Revenue "
        L = "Total Revenue (USD)"
    else:
        T = "ARPU "
        L = "ARPU (USD)"
    
    url_ER = "https://api.steama.co/exchange-rates/"                     
    r = requests.get(url=url_ER, headers = header)
    s = r.content
    df_ER = pd.read_json(s)

    for index in range(len(df_ER['rate'])):
        if(df_ER['source'][index]=='MWK' and df_ER['target'][index]=='USD'):
            ER = df_ER['rate'][index]
            break
        else:
            continue
    
    date = option_slctd

    start_time = str(date) + "-01-01T00:00:00"
    end_time = str(int(date)+1) + "-01-01T00:00:00"     

    url = "https://api.steama.co/sites/26385/revenue/" + "?start_time=" + start_time + "&end_time=" + end_time                      
    r = requests.get(url=url, headers = header)
    s = r.content
    df = pd.read_json(s)
    
    timestamp = []
    revenue = []
    time = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    
    for index in range(0,len(df['timestamp'])):
        timestamp.append(str(df['timestamp'][index]))
        revenue.append(df['revenue'][index])
            
    monthly_revenue = []
    
    for i in range(1,13):
        
        amount = 0
        
        for index in range(0,len(timestamp)):
            temptime = timestamp[index]
            if(i==int(temptime[5:7])):
                amount += (float(revenue[index])*ER)
            else:
                continue    
        
        if(amount==0):
            monthly_revenue.append(0) 
        else:    
            monthly_revenue.append(amount/div)
            amount = 0
            
    dff = pd.DataFrame(
        {"Month" : time,
         L : monthly_revenue,
        })    
    
    fig = px.bar(dff, x="Month", y=L, title = T + "for " + str(date))
    
    return fig

@app.callback(
    Output(component_id='my_graph_2', component_property='figure'),
    [Input(component_id='my-date-picker-single', component_property='date'),
     Input('TorU_1','value')])

def update_output(date_value, bttn1):
    
    div = bttn1
    
    if(div==1):
        T = "Total Microgrid "
    else:
        T = "Average User "
    
    date = str(date_value)
    
    start_time = date + "T00:00:00"
    if((int(date[5:7])==1 or int(date[5:7])==3 or int(date[5:7])==5 or int(date[5:7])==7 or
        int(date[5:7])==8 or int(date[5:7])==10) and int(date[8:10])==31):
        if(int(date[5:7])<9):
                end_time = date[0:6] + str(int(date[6])+1) + "-01T00:00:00"
        else:
                end_time = date[0:5] + str(int(date[5:7])+1) + "-01T00:00:00"
    elif(int(date[5:7])==12 and int(date[8:10])==31):
        end_time = str(int(date[0:4])+1) + "-01-01T00:00:00"
    elif((int(date[5:7])==4 or int(date[5:7])==6 or int(date[5:7])==9 or int(date[5:7])==11) and int(date[8:10])==30):    
        if(int(date[5:7])<9):
                end_time = date[0:6] + str(int(date[6])+1) + "-01T00:00:00"
        else:
                end_time = date[0:5] + str(int(date[5:7])+1) + "-01T00:00:00"
    elif(int(date[0:4])%4==0 and int(date[5:7])==2 and int(date[8:10])==29):
        end_time = date[0:6] + "3-01T00:00:00"
    elif(int(date[0:4])%4!=0 and int(date[5:7])==2 and int(date[8:10])==28):
        end_time = date[0:6] + "3-01T00:00:00"
    else:
        if(int(date[8:10])<9):
                end_time = date[0:9] + str(int(date[9])+1) + "T00:00:00"
        else:
                end_time = date[0:8] + str(int(date[8:10])+1) + "T00:00:00"
                                                    
    url = "https://api.steama.co/sites/26385/utilities/1/usage/?start_time=" + start_time + "&end_time=" + end_time
    r = requests.get(url=url, headers = header)
    s = r.content
    df = pd.read_json(s)

    usage_amount = []
    time = []
    
    for index in range(0,len(df['timestamp'])):
        holder = str(df['timestamp'][index])
        usage_amount.append(df['usage'][index]/div)
        time.append(holder[11:19])
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=time, y=usage_amount,
                        mode='lines+markers',
                        ))
    
    fig.update_layout(title = T + 'Load Profile on ' + str(date),
                   xaxis_title='Time',
                   yaxis_title='Usage Amount (kWh)')
    
    return fig
@app.callback(
    Output(component_id='my_graph_3', component_property='figure'),
    [Input(component_id='my-date-picker-single', component_property='date'),
     Input('TorU_2','value')])

def update_output_2(date_value,bttn1):
    
    date=date_value  
    month = str(date[5:7])  
    
    
    if(month == "04" or month == "06" or month == "09" or month == "11"):
            num = 30
    elif(month == "02" and int(date[0:4])%4==0):
            num = 29
    elif(month == "02" and int(date[0:4])%4!=0):
            num = 28
    else:
            num = 31
    
    start_time = date + "T00:00:00"
    
    if((int(date[5:7])==1 or int(date[5:7])==3 or int(date[5:7])==5 or int(date[5:7])==7 or
        int(date[5:7])==8 or int(date[5:7])==10) and int(date[8:10])==31):
        if(int(date[5:7])<9):
                end_time = date[0:6] + str(int(date[6])+1) + "-01T00:00:00"
        else:
                end_time = date[0:5] + str(int(date[5:7])+1) + "-01T00:00:00"
    elif((int(date[5:7])==4 or int(date[5:7])==6 or int(date[5:7])==9 or int(date[5:7])==11) and int(date[8:10])==30):    
        if(int(date[5:7])<9):
                end_time = date[0:6] + str(int(date[6])+1) + "-01T00:00:00"
        else:
                end_time = date[0:5] + str(int(date[5:7])+1) + "-01T00:00:00"
    elif(int(date[0:4])%4==0 and int(date[5:7])==2 and int(date[8:10])==29):
        end_time = date[0:6] + str(int(date[6])+1) + "-01T00:00:00"
    elif(int(date[0:4])%4!=0 and int(date[5:7])==2 and int(date[8:10])==28):
        end_time = date[0:6] + str(int(date[6])+1) + "-01T00:00:00"
    elif(int(date[5:7])==12 and int(date[8:10])==31):
        end_time = str(int(date[0:4])+1) + "-01-01T00:00:00" 
    else:
        if(int(date[8:10])<9):
                end_time = date[0:9] + str(int(date[9])+1) + "T00:00:00"
        else:
                end_time = date[0:8] + str(int(date[8:10])+1) + "T00:00:00"
                
                
    
    div = bttn1
    url = "https://api.steama.co/customers/?fields=status,foo/?page=1&page_size=100"
            
    r = requests.get(url=url, headers = header)
    s = r.content
    #converting json string to a panda object
    dfC = pd.read_json(s)
    
    cust_fnames_res=[]
    cust_fnames_bus=[]
    cust_fnames_ins=[]
    
    cust_snames_res=[]
    cust_snames_bus=[]
    cust_snames_ins=[]
    
    
    for index in range(0,len(dfC)):
                holder = dfC['results'][index]
            #if the user type is res add 1
                if(holder['user_type'] == "RES"):
                    cust_fnames_res.append(holder['first_name'])
                    cust_snames_res.append(holder['last_name'])
                elif(holder['user_type'] == "BUS"):
                    cust_fnames_bus.append(holder['first_name'])
                    cust_snames_bus.append(holder['last_name'])
                else:
                    cust_fnames_ins.append(holder['first_name'])
                    cust_snames_ins.append(holder['last_name'])
    
    if (div==1):
        
        usage_amount = [0]*24
        timestamp = []
        time = []        
        
        for index in range(0,len(cust_fnames_res)):
            first_name=cust_fnames_res[index]
            surname=cust_snames_res[index]
            
            url = "https://api.steama.co/customers/?last_name=" + surname + "&first_name=" + first_name
                
            r = requests.get(url=url, headers = header)
            s = r.content
            df = pd.read_json(s)
            holder = df['results'][0]
            
            usage_url = holder['utilities_url'] + "1/usage/"
            url2 = usage_url + "?start_time=" + start_time + "&end_time=" + end_time
            
            r2 = requests.get(url=url2, headers = header)
            s2 = r2.content
            df2 = pd.read_json(s2)
            
            for index in range(0,len(df2['timestamp'])):
                usage_amount[index] += df2['usage'][index]
        

                     
    if (div==2):
        usage_amount = [0]*24
        timestamp = []
        time = []  

        
        for index in range(0,len(cust_fnames_bus)):
            first_name=cust_fnames_bus[index]
            surname=cust_snames_bus[index]
            
            url = "https://api.steama.co/customers/?last_name=" + surname + "&first_name=" + first_name
                
            r = requests.get(url=url, headers = header)
            s = r.content
            df = pd.read_json(s)
            holder = df['results'][0]
            
            usage_url = holder['utilities_url'] + "1/usage/"
            url2 = usage_url + "?start_time=" + start_time + "&end_time=" + end_time
            
            r2 = requests.get(url=url2, headers = header)
            s2 = r2.content
            df2 = pd.read_json(s2)
            
            for index in range(0,len(df2['timestamp'])):
                usage_amount[index] += df2['usage'][index]



    if (div==3):
        usage_amount = [0]*24
        timestamp = []
        time = []  
        
        for index in range(0,len(cust_fnames_ins)):
            first_name=cust_fnames_ins[index]
            surname=cust_snames_ins[index]
            
            url = "https://api.steama.co/customers/?last_name=" + surname + "&first_name=" + first_name
                
            r = requests.get(url=url, headers = header)
            s = r.content
            df = pd.read_json(s)
            holder = df['results'][0]
            
            usage_url = holder['utilities_url'] + "1/usage/"
            url2 = usage_url + "?start_time=" + start_time + "&end_time=" + end_time
            
            r2 = requests.get(url=url2, headers = header)
            s2 = r2.content
            df2 = pd.read_json(s2)
            
            for index in range(0,len(df2['timestamp'])):
                usage_amount[index] += df2['usage'][index]
                

    for index in range(0,len(df2['timestamp'])):
                timestamp.append(str(df2['timestamp'][index]))

    
    for index in range(0,24):
                if(index<10):
                    a = "0" + str(index)
                else:
                    a = str(index)
                temp = a + ":00:00+00:00"
                time.append(temp[0:8])
                
        
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=time, y=usage_amount,
                                mode='lines+markers',
                                ))
            
    fig.update_layout(title ="Load Profile for"  " " + date,
                           xaxis_title='Time',
                           yaxis_title='Usage Amount (kWh)',
                           yaxis_range=[0,max(usage_amount)+0.02])
            
    return fig


@app.callback(
    Output(component_id='my_graph_4', component_property='figure'),
    [Input(component_id='slct_year', component_property='value'),
     Input('TorU_2','value'),Input('TorU_3', 'value')])

def update_output_3(date_value,bttn1,option_slctd):
    
    date=date_value  
    start_time = str(date) + "-01-01T00:00:00"
    end_time = str(int(date)+1) + "-01-01T00:00:00"
    
    div = bttn1
    
    div2=option_slctd
    
    if (div==1):
        User_Category = "Residential"
    elif (div==2):
        User_Category = "Business"
    else:
        User_Category = "Institutional"
        
    if (div2==1):
        Label = "Total"
    else:
        Label="Average"
    
    url = "https://api.steama.co/customers/?fields=status,foo/?page=1&page_size=100"
            
    r = requests.get(url=url, headers = header)
    s = r.content
    #converting json string to a panda object
    dfC = pd.read_json(s)
    
    cust_fnames_res=[]
    cust_fnames_bus=[]
    cust_fnames_ins=[]
    
    cust_snames_res=[]
    cust_snames_bus=[]
    cust_snames_ins=[]
    
    
    for index in range(0,len(dfC)):
                holder = dfC['results'][index]
            #if the user type is res add 1
                if(holder['user_type'] == "RES"):
                    cust_fnames_res.append(holder['first_name'])
                    cust_snames_res.append(holder['last_name'])
                elif(holder['user_type'] == "BUS"):
                    cust_fnames_bus.append(holder['first_name'])
                    cust_snames_bus.append(holder['last_name'])
                else:
                    cust_fnames_ins.append(holder['first_name'])
                    cust_snames_ins.append(holder['last_name'])
    
    daily_usage = [0]*365
    timestamp = []
    time = ["January","February","March","April","May","June","July","August","September","October","November","December"]  
    monthly_usage=[] 
    
    if (div==1):      
        
        for index in range(0,len(cust_fnames_res)):
            first_name=cust_fnames_res[index]
            surname=cust_snames_res[index]
            
            url = "https://api.steama.co/customers/?last_name=" + surname + "&first_name=" + first_name
                
            r = requests.get(url=url, headers = header)
            s = r.content
            df = pd.read_json(s)
            holder = df['results'][0]
            
            usage_url = holder['utilities_url'] + "1/usage/"
            url2 = usage_url + "?start_time=" + start_time + "&end_time=" + end_time
            
            r2 = requests.get(url=url2, headers = header)
            s2 = r2.content
            df2 = pd.read_json(s2)

            
            for index in range(0,len(df2['timestamp'])):
                if (div2==1):
                    daily_usage[index]+=(df2['usage'][index])
                else:
                    daily_usage[index]+=((df2['usage'][index])/len(cust_fnames_res))
        
                
    if (div==2):
       
        for index in range(0,len(cust_fnames_bus)):
            first_name=cust_fnames_bus[index]
            surname=cust_snames_bus[index]
            
            url = "https://api.steama.co/customers/?last_name=" + surname + "&first_name=" + first_name
                
            r = requests.get(url=url, headers = header)
            s = r.content
            df = pd.read_json(s)
            holder = df['results'][0]
            
            usage_url = holder['utilities_url'] + "1/usage/"
            url2 = usage_url + "?start_time=" + start_time + "&end_time=" + end_time
            
            r2 = requests.get(url=url2, headers = header)
            s2 = r2.content
            df2 = pd.read_json(s2)

            
            for index in range(0,len(df2['timestamp'])):
                if (div2==1):
                    daily_usage[index]+=(df2['usage'][index])
                else:
                    daily_usage[index]+=((df2['usage'][index])/len(cust_fnames_bus))



    if (div==3):

        for index in range(0,len(cust_fnames_ins)):
            first_name=cust_fnames_ins[index]
            surname=cust_snames_ins[index]
            
            url = "https://api.steama.co/customers/?last_name=" + surname + "&first_name=" + first_name
                
            r = requests.get(url=url, headers = header)
            s = r.content
            df = pd.read_json(s)
            holder = df['results'][0]
            
            usage_url = holder['utilities_url'] + "1/usage/"
            url2 = usage_url + "?start_time=" + start_time + "&end_time=" + end_time
            
            r2 = requests.get(url=url2, headers = header)
            s2 = r2.content
            df2 = pd.read_json(s2)

            
            for index in range(0,len(df2['timestamp'])):
                if (div2==1):
                    daily_usage[index]+=(df2['usage'][index])
                else:
                    daily_usage[index]+=((df2['usage'][index])/len(cust_fnames_ins))
                

    for index in range(0,len(df2['timestamp'])):
                timestamp.append(str(df2['timestamp'][index]))

    
    for i in range(1,13):
        
        amount = 0
        
        for index in range(0,len(timestamp)):
            temptime = timestamp[index]
            if(i==int(temptime[5:7])):
                amount += (float(daily_usage[index]))
            else:
                continue    

        if(amount==0):
            monthly_usage.append(0) 
        else:    
            monthly_usage.append(amount)
            amount = 0 
                
     
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=time, y=monthly_usage,
                                mode='lines+markers',
                                ))
            
    fig.update_layout(title =Label + " Load Profile for " + User_Category + " customers for " + str(date),
                           xaxis_title='Month',
                           yaxis_title='Usage Amount (kWh)',
                           yaxis_range=[0,max(monthly_usage)+0.02])
    
    return fig

@app.callback(
    Output(component_id='my_graph_5', component_property='figure'),
    [Input(component_id='slct_year', component_property='value'),
     Input('TorU_2','value'),Input('TorU_3','value')])

def update_output_4(date_value,bttn1,option_slctd):
    
    date=date_value  
    start_time = str(date) + "-01-01T00:00:00"
    end_time = str(int(date)+1) + "-01-01T00:00:00"
    
    div = bttn1
    div2 = option_slctd

    if (div==1):
        User_Category = "Residential"
    elif (div==2):
        User_Category = "Business"
    else:
        User_Category = "Institutional"
        
    if (div2==1):
        Label = "Total"
    else:
        Label="Average"
        
    url = "https://api.steama.co/customers/?fields=status,foo/?page=1&page_size=100"
            
    r = requests.get(url=url, headers = header)
    s = r.content
    #converting json string to a panda object
    dfC = pd.read_json(s)
    
    cust_fnames_res=[]
    cust_fnames_bus=[]
    cust_fnames_ins=[]
    
    cust_snames_res=[]
    cust_snames_bus=[]
    cust_snames_ins=[]
    
    
    for index in range(0,len(dfC)):
                holder = dfC['results'][index]
            #if the user type is res add 1
                if(holder['user_type'] == "RES"):
                    cust_fnames_res.append(holder['first_name'])
                    cust_snames_res.append(holder['last_name'])
                elif(holder['user_type'] == "BUS"):
                    cust_fnames_bus.append(holder['first_name'])
                    cust_snames_bus.append(holder['last_name'])
                else:
                    cust_fnames_ins.append(holder['first_name'])
                    cust_snames_ins.append(holder['last_name'])
    
    daily_revenue = [0]*365
    timestamp = []
    time = ["January","February","March","April","May","June","July","August","September","October","November","December"]  
    monthly_revenue=[]  
    
    if (div==1):      
        
        for index in range(0,len(cust_fnames_res)):
            first_name=cust_fnames_res[index]
            surname=cust_snames_res[index]
            
            url = "https://api.steama.co/customers/?last_name=" + surname + "&first_name=" + first_name


            r = requests.get(url=url, headers = header)
            s = r.content
            df = pd.read_json(s)
            holder = df['results'][0]
            
            usage_url = holder['revenue_url']
            url2 = usage_url + "?start_time=" + start_time + "&end_time=" + end_time
            
            r2 = requests.get(url=url2, headers = header)
            s2 = r2.content
            df2 = pd.read_json(s2)

            print(url2)
            print(index)
            
            
            for index in range(0,len(df2['timestamp'])):
                if (div2==1):
                    daily_revenue[index]+=(df2['revenue'][index])
                else:
                    daily_revenue[index]+=((df2['revenue'][index])/len(cust_fnames_res))
                    
        
                
    if (div==2):
       
        for index in range(0,len(cust_fnames_bus)):
            first_name=cust_fnames_bus[index]
            surname=cust_snames_bus[index]
            
            url = "https://api.steama.co/customers/?last_name=" + surname + "&first_name=" + first_name


            r = requests.get(url=url, headers = header)
            s = r.content
            df = pd.read_json(s)
            holder = df['results'][0]
            
            usage_url = holder['revenue_url']
            url2 = usage_url + "?start_time=" + start_time + "&end_time=" + end_time
            
            r2 = requests.get(url=url2, headers = header)
            s2 = r2.content
            df2 = pd.read_json(s2)

            print(url2)
            print(index)
            
            
            for index in range(0,len(df2['timestamp'])):
                if (div2==1):
                    daily_revenue[index]+=(df2['revenue'][index])
                else:
                    daily_revenue[index]+=((df2['revenue'][index])/len(cust_fnames_bus))



    if (div==3):

        for index in range(0,len(cust_fnames_ins)):
            first_name=cust_fnames_ins[index]
            surname=cust_snames_ins[index]
            
            url = "https://api.steama.co/customers/?last_name=" + surname + "&first_name=" + first_name


            r = requests.get(url=url, headers = header)
            s = r.content
            df = pd.read_json(s)
            holder = df['results'][0]
            

            usage_url = holder['revenue_url']
            url2 = usage_url + "?start_time=" + start_time + "&end_time=" + end_time
            
            r2 = requests.get(url=url2, headers = header)
            s2 = r2.content
            df2 = pd.read_json(s2)

            print(url2)
            print(index)
            
            for index in range(0,len(df2['timestamp'])):
                if (div2==1):
                    daily_revenue[index]+=(df2['revenue'][index])
                else:
                    daily_revenue[index]+=((df2['revenue'][index])/len(cust_fnames_ins))
                

    for index in range(0,len(df2['timestamp'])):
        timestamp.append(str(df2['timestamp'][index]))   
            
    for i in range(1,13):
        
            amount = 0
        
            for index in range(0,len(timestamp)):
                temptime = timestamp[index]
                if(i==int(temptime[5:7])):
                    amount += (float(daily_revenue[index])*ER)
                else:
                    continue    

            if(amount==0):
                monthly_revenue.append(0) 
            else:    
                monthly_revenue.append(amount)  
                amount = 0 
                
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=time, y=monthly_revenue,
                                mode='lines+markers',
                                ))
            
    fig.update_layout(title =Label + " Revenue for " + User_Category + " customers for " + str(date),
                           xaxis_title='Month',
                           yaxis_title='Revenue (USD)',
                           yaxis_range=[0,max(monthly_revenue)+5])
    
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)



#######Extra code to plot data as a bar chart /// may be better alternative 
#    dff = pd.DataFrame(
 #       {"Month" : time,
  #       "Usage" : monthly_usage,
   #     })    
    
    #fig = px.bar(dff, x="Month", y="Usage", title = "Load profile")
    
#    return fig F

