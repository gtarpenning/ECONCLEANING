import controls
import infantmortality
import pandas as pd
import numpy as np
from statsmodels.tsa.base.datetools import dates_from_str
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt


# Inputs
# THIS IS WHERE YOU CAN CHANGE THE MODEL
COUNTRIES = ['france', "us", "germany", 'brazil', 'canada', 'nigeria', 'greece', 'turkey']
CONTROLS = ['nra', 'nra_nch', 'nra_covm', 'nps', 'ssr', 'vop_covt', 'pop_urban', 'pop_total', 'ac_prod']
INDEPENDENT_VAR = 'nra_o'
# The dependent var is currently forced to be Infant Mortality Data until we find better pov data


# Loads in the Mortality Data
dependent_var_obj = infantmortality.InfantMortalityData()
dep_var = dependent_var_obj.get_data(COUNTRIES)

# Loads in the Controls
controls = controls.Controls()
control_data = {}
found_countries = {}
for control in CONTROLS:
    c, d = controls.main(COUNTRIES, control, False)
    control_data[control] = d
    found_countries[control] = c

found_countries[INDEPENDENT_VAR], ind_var = controls.main(COUNTRIES, INDEPENDENT_VAR, False)

# Imports the Dependent Var
var_formatted = {}
for country in dep_var:
    for yd_tuple in dep_var[country]:
        try:
            var_formatted[country].append([country, yd_tuple[0], yd_tuple[1]])
        except:
            var_formatted[country] = [([country, yd_tuple[0], yd_tuple[1]])]

# Imports the Independent Var
for country in ind_var:
    for yd_tuple in ind_var[country]:
        if country.capitalize() in var_formatted:
            for i, tuple1 in enumerate(var_formatted[country.capitalize()]):
                if yd_tuple[0] == tuple1[1] and country.capitalize() == tuple1[0]:
                    var_formatted[country.capitalize()][i].append(yd_tuple[1])

# Imports the controls
used_controls = {}
for control in control_data:
    for country in control_data[control]:
        if country.capitalize() in var_formatted:
            d = control_data[control][country]
            for datum in d:
                for i, tuple1 in enumerate(var_formatted[country.capitalize()]):
                    if datum[0] == tuple1[1] and country.capitalize() == tuple1[0]:
                        try:
                            if control not in used_controls[country]:
                                used_controls[country].append(control)
                        except:
                            used_controls[country] = [(control)]
                        var_formatted[country.capitalize()][i].append(datum[1])


print used_controls

#  --------------------
# |                     |
# |    !!START HERE!!   |
# |                     |
#  ---------------------

# Here is the actual VAR
for country in var_formatted:
    # These are the columns of the dataframe, will be displayed
    columns = ['Country', 'Year', 'Dep Var', "Ind Var"]
    try:
        for cont in used_controls[country.lower()]:
            columns.append('Control: ' + str(cont))
    except Exception as e:
        print 'Country has no controls'

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
        for datum in df[column]:
            total += datum
        col = df[column]
        if total in [0, 0.0,  0.00, col[0], col[0]*len(col), col[0]*len(col)/len(col)]:
            print 'Dropping column: ' + column
            df = df.drop(column, 1)

    print df
    # Does the VAR model!
    model = VAR(df)
    # This actually fits the model  results of the model. 1 means VAR to one power (just linear)
    # You can change the number to 2 or 3 if you want a non-linear regression
    # We will have to figure out which gives us the best results and then fudge a reason for it
    results = model.fit(1)
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
    results.plot()
    plt.show()
