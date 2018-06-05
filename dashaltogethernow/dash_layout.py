#import dash
import dash
#import dash core components as dcc
import dash_core_components as dcc
#import dash html components as html
import dash_html_components as html

import plotly.graph_objs as go
# import Input, Output from dash.dependencies for callback functions
from dash.dependencies import Input, Output

from dashaltogethernow import app
from dashaltogethernow.models import db, City, Demographic, State

def generate_drop_down():
    return dcc.Dropdown(
        id='sort-by-selector',
        options=[
            {'label': 'Country', 'value': 'Country'},
            {'label': 'Pho', 'value': 'Pho'},
            {'label': 'Ramen', 'value': 'Ramen'},
            {'label': 'Soba', 'value': 'Soba'}
        ],
        value="Country"
    )

def generate_scatter_plot():
    all_cities = list(City.query.all())
    traces = []
    for city in all_cities[1:]:
        traces.append(go.Scatter(x=city.demographics[0].population, y=city.demographics[0].mean_rent, text=city.state.name, mode='markers', opacity=0.7, name=city.state.name, marker={ 'size': 10, 'line': {'width': 0.5, 'color': 'blue'} }
        ))
    return dcc.Graph (
        id='life-exp-vs-gdp',
        figure={
            'data': traces,
            'layout': go.Layout(
                xaxis={'title': 'City Population'},
                yaxis={'title': 'City Mean Rent'},
                hovermode='closest'
            )
        }
    )


app.layout = html.Div(children=[
    # html.Div(id='table_container'),
    html.H3(children='Interest in Pho, Ramen, and Soba by Country according to Google Search from 01/2004 - 06/2018'),
    generate_scatter_plot()
])

# @app.callback(
#     Output(component_id='table_container', component_property='children'),
#     [Input(component_id='sort-by-selector', component_property='value')]
# )
# def sort_table(input_value):
#     global data
#     sorted_data = sorted(data, key=lambda datum: datum[input_value])
#     return generate_table(sorted_data)
