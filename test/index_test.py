import unittest, sys, sqlite3, json
sys.path.insert(0, '..')
from dashaltogethernow import *
from dashaltogethernow.models import City, State, Demographic

class TestDashAltogetherNow(unittest.TestCase):

    # --- tests app from __init__.py
    if app:
        def test_app_setup(self):
            self.assertEqual(app.url_base_pathname, '/dashboard')


    # --- tests models/relationships prior to data seeding ---
    if City and State and Demographic:
        brohio = State(name="Brohio", state_ab="BH")
        snaketown = City(name="Snaketown", type="City", zip_code=10583, lat=35, lng=99)
        jackson = City(name="Jackson", type="City", zip_code=83014, lat=40, lng=40)
        brohio.cities.extend((snaketown, jackson))
        demo = Demographic(population=8000, male_pop=6000, female_pop=2000, mean_rent=850, pct_own=20, pct_married=25)
        jackson.demographic = demo

        def test_state_model(self):
            self.assertEqual(self.brohio.name, "Brohio", "state has a name")
            self.assertEqual(self.brohio.state_ab, "BH", "state has an abbreviation")
            brohio_cities = [city.name for city in self.brohio.cities]
            self.assertEqual(brohio_cities, ['Snaketown', 'Jackson'], "state has many cities")

        def test_city_model(self):
            self.assertEqual(self.jackson.name, "Jackson", "city has a name")
            self.assertEqual(self.jackson.type, "City", "city has a type")
            self.assertEqual(self.jackson.zip_code, 83014, "city has a zip code")
            self.assertEqual(self.jackson.lat, 40, "city has a latitude")
            self.assertEqual(self.jackson.lng, 40, "city has a longitude")
            self.assertEqual(self.jackson.demographic, self.demo, "city has a demographic")
            self.assertEqual(self.jackson.state, self.brohio, "city belongs to a state")

        def test_demographic_model(self):
            self.assertEqual(self.demo.population, 8000, "demographic has a population")
            self.assertEqual(self.demo.male_pop, 6000, "demographic has a male_pop")
            self.assertEqual(self.demo.female_pop, 2000, "demographic has a female_pop")
            self.assertEqual(self.demo.mean_rent, 850, "demographic has a mean_rent")
            self.assertEqual(self.demo.pct_own, 20, "demographic has a pct_own")
            self.assertEqual(self.demo.pct_married, 25, "demographic has a pct_married")
            self.assertEqual(self.demo.city, self.jackson, "demographic has a city")


    # --- tests models/relationship after data seeding ---
    if db:
        session = db.session

        def test_db_total_cities(self):
            self.assertEqual(len(self.session.query(City).all()), 11276)

        def test_db_total_states(self):
            self.assertEqual(len(self.session.query(State).all()), 52)

        def test_state_has_many_cities(self):
            alaska = self.session.query(State).first()
            self.assertEqual(len(alaska.cities), 45)

        def test_city_has_correct_demographic_info(self):
            brooklyn_ny = brooklyn = self.session.query(City).filter(City.name == "Brooklyn", City.state_id == 35).first()
            self.assertEqual(brooklyn.demographic.population, 1453565)
            self.assertEqual(brooklyn.demographic.male_pop, 682992)
            self.assertEqual(brooklyn.demographic.female_pop, 770573)
            self.assertEqual(round(brooklyn.demographic.mean_rent, 2), 1318.46)
            self.assertEqual(round(brooklyn.demographic.pct_own, 2), 0.35)
            self.assertEqual(round(brooklyn.demographic.pct_married, 2), 0.46)


    # --- test Dash layout ---
    response = app.serve_layout()
    str = response.data.decode()
    children = json.loads(str)['props']['children']
    states_dd = children[0]['props']['options']

    def test_dropdown(self):
        gather_states = [state['label'] for state in self.states_dd]
        result = ['Alaska', 'Alabama', 'Arkansas', 'Arizona', 'California', 'Colorado', 'Connecticut', 'District of Columbia', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana', 'Kansas', 'Kentucky', 'Louisiana', 'Massachusetts', 'Maryland', 'Maine', 'Michigan', 'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North Carolina', 'North Dakota', 'Nebraska', 'New Hampshire', 'New Jersey', 'New Mexico', 'Nevada', 'New York', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Virginia', 'Vermont', 'Washington', 'Wisconsin', 'West Virginia', 'Wyoming']
        self.assertEqual(gather_states, result, "dropdown includes all 52 'states'")
        self.assertEqual(self.children[0]['props']['value'], 'New Jersey', "default layout set to New Jersey")


    # --- test table callbacks
    def test_population_graph(self):
        pop_callback = app.callback_map['pop_graph_container.children']['callback']
        response = pop_callback('New York')
        str = response.data.decode()
        data = json.loads(str)
        x_values = data['response']['props']['children']['props']['figure']['data'][0]['x']
        x_result = ['East Elmhurst', 'Bethpage', 'Newburgh', 'Bay Shore', 'Liverpool', 'Saratoga Springs', 'Endicott', 'Rome', 'Amherst', 'North Babylon', 'Long Beach', 'East Setauket', 'Holtsville', 'Far Rockaway', 'Williamsville', 'Freeport', 'Hamburg', 'Middle Village', 'Hollis', 'Farmingdale', 'Elmont', 'East Amherst', 'Elmira', 'Fairport', 'East Meadow', 'Richmond Hill', 'Glendale', 'Ossining', 'Huntington Station', 'Westbury', 'Jamestown', 'Amityville', 'Lindenhurst', 'West Seneca', 'Monroe', 'Levittown', 'New City', 'Queens Village', 'Poughkeepsie', 'Ridgewood', 'Ithaca', 'Forest Hills', 'Spring Valley', 'Ozone Park', 'Rego Park', 'Utica', 'Brentwood', 'North Tonawanda', 'Floral Park', 'Woodside', 'Jackson Heights', 'Mount Vernon', 'New Rochelle', 'Corona', 'South Ozone Park', 'Binghamton', 'Elmhurst', 'Valley Stream', 'White Plains', 'Hempstead', 'Troy', 'Bayside', 'Schenectady', 'Albany', 'Long Island City', 'Syracuse', 'Yonkers', 'Buffalo', 'Jamaica', 'Flushing', 'Staten Island', 'Rochester', 'Bronx', 'New York', 'Brooklyn']
        y_values = data['response']['props']['children']['props']['figure']['data'][0]['y']
        y_result = [21544, 21603, 22129, 22386, 22528, 22637, 23228, 23286, 23516, 23615, 24177, 24222, 24238, 25029, 25465, 25551, 25563, 25678, 25778, 25974, 26470, 26606, 27292, 27361, 27528, 27710, 28007, 28500, 28678, 28831, 29258, 29410, 29961, 31271, 32250, 32428, 33095, 33557, 33627, 34488, 34634, 35051, 35490, 36509, 37624, 38820, 39253, 39465, 39471, 41350, 41408, 43029, 43608, 43787, 44479, 46959, 47083, 49844, 50745, 51716, 52739, 57625, 65753, 82881, 89751, 95501, 114578, 138655, 143679, 147308, 207095, 275188, 781455, 852276, 1453565]
        self.assertEqual(x_values, x_result)
        self.assertEqual(y_values, y_result)

    def test_mean_rent_graph(self):
        pop_callback = app.callback_map['rent_graph_container.children']['callback']
        response = pop_callback('New York')
        str = response.data.decode()
        data = json.loads(str)
        x_values = data['response']['props']['children']['props']['figure']['data'][0]['x']
        x_result = ['East Elmhurst', 'Bethpage', 'Newburgh', 'Bay Shore', 'Liverpool', 'Saratoga Springs', 'Endicott', 'Rome', 'Amherst', 'North Babylon', 'Long Beach', 'East Setauket', 'Holtsville', 'Far Rockaway', 'Williamsville', 'Freeport', 'Hamburg', 'Middle Village', 'Hollis', 'Farmingdale', 'Elmont', 'East Amherst', 'Elmira', 'Fairport', 'East Meadow', 'Richmond Hill', 'Glendale', 'Ossining', 'Huntington Station', 'Westbury', 'Jamestown', 'Amityville', 'Lindenhurst', 'West Seneca', 'Monroe', 'Levittown', 'New City', 'Queens Village', 'Poughkeepsie', 'Ridgewood', 'Ithaca', 'Forest Hills', 'Spring Valley', 'Ozone Park', 'Rego Park', 'Utica', 'Brentwood', 'North Tonawanda', 'Floral Park', 'Woodside', 'Jackson Heights', 'Mount Vernon', 'New Rochelle', 'Corona', 'South Ozone Park', 'Binghamton', 'Elmhurst', 'Valley Stream', 'White Plains', 'Hempstead', 'Troy', 'Bayside', 'Schenectady', 'Albany', 'Long Island City', 'Syracuse', 'Yonkers', 'Buffalo', 'Jamaica', 'Flushing', 'Staten Island', 'Rochester', 'Bronx', 'New York', 'Brooklyn']
        y_values_raw = data['response']['props']['children']['props']['figure']['data'][0]['y']
        y_values = [round(el, 2) for el in y_values_raw]
        y_result = [1395.7, 1699.26, 1288.28, 1610.4, 866.53, 1334.01, 793.47, 1415.08, 964.89, 1602.21, 1533.47, 1543.05, 1657.93, 917.06, 1257.47, 1585.3, 847.54, 1474.78, 1256.69, 1685.46, 1531.68, 1401.26, 796.83, 964.27, 1840.68, 1263.91, 1400.35, 1551.32, 1443.04, 1712.59, 683.03, 1632.21, 1578.83, 921.89, 1473.38, 1581.25, 1498.99, 1442.92, 1142.02, 1321.88, 1177.37, 1570.08, 1409.83, 1368.01, 1410.95, 790.14, 1400.13, 732.39, 1586.12, 1445.66, 1390.23, 1257.31, 1394.31, 1413.56, 1432.54, 747.16, 1456.18, 1591.84, 1575.08, 1405.73, 917.06, 1775.31, 930.01, 1001.43, 1664.63, 850.19, 1306.09, 713.99, 1384.26, 1392.83, 1305.46, 888.82, 1130.05, 1675.37, 1318.46]
        self.assertEqual(x_values, x_result)
        self.assertEqual(y_values, y_result)
