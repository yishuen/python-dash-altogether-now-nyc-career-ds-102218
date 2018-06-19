#import dash core components as dcc
import dash_core_components as dcc
#import dash html components as html
import dash_html_components as html
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

def create_pop_data_obj(list_of_cities, name):
    sorted_cities = sorted(list_of_cities, key=lambda city: city.demographic.population)[-75:]
    names = [city.name for city in sorted_cities]
    populations = [city.demographic.population for city in sorted_cities]
    return {'name': name, 'x': names, 'y': populations, 'type': 'bar'}

def create_rent_data_obj(list_of_cities, name):
    sorted_cities = sorted(list_of_cities, key=lambda city: city.demographic.population)[-75:]
    names = [city.name for city in sorted_cities]
    populations = [city.demographic.mean_rent for city in sorted_cities]
    return {'name': name, 'x': names, 'y': populations, 'type': 'line'}

def get_all_cities(state_name):
    state_obj = State.query.filter(State.name == state_name).first()
    return state_obj.cities

def create_graph(data, comparison):
    return dcc.Graph(id = "city_population_graph_{}".format(data['name']), figure = { 'data': [data],'layout': { 'title': '{} - {} per City'.format(data['name'], comparison)}})

def generate_pop_bar_graph(state):
    all_cities = get_all_cities(state)
    data = create_pop_data_obj(all_cities, state)
    return create_graph(data, 'Population')

def generate_rent_bar_graph(state):
    all_cities = get_all_cities(state)
    data = create_rent_data_obj(all_cities, state)
    return create_graph(data, 'Mean Rent')

app.layout = html.Div(children=[
    generate_pop_drop_down(),
    html.Div(id='pop_graph_container'),
    html.Div(id='rent_graph_container')
])

@app.callback(
    Output(component_id='pop_graph_container', component_property='children'),
    [Input(component_id='state_selector', component_property='value')]
)
def change_table(input_value):
    return generate_pop_bar_graph(input_value)

@app.callback(
    Output(component_id='rent_graph_container', component_property='children'),
    [Input(component_id='state_selector', component_property='value')]
)
def change_table(input_value):
    return generate_rent_bar_graph(input_value)
