# -*- coding: utf-8 -*- 


'''
Script to generate batch file to feed multiple runs of the EPA 
CO-Benefits Risk Assessment Health Impacts Screening and Mapping Tool (COBRA)
with different county-level emissions data.
COBRA Tool url:
https://www.epa.gov/cobra

This makes it easier to estimate cumulative emissions reduction health impacts
for a series of years and/or different discount rates, for example.

For more information about COBRA's batch file capability see the user manual,
Appendix G:

https://www.epa.gov/sites/default/files/2018-05/documents/cobra_user_manual_may2018_508.pdf

NOTE: This is could be refactored and made into a function but this was a one-off task so 
I did not do this.
'''


import os


# Variables:
# edit these based on the file you want to generate
cd = os.getcwd()

# example input data file name: baseline\s2022.csv"
# location of the baseline emissions data
baseline_dir = os.path.join(cd,"baseline")
# location of the control emissions data
control_dir = os.path.join(cd,"control")
# directories where you want COBRA to save output
# under different discount rates
results_dir_3pct =  os.path.join(cd,"dr3pct") 
results_dir_7pct =  os.path.join(cd,"dr7pct") 
# name of the batch file to output from this script
batch_file = "example_cobra_run.bat" 
# optional: prefix for input file names:
file_prefix = 's'

# start and end years for the emissions files
# these are part of the emission file names
start_year = 2022
end_year = 2049

pop_incidence_year = 2023 # Options: 2016, 2023, 2028
use_closest_default = False

# Constants used in contructing the batch commands
# pointers
program = "\"C:\Program Files\COBRA\cobra_console.exe\" " 
db_arg = '--db '
db3 = "\"C:\Program Files\COBRA\data\cobra.db\" "
db7 = "\"C:\Program Files\COBRA\data\cobra7pct.db\" "
# args
bl_arg = "--baseline "
control_arg = ' --control ' 
out_arg = ' --output '
pct_arg = r" --pct3 " 
year_arg = r"--year "



# make file paths

yr_range = [str(i) for i in range(2022, end_year+1)]  # range of years 
nyrs = len(yr_range)
file_names = [file_prefix +i+'.csv' for i in yr_range]


# this is clunky but each file path needs to be formatted with double quotes for Windows

blfp = [baseline_dir+"\\"+i for i in file_names]
blfp = ['"{}"'.format(i) for i in blfp]

ctrlfp = [control_dir+"\\"+i for i in file_names]
ctrlfp = ['"{}"'.format(i) for i in ctrlfp]

outfp3 = [results_dir_3pct+"\\"+i for i in file_names]
outfp3 = ['"{}"'.format(i) for i in outfp3]

outfp7 = [results_dir_7pct+"\\"+i for i in file_names]
outfp7 = ['"{}"'.format(i) for i in outfp7]



if use_closest_default:
	input_year = [] 
	yr_range = [i for i in range(2022, 2050)]  
	years = [2016, 2023, 2028]
	for i in yr_range:
		diffs = [abs(j-i) for j in years]
		min_diff = min(diffs)
		min_diff_index = diffs.index(min_diff)
		closest_year = years[min_diff_index]
		input_year.append(closest_year)
		input_year = [str(i) for i in input_year] 

else:
	input_year = [str(pop_incidence_year) for i in yr_range]


# write results: first 3 % DR and append 7 % DR

# 3%
batch_lines = [program + db_arg + db3  + bl_arg + blfp[i] + control_arg + ctrlfp[i] + out_arg + outfp3[i]+ pct_arg + str("yes ")  + year_arg + input_year[i] + '\n\n'  for i in range(nyrs)]
f = open(batch_file, 'w')
f.writelines(batch_lines)
f.close()

# 7%
batch_lines = [program + db_arg + db7  + bl_arg + blfp[i] + control_arg + ctrlfp[i] + out_arg + outfp7[i]+ pct_arg + str("no ")  + year_arg + input_year[i] + '\n\n'  for i in range(nyrs)]
f = open(batch_file, 'a')
f.writelines(batch_lines)
f.close()

