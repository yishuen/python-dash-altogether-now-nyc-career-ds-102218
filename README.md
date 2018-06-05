
# Dash with Tables Lab

UID	BLOCKID	SUMLEVEL	COUNTYID	STATEID	state	state_ab	city	place	type	primary	zip_code	area_code	lat	lng	ALand	AWater	pop	male_pop	female_pop	rent_mean	rent_median	rent_stdev	rent_sample_weight	rent_samples	rent_gt_10	rent_gt_15	rent_gt_20	rent_gt_25	rent_gt_30	rent_gt_35	rent_gt_40	rent_gt_50	universe_samples	used_samples	hi_mean	hi_median	hi_stdev	hi_sample_weight	hi_samples	family_mean	family_median	family_stdev	family_sample_weight	family_samples	hc_mortgage_mean	hc_mortgage_median	hc_mortgage_stdev	hc_mortgage_sample_weight	hc_mortgage_samples	hc_mean	hc_median	hc_stdev	hc_samples	hc_sample_weight	home_equity_second_mortgage	second_mortgage	home_equity	debt	second_mortgage_cdf	home_equity_cdf	debt_cdf	hs_degree	hs_degree_male	hs_degree_female	male_age_mean	male_age_median	male_age_stdev	male_age_sample_weight	male_age_samples	female_age_mean	female_age_median	female_age_stdev	female_age_sample_weight	female_age_samples	pct_own	married	married_snp	separated	divorced

## Introduction
In this lab we will practice creating data tables and other elements in Dash. We will then introduce defining callbacks and practice using one to manipulate our table's data.

## Objectives
In package dir, create init.py with app, slqlalchemy hookup, and necessary imports
create models.py, routes.py, & etl.py
in terminal, create tables in the database
create etl functions that create instances in the database
display information in table & graph

## Reading Our Data

