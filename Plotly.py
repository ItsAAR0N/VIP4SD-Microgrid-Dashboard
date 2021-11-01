"""
Created on Sun Oct 31 21:24:20 2021

@author: Aaron Shek
"""

# Ensure to run the following in your CMD terminal in Windows as admin:
"""
python3 -m pip install dash
python3 -m pip install dash-renderer
python3 -m pip install dash_html_components 
python3 -m pip install dash_core_components
python3 -m pip install plotly.express
"""

import dash # Dash is python framework created by plotly for creating interactive web applications
import dash_core_components as dcc 
import dash_html_components as html
import plotly  
import plotly.express as px 

app = dash.Dash(__name__)
df = px.data.iris()

colors = { # Dictionary of values assigned to variables to save time and efficiency
    'plotColor':'#D3D3D3',
    'globalFont':'verdana',
}

app.layout = html.Div([ # The <div> tag defines a division or a section in an HTML document.
    
    html.H1("Simple Plotly example ", # Heading H1 etc. Refer to HTML5.
        style = {
            'textAlign':'center',
            'color':'#3E71C2',
            'font-family':colors['globalFont'],
            
        }
    ),

    html.Hr(), # Used to create lines and separate parts
    html.Br(),
    html.Div("A simple example of a development framework from Plotly.", # Use comma for next line
        style = {
            'textAlign':'center',
            'font-family':colors['globalFont'],
        }
    ), 

    html.Br(), 
    dcc.Graph(
        id = 'samplechart',
        figure = {
            'data': [
                {'x':[5,6,7],'y':[12,15,18],'type':'bar','name':'First Chart'}, # Simple bar chart
                {'x':[1,2,3],'y':[4,5,6],'type':'bar','name':'First Chart'},
            ],

            'layout': {
                'title':'Simple Bar Chart',
                'plot_bgcolor':colors['plotColor'],
                'paper_bgcolor':colors['plotColor'],
    
            }
        }
    )

])
if __name__ == '__main__': # Protects users from accidentally invoking the script when they didn't intend to. Based on Flask framework
    app.run_server(debug=True) # Ctrl+C in terminal to quit


# Up to tut. 6 of Plotly of link 5 