********************************************************************************
*Program: stat01.do
*Project: Python Training
*Author: Josh Taylor, Greylock McKinnnon Associates
*Last Edited: 6/23/15
********************************************************************************
capture log close
log using "C:\Users\jtaylor\Projects\Training\Python\Code\Log\stat01Log.smcl", append
set more off 
cd "C:\Users\jtaylor\Projects\Training\Python\Charts and Tables"

timer clear

import delimited C:\Users\jtaylor\Projects\Training\Python\Data\ds_test_final.txt, clear 
gen black = rac1p == 2
gen otherRace = rac1p > 2
gen male = sex == 1
replace dis = 0 if dis == 2
replace hicov = 0 if hicov == 2
replace fs = 0 if fs == 2
replace hincp = 1 if hincp < 1
gen logIncome = log(hincp)


timer on 1
reg logIncome agep dis wif fs noc pap black otherRace male wkhp i.st
timer off 1
qui timer list
local time1 = r(t1)
outreg2 using "Stata, Income OLS.rtf", replace ctitle("OLS", "`time1' S") ///
		keep(agep dis wif fs noc pap black otherRace male wkhp)

 
timer on 2
reg logIncome agep dis wif fs noc pap black otherRace male wkhp i.st, robust
timer off 2
qui timer list
local time2 = r(t2)
outreg2 using "Stata, Income OLS.rtf",  ctitle("OLS, Robust SE", "`time2' S") ///
			keep(agep dis wif fs noc pap black otherRace male wkhp)

timer on 3
logit hicov agep dis fs black otherRace male hincp
timer off 3
qui timer list
local time3 = r(t3)
outreg2 using "Stata, Insure Logit.rtf", replace ctitle("Logit", "`time3' s")



use http://www.stata-press.com/data/r13/hsng, clear

timer on 4
ivregress 2sls rent pcturban (hsngval = faminc i.region)
timer off 4
qui timer list
local time4 = r(t4)
outreg2 using "Stata, Housing IV.rtf", replace ctitle("IV", "`time4' s")


import delimited "C:\Users\jtaylor\Projects\Training\Python\Data\Airline.csv", clear
encode route, gen(market)
xtset market time

timer on 5
xtreg lnmktfare mktdistance passengers percent*
timer off 5
qui timer list
local time5 = r(t5)
outreg2 using "Stata, Airline Panel.rtf", replace ctitle("RE", "`time5' s")
 


timer on 6
xtreg lnmktfare mktdistance passengers percent*, fe
timer off 6
qui timer list
local time5 = r(t6)
outreg2 using "Stata, Airline Panel.rtf",  ctitle("FE", "`time6' s")










log close
