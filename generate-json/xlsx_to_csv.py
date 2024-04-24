"""
Converts all xlsx documents from `/xlsx/` dir
to respective csv format, for further processing.

By default saves new files into `/csv/` dir
as required by [json_generator.py].

CLEAR CSV, OUTPUT, XLS for EACH iteration
"""

import pandas as pd 
import os

modified_count = 0

if not os.path.exists('csv/'):
    os.makedirs('csv/')

for excelFile in os.listdir('xls/'):
    # Read and store content 
    # of an excel file 
    read_file = pd.read_excel('xls/' + excelFile) 

    # Write the dataframe object 
    # into csv file 
    read_file.to_csv('csv/' + excelFile + '.csv', index = None, header=True)
    modified_count += 1

print("\n|------------- CONVERTED {} XLS -> CSV FILES -------------|\n".format(modified_count))
