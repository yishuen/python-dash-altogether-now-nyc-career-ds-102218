
# Dash Altogether Now

UID	BLOCKID	SUMLEVEL	COUNTYID	STATEID	state	state_ab	city	place	type	primary	zip_code	area_code	lat	lng	ALand	AWater	pop	male_pop	female_pop	rent_mean	rent_median	rent_stdev	rent_sample_weight	rent_samples	rent_gt_10	rent_gt_15	rent_gt_20	rent_gt_25	rent_gt_30	rent_gt_35	rent_gt_40	rent_gt_50	universe_samples	used_samples	hi_mean	hi_median	hi_stdev	hi_sample_weight	hi_samples	family_mean	family_median	family_stdev	family_sample_weight	family_samples	hc_mortgage_mean	hc_mortgage_median	hc_mortgage_stdev	hc_mortgage_sample_weight	hc_mortgage_samples	hc_mean	hc_median	hc_stdev	hc_samples	hc_sample_weight	home_equity_second_mortgage	second_mortgage	home_equity	debt	second_mortgage_cdf	home_equity_cdf	debt_cdf	hs_degree	hs_degree_male	hs_degree_female	male_age_mean	male_age_median	male_age_stdev	male_age_sample_weight	male_age_samples	female_age_mean	female_age_median	female_age_stdev	female_age_sample_weight	female_age_samples	pct_own	married	married_snp	separated	divorced

## Introduction
In this lab we will be using our skills from flask, dash, pandas, and sqlalchemy to create a dashboard that contains graphs that we can manipulate to show data based on our input. We will be working with a very large dataset containing information on rent and population demographics in the US. We will be using the ETL pattern to create extract, format (or transform), and enter (or load) our data into our database. Let's get started!

## Objectives
* Instruct to create package directory with __init__.py and instantiate App, and make run file
* Instruct to set up database -- import Sqlalchemy and create models -- create_all in terminal
* Instruct to use pandas to read the excel file & fillna with 0.0
* Walk through ETL Pattern -- uses the data, database, and models to bring information over to our program and easier to use/query
* Once database is setup and populated, instruct to create a layout that uses a callback to populate a div's children with a bar graph that has each city's population for a given state
* then instruct to add similar graph to layout but with each city's mean_rent

## Setting Up a New Dash App

First things first. We will need to structure our app and get just our baseline dash app running. We already have our package directory with the name of our app (lesson), `dashaltogethernow`. We also already have our excel file with the data we will be working with, `real_estate_db.xlsx`. Our package should have an `__init__.py` file that imports dash and instantiates a new app with a `url_base_pathname` of `'/dashboard'`. Next, we will need to create our run file in our top-level directory which starts the server for us with debug mode assigned to True.

Your directory should look something like this:
```python
├── CONTRIBUTING.md
├── LICENSE.md
├── README.md
├── dashaltogethernow
│   ├── __init__.py
│   ├── real_estate_db.xlsx
├── index.ipynb
├── requirements.txt
└── run.py
```

## Connecting Sqlalechemy and Database Set-up

Now that we have our app set up and we are able to run it in the browser, we need to turn our attention to getting our database configured. First, we will need to import sqlalchemy and then tell our database where to store its data. We will need to configure our app's server to save our data to a local sqllite database at `app.db` in our dashaltogethernow package.

After we have configured our server to save its data to the `spp.db` file, we need to create our sqlalchemy database object with our sqlalchemy import and our app's server.

Once we have created our database object, `db`, we will need to create our models. As is convention, we will create our models in a `models.py` file. We will be using 3 models; State, City, Demograhic. The relationships will be that a state **has many** cities and a city **belongs to** a state, a city **has one** demographic and a demographic **belongs to** a city. Below are a list of the attributes we will need for each model and table.

**State** - id, name, state_ab, cities

**City** - id, name, type, zip_code, lat, lng, state, state_id, demographic

**Demographic** - id, population, male_pop, female_pop, mean_rent, pct_own, pct_married, city, city_id



At this point our file tree should now looks like the following:
```python
├── CONTRIBUTING.md
├── LICENSE.md
├── README.md
├── dashaltogethernow
│   ├── __init__.py
│   ├── app.db
│   ├── models.py
│   ├── real_estate_db.xlsx
├── index.ipynb
├── requirements.txt
└── run.py
```

## Creating Database Models

## Summary

Great work! In this lab, we practiced creating a dash app, using both dash corecomponents and dash html components to create a table on our app's dashboard. Then we defined a callback that programmatically sorted our app's table by the selected column from our dropdown element.
