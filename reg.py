import controls
import infantmortality
import foodprice
import pandas as pd
import numpy as np
from statsmodels.tsa.base.datetools import dates_from_str
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt


# Inputs
# THIS IS WHERE YOU CAN CHANGE THE MODEL
COUNTRIES = ['france', "us", "germany"]
INDEPENDENT_VARS = ['nra_o', 'nra_i', 'vop_prod', 'cte', 'voc_prod', 'nra_covm', 'nra_covx', 'rra', 'tbi', 'ssr', 'shrimp', 'shrexp', 'pop_rural', 'pop_urban', 'cte_dollar_constant', 'gse_constant', 'gdpdeflator']

# BROKEN VARS:
# 'er_econ': 7 datapoints
# The dependent var is currently forced to be Infant Mortality Data until we find better pov data


# Loads in the Mortality Data
dependent_var_obj = infantmortality.InfantMortalityData()
dep_var = dependent_var_obj.get_data(COUNTRIES)

# Loads in the Controls
get_ind_var = controls.Controls()
ind_var_data = {}
found_countries = {}
for var in INDEPENDENT_VARS:
    c, d = get_ind_var.main(COUNTRIES, var, False)
    ind_var_data[var] = d
    found_countries[var] = c

# Imports the Dependent Var
var_formatted = {}
for country in dep_var:
    for yd_tuple in dep_var[country]:
        try:
            var_formatted[country].append([country, yd_tuple[0], yd_tuple[1]])
        except:
            var_formatted[country] = [([country, yd_tuple[0], yd_tuple[1]])]

# Imports the independent variables
used_controls = {}
for ivar in ind_var_data:
    for country in ind_var_data[ivar]:  # now we know country and ivar
        print ivar, country, len(ind_var_data[ivar][country])
        if country.capitalize() in var_formatted:  # if the country is in the good data
            d = ind_var_data[ivar][country]  # Now we are looking the actual data for the country and ivar
            for datum in d:  # individual datum
                for i, tuple1 in enumerate(var_formatted[country.capitalize()]):  # looking at the data tuple
                    if datum[0] == tuple1[1] and country.capitalize() == tuple1[0]:
                        """print datum, tuple1"""
                        try:
                            if ivar not in used_controls[country]:
                                """print '\n\n#################\n'
                                print ivar
                                print '\n################\n\n'"""
                                used_controls[country].append(ivar)
                        except:
                            used_controls[country] = [(ivar)]
                        var_formatted[country.capitalize()][i].append(datum[1])

# Loads in the food price data
food = foodprice.FoodPrice()
food_data = food.get_data()

for country in var_formatted:
    for array in var_formatted[country]:
        for food in food_data:
            for tupl3 in food_data[food]:
                if array[1] == tupl3[0]:
                    array.append(tupl3[1])

#  --------------------
# |                     |
# |    !!START HERE!!   |
# |                     |
#  ---------------------

# Here is the actual VAR
for country in var_formatted:
    # These are the columns of the dataframe, will be displayed
    columns = ['Country', 'Year', 'Dep Var']
    try:
        for cont in used_controls[country.lower()]:
            columns.append(str(cont))
    except Exception as e:
        print 'Country has no controls'

    for food in ['Maize', 'Wheat', 'Barley']:
        columns.append(food)

    # Currently, the VAR runs one country at a time, not sure if we want to change that later
    print 'Doing analysis of: ' + country
    # Creates a general dataframe, sorts by year, then removes year

    df = pd.DataFrame(data=var_formatted[country], columns=columns)
    df = df.sort(['Year'], ascending=[1])
    years = dates_from_str(df['Year'])
    df.index = pd.DatetimeIndex(years)
    # THIS DROPS THE N/A DATA, MIGHT REVISE LATER
    # For example, countries only have like 10 entries sometimes that are perfect
    # However, inputing a zero would skew the results, which is worse than limited data
    # So we will have to make that decision later. currently the model just drops any non-data entries
    df = df.drop('Year', 1).dropna()
    df = df.drop('Country', 1).dropna()

    # Regression engine doesn't like columns of only zeros (or constants), this gets rid of those
    for column in df:
        total = 0
        conse_dupe_counter = 0
        old_val = 0
        for datum in df[column]:
            if datum == old_val:
                conse_dupe_counter += 1
            total += datum
            old_val = datum
        col = df[column]
        if total in [0, 0.0,  0.00, col[0], col[0]*len(col), col[0]*len(col)/len(col)]:
            print 'Dropping column: ' + column
            df = df.drop(column, 1)
        elif conse_dupe_counter > len(df[column])/2:
            df = df.drop(column, 1)
            print '\n\n***********\nToo many duplicates in the: ' + column + ' column\n***********\n\n'

    # Does the VAR model!
    model = VAR(df)
    # This actually fits the model  results of the model. 1 means VAR to one power (just linear)
    # You can change the number to 2 or 3 if you want a non-linear regression
    # We will have to figure out which gives us the best results and then fudge a reason for it
    results = model.fit(1)
    print df
    try:
        print results.summary()
    except Exception as e:
        print e
        # Sometimes printing the regression fails because of a linear algebra error
        # Jen Selby suggested that maybe it cant take the second derivative of the matrix
        # Not sure how we can modify the data to fix this, but maybe we could log everything
        print 'Random LinAlg error that I can\'t fix!'

    # This prints out the cool graphs at the end
    # There is a lot more ways of graphing etc. so we can find better ones these are default
    # If they get annoying you can comment out these last two lines
    """results.plot()
    plt.show()"""