The first thing we need to do is read our excel file `ramenPhoSobaInterest.xlsx` and extract the data we need to populate our table in dash. To do that, we will import pandas and use the `read_excel` function, which takes at least one argument, the path to the excel file, and multiple optional arguments such as a list of the column `names`. For more information on how this function works, refer to the documentation [here](http://pandas.pydata.org/pandas-docs/version/0.20.2/generated/pandas.read_excel.html)

```python
# in the food_interest_data.py file
# importing pandas module to read the excel file and extract the data
import pandas
# using pandas to read the excel file  and giving the names of the columns
excel_data = pandas.read_excel('FILE PATH', names=["Country", "Pho", "Ramen", "Soba"])

# removing the first line of data that contains the headers
# and returning the remating data in a list of dictionaries
data = excel_data.to_dict('records')[1:]
```

Once we have our data, which is a list of dictionaries, which each contain the country and the percentage representing how many google searches were made for Pho, Ramen, or Soba, we can import it to our __init__.py file where we are creating the app's layout and table.

## Creating a Data Table with Dash

Now that we have our information we can begin making our layout. 

Unlike graphs, tables are HTML elements. So, we will add a table to our layout by using the dash_html_components module. So we will need to make sure we first import dash, then dash_html_corecomponents, and our data from the `food_interest_data.py` file. Since we are keeping up with our package structure for our dash app our imports for other files will follow the `from [PACKAGE NAME].[FILE NAME] import [OBJECT NAME]` format. So, to import our `data` our imports will look like the following:

```python
import dash
import dash_html_components as html

from dashwithtables.food_interest_data import data
```

Then, we will instantiate our new instance of our dash app and give it a url_base_pathname of '/', as a good practice so we signal to ourselves and other developers where we would like for our dashboard to display.

```python
app = dash.Dash(__name__, url_base_pathname='/')
```

Let's add our layout! We will want an `h3` tag that reads `"Interest in Pho, Ramen, and Soba by Country according to Google Search from 01/2004 - 06/2018"`, and beneath that we will want our table.

Tables are easy to instantiate. We simply use html.Table(`children=[SOMECODE]`). Tables have several rows, the first of which is the header for the rest of the table, or the name of the columns. Since each dictionary has the name of the column pointing to its value `{'Country': 'Japan', 'Pho': 0.04, 'Ramen': 0.72, 'Soba': 0.24}` we, can create a function that will create the header row for us. Let's define a function called `generate table` that will create the dash html components and rows we need for our table. We can then call this function in our layout, to, well... generate the table! Remember to give it an argument that is the data we are importing from our `food_interest_data` file. We can give this function a default argument of our data object. 

```python
def generate_table(table_data=data):
html.Tr(id='food-table', children=[html.Th(col) for col in dataframe[0].keys()])]
```

First we create a table row (i.e. `html.Tr`). Then we are creating the children for that first row, which will be the table headers (i.e. `html.Th`). To get each column name as a table header we can use one element from our list of data and get the keys (i.e. `data[0].keys()`). Then we use list compresion to push each new table header into the array of children for the first row.

If we look at our table now, it should look something like the folling:

> <h3>Interest in Pho, Ramen, and Soba by Country according to Google Search from 01/2004 - 06/2018</h3>
> <table>
    <tr>
        <strong><th>Country</th><th>Pho</th><th>Ramen</th><th>Soba</th></strong>
    </tr>
</table>

We made this first row somewhat manually since there is only one. However, we aren't sure how many other rows there are in total. So, we're probably better off creating a list of table rows similar to how we made the table columns, using list comprehension:

```python
# creating a table row for each dictionary in our list of data
[html.Tr(children=[somecode]) for data_dict in data]
```

We haven't yet told our table rows what they are going to contain. They aren't going to contain table headers, since they aren't going to be the first row. They will contain table cells or table data (i.e. html.Td(`[somecode]`)). 

```python
# creating a table row for each dictionary in our list of data
[html.Tr(children=[html.Td(data_dict['country']), html.Td(data_dict['Pho']), html.Td(data_dict['Ramen']), html.Td(data_dict['Soba'])]) for data_dict in data]
```

Our first naive approach might be to do the above. We have seen what the data looks like and know there are 4 columns and we can just create four table data elements for each row and get the value from our dictionary by hardcoding the names of each key like we do above. However, if we wanted to make this code a but more re-usable and programmatic, we would need to change this. Plus, if our excel ever changes by adding a column or just changing one of the column names, we would have to then change this function. So, let's see how we could make this more programmatic.

```python
# creating a table row for each dictionary in our list of data
[html.Tr(children=[html.Td(data_dict[column]) for column in data_dict.keys()]) for data_dict in data]
```

Above we are creating a dictionary keys (`dict_keys`) object and iterating over each element, which represent the name of each key in the dictionary, and using it to create a table cell with the value from each key or column with list comprehension. Now, our code is not only more concise, but it is autmatically generating a table cell for each column in the table and accurately giving it the value of that cell. 

This should create all the cells we need for our table. However, we have headers in a list too, so, if we keep our code as is, we will get an error since we will have our table's children attribute pointing to two separate lists. To fix this we will need to combine these lists into one. One way of combining lists is simply adding the two together. So, we simply need to add a `+` between our two lists.

Now, if we look at our dashboard in the browser we should have a fully filled-in table!

> <h3>Interest in Pho, Ramen, and Soba by Country according to Google Search from 01/2004 - 06/2018</h3>
> <table>
    <tr>
        <strong><th>Country</th><th>Pho</th><th>Ramen</th><th>Soba</th></strong>
    </tr>
    <tr><td>Japan</td><td>0.04</td><td>0.72</td><td>0.24</td></tr>
    <tr><td>Taiwan</td><td>0.04</td><td>0.91</td><td>0.05</td></tr>
    <tr><td>Singapore</td><td>0.16</td><td>0.74</td><td>0.1</td></tr>
    <tr><td>Hong Kong</td><td>0.14</td><td>0.75</td><td>0.11</td></tr>
    <tr><td>Philippines</td><td>0.18</td><td>0.78</td><td>0.04</td></tr>
    <tr><td>Canada</td><td>0.6</td><td>0.34</td><td>0.06</td></tr>
    <tr><td>United States</td><td>0.51</td><td>0.45</td><td>0.04</td></tr>
</table>

## Creating a Callback Function in Dash

Great, we now have a table that is displaying the countries and the comparative percentages for whic they query google for Pho, Ramen, and Soba. What if we'd like to sort this information? First we will need to add in a dropdown, which is a dcc component. We can add the following drop down which will give us 4 `options` which are elements that are the children of a dropdown. The options have a `label`, the text you want displayed, and a `value`, the string or other piece of data you want to use to represent that selection. In this case ours will be the same as we will want our drop down selections to indicate the column we want to filter by.

```python
dcc.Dropdown(
        id='sort-by-selector',
        options=[
            {'label': 'None', 'value': None},
            {'label': 'Country', 'value': 'Country'},
            {'label': 'Pho', 'value': 'Pho'},
            {'label': 'Ramen', 'value': 'Ramen'},
            {'label': 'Soba', 'value': 'Soba'}
        ],
        value="Country"
```
Like all other elements, we give the dropdown an `id`. The `value` property will be the starting value for the dropdown.

Now that we have added a dropdown to the top of our app's layout, we can interact with our table by using a callback. A callback is defined using a decorator on the app, similar to a route.

```python
@app.callback(
    # some code goes here   
)
```

Inside our call back, we decide what the callback is going to take in as the value we are looking to change and the output, or where we would like to make our change. Our dropdown is going to have the value by which we want to filter our table, and the table (id='food-table') is going to be the element we want to alter. 

First we will need to import the `Input` and `Output` modules from `dash.dependencies`. So, let's update our imports to include that.

```python
from dash.dependencies import Input, Output
```

Now let's star to fill in our callback function. 

```python
@app.callback(
    Output(component_id='food-table', component_property='children'),
    [Input(component_id='sort-by-selector', component_property='value')]
)
```

First we define which element is going to take the output and which attribute we are going to overwrite. Then we define the input for our callback in a list. Next, we define our function and how we would like to manipulate our data. We will call this function `sort_table` and pass it the an arugment that is going to be the value from the dropdown with the id `sort-by-selector`. We can call this argument whatever we want, but let's name it `input_value` for now.

```python
def sort_table(input_value):
    # some code
```

The input value is going to be the value of whichever `option` we select in our dropdown element. So, our sort logiv will look something like this:

```python
# datum is a single dictionary
# input value represents the value we selected
# we will use this value to access the datum key's value by which we want to sort our data
sorted(data, key=lambda datum: datum[input_value])
```

Lastly, we will pass this sorted data to our `generate_table` function so that we can re-create our newly sorted table.

```python
def sort_table(input_value):
    # using global to make sure we are accessing the imported data object
    global data
    sorted_data = sorted(data, key=lambda datum: datum[input_value])
    return generate_table(sorted_data)
```

Now when we make a selection our table will sort by the selection -- the default is currently by country.

Uh oh! If we look at our terminal we can see that this callback is firing over and over! 

To fix this, we will need to change a bit how we structured things. Instead of calling `generate_table` in our app's layout, we will create a new `html.Div` element named `table-container` that will now recieve the output value of our callback -- which will get invoked once, when the page loads and everytime we make a selection in the dropdown. We then need to update our callback definition's output `id` to be `table-container`. Once we do both of these changes our table should be sorting and our terminal should be working a bit easier.

```python
app.layout = html.Div(children=[
    dcc.Dropdown(
        id='sort-by-selector',
        options=[
            {'label': 'Country', 'value': 'Country'},
            {'label': 'Pho', 'value': 'Pho'},
            {'label': 'Ramen', 'value': 'Ramen'},
            {'label': 'Soba', 'value': 'Soba'}
        ],
        value="Country"
    ),
    html.H3('Interest in Pho, Ramen, and Soba by Country according to Google Search from 01/2004 - 06/2018'),
    html.Div(id='table-container')
])

@app.callback(
    Output(component_id='table-container', component_property='children'),
    [Input(component_id='sort-by-selector', component_property='value')]
)
def sort_table(input_value):
    global data
    sorted_data = sorted(data, key=lambda datum: datum[input_value])
    return generate_table(sorted_data)
```

## Summary

Great work! In this lab, we practiced creating a dash app, using both dash corecomponents and dash html components to create a table on our app's dashboard. Then we defined a callback that programmatically sorted our app's table by the selected column from our dropdown element.
