#importing pandas as pd 
import pandas as pd 
import os

if not os.path.exists('csv/'):
    os.makedirs('csv/')

for excelFile in os.listdir('xls/'):
    # Read and store content 
    # of an excel file 
    read_file = pd.read_excel ('xls/' + excelFile) 

    # Write the dataframe object 
    # into csv file 
    read_file.to_csv('csv/' + excelFile + '.csv', index = None, header=True)
    