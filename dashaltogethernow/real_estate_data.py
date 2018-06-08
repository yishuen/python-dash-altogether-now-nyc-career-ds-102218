# importing the os (operating system module)
import os
# using the os module to get the current working directory
# in order get the proper path for the excel file
cwd = os.getcwd()

# importing pandas module to read the excel file and extract the data
import pandas

# using pandas to read the excel file and giving the names of the columns
excel_data = pandas.read_excel(cwd+'/real_estate_db.xlsx', names=["UID", "BLOCKID", "SUMLEVEL", "COUNTYID", "STATEID", "state", "state_ab", "city", "place", "type", "primary", "zip_code", "area_code", "lat", "lng", "ALand", "AWater", "pop", "male_pop", "female_pop", "rent_mean", "rent_median", "rent_stdev", "rent_sample_weight", "rent_samples", "rent_gt_10", "rent_gt_15", "rent_gt_20", "rent_gt_25", "rent_gt_30", "rent_gt_35", "rent_gt_40", "rent_gt_50", "universe_samples", "used_samples", "hi_mean", "hi_median", "hi_stdev", "hi_sample_weight", "hi_samples", "family_mean", "family_median", "family_stdev", "family_sample_weight", "family_samples", "hc_mortgage_mean", "hc_mortgage_median", "hc_mortgage_stdev", "hc_mortgage_sample_weight", "hc_mortgage_samples", "hc_mean", "hc_median", "hc_stdev", "hc_samples", "hc_sample_weight", "home_equity_second_mortgage", "second_mortgage", "home_equity", "debt", "second_mortgage_cdf", "home_equity_cdf", "debt_cdf", "hs_degree", "hs_degree_male", "hs_degree_female", "male_age_mean", "male_age_median", "male_age_stdev", "male_age_sample_weight", "male_age_samples", "female_age_mean", "female_age_median", "female_age_stdev", "female_age_sample_weight", "female_age_samples", "pct_own", "married", "married_snp", "separated", "divorced"])
excel_data.fillna(value=0.0)
# removing the first line of data that contains the headers
# and returning the remaining data in a list of dictionaries
data = excel_data.to_dict('records')
