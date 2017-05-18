import controls
import foodprice
import dep_var
import pandas as pd
import numpy as np
from statsmodels.tsa.base.datetools import dates_from_str
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt
from datetime import datetime as dt
import json
import pickle
import sys

if len(sys.argv) > 1:
    if sys.argv[len(sys.argv)-1].lower() in ['t', 'true', 'y', 'sure', 'force']:
        PICKLE = False
else:
    PICKLE = True


# Inputs
# THIS IS WHERE YOU CAN CHANGE THE MODEL
COUNTRIES = ['argentina']
INDEPENDENT_VARS = ['nra_o', 'vop_prod', 'cte', 'voc_prod', 'nra_covm', 'nra_covx', 'rra', 'tbi', 'ssr', 'shrimp']  # 'shrexp', 'pop_rural', 'pop_urban', 'cte_dollar_constant', 'gse_constant', 'gdpdeflator'
DEPENDENT_VARS = ['21004', '21022', '21029', '210023']  # '21022', 21029, 210023
MASTER_DICT = {}

# BROKEN VARS:2
# 'er_econ': 7 datapoints
# The dependent var is currently forced to be Infant Mortality Data until we find better pov data

print '\n\nStarting process of extracting data and compiling master dictionary... ' + str(dt.now())
start_time = dt.now()


c_2 = []
for c in COUNTRIES:
    c_2.append(c.lower())

COUNTRIES = c_2


"""
Master dict
      |
    country
        |
        ind. var
            |
            year
              |
             ['general/specific', data]
"""


def manual_load_data():
    # Loads in the Controls
    get_ind_var = controls.Controls()
    found_countries = {}
    for var in INDEPENDENT_VARS:
        c, d = get_ind_var.main(COUNTRIES, var, False)
        for country in d:
            try:
                MASTER_DICT[country.lower()]
            except:
                MASTER_DICT[country.lower()] = {}
            for f_var in d[country]:
                try:
                    int(f_var)
                    MASTER_DICT[country.lower()][var] = d[country]
                    print '.',
                    break
                except:
                    MASTER_DICT[country.lower()][f_var] = d[country][f_var]
                    print '.',
        found_countries[var] = c

    # loads in the dependent variable
    sheet = dep_var.Dep_Var()
    d = sheet.get_data()
    for var in DEPENDENT_VARS:
        for country in d:
            if country in COUNTRIES:
                try:
                    MASTER_DICT[country]
                except:
                    MASTER_DICT[country] = {}
                for s_var in d[country]:
                    print var, country, s_var
                    MASTER_DICT[country][s_var] = d[country][s_var]

    # Loads in the food price data
    food = foodprice.FoodPrice()
    food_data = food.get_data()
    for country in MASTER_DICT:
        for food in food_data:
            MASTER_DICT[country.lower()][food] = {}
            for year in food_data[food]:
                try:
                    MASTER_DICT[country.lower()][food][year].append(food_data[food][year])
                except:
                    MASTER_DICT[country.lower()][food][year] = food_data[food][year]

    with open('data.pickle', 'wb') as d:
        pickle.dump(MASTER_DICT, d, protocol=pickle.HIGHEST_PROTOCOL)

    print json.dumps(MASTER_DICT, sort_keys=True, indent=4)
    print '\n\nThe dictionary compiling process took: ' + str(dt.now()-start_time) + ' seconds'


if PICKLE:
    print 'Loading from pickle barrel!'
    with open('data.pickle', 'rb') as raw:
        MASTER_DICT = pickle.load(raw)
    # print json.dumps(MASTER_DICT, sort_keys=True, indent=4)
else:
    manual_load_data()

#  --------------------
# |                     |
# |    !!START HERE!!   |
# |                     |
#  ---------------------

# Here is the actual VAR
for country in MASTER_DICT:
    # Currently, the VAR runs one country at a time, not sure if we want to change that later
    print 'Doing analysis of: ' + country
    # Creates a general dataframe, sorts by year, then removes year
    df = pd.DataFrame(data=MASTER_DICT[country])
    df = df.dropna()  # how='all'
    dates = dates_from_str(df.index)
    df.index = pd.DatetimeIndex(dates)

    # THIS DROPS THE N/A DATA, MIGHT REVISE LATER
    # For example, countries only have like 10 entries sometimes that are perfect
    # However, inputing a zero would skew the results, which is worse than limited data
    # So we will have to make that decision later. currently the model just drops any non-data entries
    # Regression engine doesn't like columns of only zeros (or constants), this gets rid of those
    for column in df:
        pd.to_numeric(df[column])
        total = 0
        conse_dupe_counter = 0
        old_val = 0
        for datum in df[column]:
            try:
                if datum == old_val:
                    conse_dupe_counter += 1
                total += datum
                old_val = datum
            except:
                print 'L'
        col = df[column]
        try:
            if total in [0, 0.0,  0.00, col[0], col[0]*len(col), col[0]*len(col)/len(col)]:
                print 'Dropping column: ' + column + ' because it looks like: '
                print df[column]
                df = df.drop(column, 1)
            elif conse_dupe_counter > len(df[column])/2:
                df = df.drop(column, 1)
                print '\n\n***********\nToo many duplicates in the: ' + column + ' column\n***********\n\n'
        except:
            'LLL'

    # Does the VAR model!

    """for column in df:
        for i, datum in enumerate(df[column]):
            if datum:
                pass
            else:
                print "This column is causing problems!!: " + column + ' in row: ' + str(i)
                answer = raw_input('How would you like to proceed, 1 for drop column, 2 for drop all rows with blanks')
                if answer.lower() in ['1', 'one', 'column']:
                    print 'Dropping column'
                    df.drop(column, 1)
                else:
                    print 'Dropping row(s)'
                    df.drop([1956+i], 0)"""

    df = df.apply(lambda x: x.str.strip() if isinstance(x, str) else x).replace('NaN', np.nan)

    df.dropna(axis=0)

    final_frame = pd.DataFrame(data=df).dropna()
    print df
    # print np.asarray(final_frame)
    model = VAR(final_frame)
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
    """results.plot()
    plt.show()"""
