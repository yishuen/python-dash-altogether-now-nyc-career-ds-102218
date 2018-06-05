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

def generate_pop_drop_down():
    states = [{'label': state.name, 'value': state.name} for state in State.query.all()]
    return dcc.Dropdown(
        id='state_selector',
        options=states,
        value="New Jersey"
    )

def generate_bar_graphs(state="New Jersey"):
    state_obj = State.query.filter(State.name == state).first()
    all_cities = state_obj.cities
    names = [city.name for city in all_cities]
    populations = [city.demographics[0].population for city in all_cities]
    return dcc.Graph(
    id = "city_population_graph",
    figure = {
            'data': [{
            'name': state_obj.name,
            'x': names,
            'y': populations,
            'type': 'bar'
            }],
            'layout': {
                'title': '{} Population Data'.format(state_obj.name)
            }
        }
    )


app.layout = html.Div(children=[
    generate_pop_drop_down(),
    html.Div(id='pop_graph_container'),
])

@app.callback(
    Output(component_id='pop_graph_container', component_property='children'),
    [Input(component_id='state_selector', component_property='value')]
)
def change_table(input_value):
    return generate_bar_graphs(input_value)
