# Cleaning and Vector Auto Regression

This is a repository for the Nueva Senior Econ Thesis Seminar. Griffin and Daniels project requires lots of data cleaning, so they made this Github to store their evolving Python code.

The main use of Python was the implementation of Vector Auto-Regression, a tool to effectively regress time-series data.

# Structure

## The Component Files

### Controls:

The controls file sorts and retrieves indicators from a massive excel file. Use the indicators at the top of the Controls file  to figure out what key-words can be used to return values.

### Dependent Variable:

The dependent variable is currently restricted to *mortality data*, but with the expension of the project will come more dependent variables to choose from. Mortality Data was chosen because of its sensitivity to fluxuations of malnutrition. In the final regression, if Mortality Data is to be used, there will likely need to be a lag between any food price shock and impact.

## The Regression File

The main file is ``` reg.py ``` where all three sources of data are compiled to allow for a compiled VAR. The top of this file is where the model can be changed. 

For example (this is the default currently): 

```
COUNTRIES = ['france', "us", "germany", 'brazil', 'canada', 'nigeria', 'greece', 'turkey']
CONTROLS = ['nra', 'nra_nch', 'nra_covm', 'nps', 'ssr', 'vop_covt', 'pop_urban', 'pop_total', 'ac_prod']
INDEPENDENT_VAR = 'nra_o'
```

While the model only evaluates one country at a time, inputing more than one country will queue the regression results. Exiting from the graph viewing will start the next regression. An example of a simple INPUTS section of the reg.py file would be: 

```
COUNTRIES = ['france', "us"]
CONTROLS = ['nra', 'nra_nch']
INDEPENDENT_VAR = 'nra_o'
``` 
