from models import State, City, Demographic, db
from real_estate_data import data

def get_all_rows_for_city(city_name, state_name, city_data=data):
    cities_list = []
    for city in city_data:
        if city['state'].lower() == state_name.lower() and city['city'].lower() == city_name.lower():
            cities_list.append(city)
    return cities_list

def aggregate_demograpic_attribute(city_rows_list, attribute):
    attribute_sum = 0.0
    for city in city_rows_list:
        attribute_sum += float(city[attribute])
    return attribute_sum

def mean_demograpic_attribute(city_rows_list, attribute):
    attribute_sum = 0.0
    for city in city_rows_list:
        attribute_sum += float(city[attribute])
    attribute_mean = (attribute_sum/len(city_rows_list))
    return attribute_mean

def make_demographic_object(city_rows_list, city_id):
    if list(Demographic.query.filter(Demographic.city_id == city_id)):
        return Demographic.query.filter(Demographic.city_id == city_id).first()
    else:
        base_instance = city_rows_list[0]
        aggregate_pop = aggregate_demograpic_attribute(city_rows_list, 'pop')
        aggregate_female_pop = aggregate_demograpic_attribute(city_rows_list, 'female_pop')
        aggregate_male_pop = aggregate_demograpic_attribute(city_rows_list, 'male_pop')
        mean_rent = mean_demograpic_attribute(city_rows_list, 'rent_mean')
        mean_pct_own = mean_demograpic_attribute(city_rows_list, 'pct_own')
        mean_pct_married = mean_demograpic_attribute(city_rows_list, 'married')
        return Demographic(population=aggregate_pop, male_pop=aggregate_male_pop, female_pop=aggregate_female_pop, mean_rent=mean_rent, pct_own=mean_pct_own, pct_married=mean_pct_married, city_id=city_id)

def make_city_object(city_rows_list, state_id):
    base_instance = city_rows_list[0]
    if list(City.query.filter(City.name == city_rows_list[0]['city'], City.state_id == state_id)):
        return City.query.filter(City.name == base_instance['city']).first()
    else:
        return City(name=base_instance['city'], type=base_instance['type'], zip_code=base_instance['zip_code'], lat=base_instance['lat'], lng=base_instance['lng'], state_id=state_id)

def make_state_object(city_rows_list):
    base_instance = city_rows_list[0]
    if list(State.query.filter(State.name == base_instance['state'])):
        return State.query.filter(State.name == base_instance['state']).first()
    else:
        return State(name=base_instance['state'], state_ab=base_instance['state_ab'])

def get_all_cities_and_states(city_data=data):
    list_of_city_and_states = []
    for city in city_data[1:]:
        obj = {'city': city['city'], 'state': city['state']}
        if obj not in list_of_city_and_states:
            list_of_city_and_states.append(obj)
    return list_of_city_and_states

def add_all_related_instances_by_state():
    for city_state_obj in get_all_cities_and_states():
        city_rows_list = get_all_rows_for_city(city_state_obj['city'], city_state_obj['state'])
        state = make_state_object(city_rows_list)
        new_city = make_city_object(city_rows_list, state.id)
        new_demographic = make_demographic_object(city_rows_list, new_city.id)
        state.cities.append(new_city)
        new_city.demographic = new_demographic
        db.session.add(state)
        db.session.add(new_city)
        db.session.add(new_demographic)
    db.session.commit()

add_all_related_instances_by_state()
