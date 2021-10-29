# -*- coding: utf-8 -*- 

#%%
import os


#%%

#%%
# Variables:
# edit these based on the file you want to generate
cd = os.getcwd()

baseline_dir = os.path.join(cd,"baseline")
control_dir = os.path.join(cd,"control")
results_dir_3pct =  os.path.join(cd,"dr3pct") 
results_dir_7pct =  os.path.join(cd,"dr7pct") 

batch_file = "cobra_run.bat" 

file_prefix = 's'

#%%

#%%


#%%

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


# this is clunky but each file path needs to be formatted with double quotes

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

