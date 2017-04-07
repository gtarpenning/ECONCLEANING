import controls
import infantmortality
import pandas as pd
import numpy as np
from statsmodels.tsa.base.datetools import dates_from_str
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt


# Inputs
COUNTRIES = ['france', "us", "germany", 'brazil', 'canada']
CONTROLS = ['nra', 'nra_nch', 'nra_covm', 'nps', 'ssr', 'vop_covt']
INDEPENDENT_VAR = 'nra_o'


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

# Formats the data for a dataframe


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


used_controls = []
for control in control_data:
    for country in control_data[control]:
        if country.capitalize() in var_formatted:
            d = control_data[control][country]
            for datum in d:
                for i, tuple1 in enumerate(var_formatted[country.capitalize()]):
                    if datum[0] == tuple1[1] and country.capitalize() == tuple1[0]:
                        if control not in used_controls:
                            used_controls.append(control)
                        var_formatted[country.capitalize()][i].append(datum[1])


columns = ['Country', 'Year', 'Dep Var', "Ind Var"]
for cont in used_controls:
    columns.append('Control: ' + str(cont))

for country in var_formatted:
    print 'Doing analysis of: ' + country
    df = pd.DataFrame(data=var_formatted[country], columns=columns)

    years = dates_from_str(df['Year'])
    df.index = pd.DatetimeIndex(years)

    # THIS DROPS THE NA DATA, MIGHT REVISE LATER
    df = df.drop('Year', 1).dropna()
    df = df.drop('Country', 1).dropna()

    print df

    model = VAR(df)

    results = model.fit(1)
    try:
        print results.summary()
    except:
        print 'Random LinAlg error that I can\'t fix!'

results.plot()
plt.show()



# lol = pd.DataFrame(dep_var.values(), index=pd.MultiIndex.from_tuples(dep_var.keys()))
