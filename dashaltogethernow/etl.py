# importing the os (operating system module)
import os
# using the os module to get the current working directory
# in order get the proper path for the excel file
cwd = os.getcwd()

# importing pandas module to read the excel file and extract the data
import pandas

# using pandas to read the excel file and giving the names of the columns
excel_data = pandas.read_excel(cwd+'/dashaltogethernow/real_estate_db.xlsx', names=["UID", "BLOCKID", "SUMLEVEL", "COUNTYID", "STATEID", "state", "state_ab", "city", "place", "type", "primary", "zip_code", "area_code", "lat", "lng", "ALand", "AWater", "pop", "male_pop", "female_pop", "rent_mean", "rent_median", "rent_stdev", "rent_sample_weight", "rent_samples", "rent_gt_10", "rent_gt_15", "rent_gt_20", "rent_gt_25", "rent_gt_30", "rent_gt_35", "rent_gt_40", "rent_gt_50", "universe_samples", "used_samples", "hi_mean", "hi_median", "hi_stdev", "hi_sample_weight", "hi_samples", "family_mean", "family_median", "family_stdev", "family_sample_weight", "family_samples", "hc_mortgage_mean", "hc_mortgage_median", "hc_mortgage_stdev", "hc_mortgage_sample_weight", "hc_mortgage_samples", "hc_mean", "hc_median", "hc_stdev", "hc_samples", "hc_sample_weight", "home_equity_second_mortgage", "second_mortgage", "home_equity", "debt", "second_mortgage_cdf", "home_equity_cdf", "debt_cdf", "hs_degree", "hs_degree_male", "hs_degree_female", "male_age_mean", "male_age_median", "male_age_stdev", "male_age_sample_weight", "male_age_samples", "female_age_mean", "female_age_median", "female_age_stdev", "female_age_sample_weight", "female_age_samples", "pct_own", "married", "married_snp", "separated", "divorced"])

# removing the first line of data that contains the headers
# and returning the remating data in a list of dictionaries
data = excel_data.to_dict('records')


from dashaltogethernow.models import State, City, Demographic, db


def get_all_rows_for_city(city_name, state_name, city_data=data):
    cities_list = []
    for city in city_data:
        if city['state'].lower() == state_name.lower() and city['city'].lower() == city_name.lower():
            cities_list.append(city)
    return cities_list

def aggregate_demograpic_attribute(city_rows_list, attribute):
    attribute_sum = 0
    for city in city_rows_list:
        attribute_sum += int(city[attribute])
    return attribute_sum

def mean_demograpic_attribute(city_rows_list, attribute):
    attribute_sum = 0
    for city in city_rows_list:
        attribute_sum += int(city[attribute])
    attribute_mean = (attribute_sum/len(city_rows_list))
    return attribute_mean

def make_demographic_object(city_rows_list, city_id):
    base_instance = city_rows_list[0]
    aggregate_pop = aggregate_demograpic_attribute(city_rows_list, 'pop')
    aggregate_female_pop = aggregate_demograpic_attribute(city_rows_list, 'female_pop')
    aggregate_male_pop = aggregate_demograpic_attribute(city_rows_list, 'male_pop')
    mean_rent = mean_demograpic_attribute(city_rows_list, 'rent_mean')
    mean_pct_own = mean_demograpic_attribute(city_rows_list, 'pct_own')
    mean_pct_married = mean_demograpic_attribute(city_rows_list, 'married')
    return Demographic(name=base_instance['name'], population=aggregate_pop, male_pop=aggregate_male_pop, female_pop=aggregate_female_pop, mean_rent=mean_rent, pct_own=mean_pct_own, pct_married=mean_pct_married, city_id=city_id)

def make_city_object(city_rows_list, state_id):
    base_instance = city_rows_list[0]
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
        new_city.demographics.append(new_demographic)
        db.commit(state)
        db.commit(new_city)
