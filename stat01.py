########################################################################################################################
# Program: stat01.py
# Project: Python Training
# Author: Josh Taylor, Greylock Mckinnon Associates
# Last Edited: 6/23/15
########################################################################################################################

from __future__ import division
import pandas as pd
import pandas.stats.plm as plm
import numpy as np
import statsmodels.formula.api as sm
from statsmodels.sandbox.regression import gmm
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import timeit


#path to this file: "C:\Users\jtaylor\Projects\Training\Python\Code\stat01.py"


# Import census data
pums = pd.read_table("C:\Users\jtaylor\Projects\Training\Python\Data\ds_test_final.txt")

#clean the data
pums['twoWorkers'] = (pums['fes'] == 1) + 0
pums['black'] = (pums['rac1p'] == 2) + 0
pums['otherRace'] = (pums['rac1p'] > 2) + 0
pums['male'] = (pums['sex'] == 1) + 0
pums['dis'].replace(2,0,inplace = True)
pums['hicov'].replace(2,0,inplace = True)
pums['fs'].replace(2,0, inplace = True)
for i in range(len(pums['hincp'])):
    if pums.loc[i,'hincp'] < 1 or pums.loc[i,'hincp'] == np.nan:
        pums.loc[i, 'hincp'] = 1


#create a linear model that describes logIncome
pums['logIncome'] = np.log(pums['hincp'])

startOLS = timeit.default_timer()
incomeOLS = sm.ols(formula = 'logIncome ~  agep + dis + wif + fs + noc +  pap + black + otherRace + male + wkhp + C(st) ',
                data = pums, missing='drop').fit()
stopOLS = timeit.default_timer()
timeOLS = stopOLS - startOLS
print "Run time to fit this model: %s S" % timeOLS
print incomeOLS.summary()
incomeOLSText = incomeOLS.summary().as_text()
incomeOLSTable = file("C:\Users\jtaylor\Projects\Training\Python\Charts and Tables\Python, Income OLS.txt", 'w')
incomeOLSTable.write(incomeOLSText)
incomeOLSTable.close()
print
print "The model with robust standard errors"
incomeOLSRobustSE = incomeOLS.get_robustcov_results(cov_type='HC0', use_t=True)
print incomeOLSRobustSE.summary()
incomeOLSRobustSEText = incomeOLSRobustSE.summary().as_text()
incomeOLSRobustSETable = file("C:\Users\jtaylor\Projects\Training\Python\Charts and Tables\Python, Income OLS Robust.txt", 'w')
incomeOLSRobustSETable.write(incomeOLSRobustSEText)
incomeOLSRobustSETable.close()


#Create a logit model that describes the likelihood of being insured
print
print "Testing out the logit function in python"
print
startLogit = timeit.default_timer()
insureLogit = sm.logit(formula = 'hicov ~ agep + dis + fs + black + otherRace + male  + hincp',
                       data=pums, missing='drop').fit()
stopLogit = timeit.default_timer()
print "Run time to fit this model is: %s S" % (stopLogit - startLogit)
print insureLogit.summary()
insureLogitText = insureLogit.summary().as_text()
insureLogitTable = file("C:\Users\jtaylor\Projects\Training\Python\Charts and Tables\Python, Insure Logit.txt", 'w')
insureLogitTable.write(insureLogitText)
insureLogitTable.close()


#Use IV regression to estimate a model
housing = pd.read_csv("C:\Users\jtaylor\Projects\Training\Python\Data\housing.csv")
housing['west'] = housing['region'] == "West"
housing['south'] = housing['region'] == "South"
housing['ne'] = housing['region'] == 'NE'
housing['constant'] = 1
stopIV = timeit.default_timer()
housingIV = gmm.IV2SLS(housing['rent'], housing[['hsngval', 'pcturban', 'constant']], instrument= housing[['pcturban', 'faminc', 'west', 'south', 'ne', 'constant']]).fit()
stopIV = timeit.default_timer()




#Use panel data models to explain ticket pricing on airline routes

airline = pd.read_csv("C:\Users\jtaylor\Projects\Training\Python\Data\Airline.csv")
airline['constant'] = 1
airline = airline.set_index(['route', 'time'])
airlinePanel = airline.to_panel()
startRE = timeit.default_timer()
airlineRE = plm.PanelOLS(y = airlinePanel['lnMktfare'], x=airlinePanel[['constant', 'mktdistance', 'passengers', 'percentAA', 'percentAS',
                'percentDL', 'percentHA', 'percentNK', 'percentUA', 'percentUS', 'percentWN']],
                time_effects=True, dropped_dummies=True, verbose=True)
stopRE = timeit.default_timer()
print "The RE model ran in %s" % (stopRE - startRE)
print airlineRE
# airlineRETable = file("C:\Users\jtaylor\Projects\Training\Python\Charts and Tables\Python: Random Effects.txt", 'w')
# airlineRETable.write(airlineRE)
# airlineRETable.close()



startFE = timeit.default_timer()
airlineFE = plm.PanelOLS(y = airlinePanel['lnMktfare'], x=airlinePanel[['constant', 'mktdistance', 'passengers', 'percentAA', 'percentAS',
                'percentDL', 'percentHA', 'percentNK', 'percentUA', 'percentUS', 'percentWN']],
                entity_effects=True, time_effects=True, dropped_dummies= True, verbose=True)
stopFE = timeit.default_timer()
print
print "The FE model ran in %s" % (stopFE - startFE)
print airlineFE
# airlineFETable = file("C:\Users\jtaylor\Projects\Training\Python\Charts and Tables\Python: Fixed Effects.txt", 'w')
# airlineFETable.write(airlineFE)
# airlineFETable.close()


