
import pandas as pd
import numpy as np
import os

#Edit: Choose UCMR file to work with
ucmr_file = "Michigan_UCMR4.csv"

#get the working directories for this code
output_direc = os.getcwd() + "/output/"


#Read in the original file
og_file = pd.read_csv(output_direc + ucmr_file)

# Keep the columns we will need
single_file = og_file[['ZIPCODE', 'AnalyticalResultValue', 'Contaminant', 'CollectionDate']].copy()


#create unique list of contaminants
UniqueCont = single_file.Contaminant.unique()

#create a data frame dictionary to store your data frames
DataFrameDict = {elem : pd.DataFrame for elem in UniqueCont}

for key in DataFrameDict.keys():

    #Turn the ##/##/## dates into just years for every entry
    DataFrameDict[key] = single_file[:][single_file.Contaminant == key]
    DataFrameDict[key]['CollectionDate'] = pd.DatetimeIndex(pd.to_datetime(DataFrameDict[key]['CollectionDate'])).year
    DataFrameDict[key].to_csv("testDataKey")
    

    #Find mean values over a single year within a zipcode
    DataFrameDict[key] =  DataFrameDict[key].groupby(["CollectionDate","ZIPCODE"], as_index=False).mean()
    


    #create unique list of years per contaminant
    UniqueYear = DataFrameDict[key].CollectionDate.unique()


    #create a data frame dictionary to store your data frames
    YearDict = {elem : pd.DataFrame for elem in UniqueYear}


    #create new dataframe to sort out each year within each chemical
    for kay in YearDict.keys():
        YearDict[kay] = DataFrameDict[key][:][DataFrameDict[key].CollectionDate == kay]



    # Set each key in the main dict to store the chemical/years combo
    DataFrameDict[key] = YearDict


#change working directory to the output folder
os.chdir(output_direc + '/chem_files/')



#Create a seperate text file for all the entries in each year per chemical
for key in DataFrameDict.keys():
    for kay in DataFrameDict[key].keys():
    
        #print(kay)
        part1 = "Michigan_UCMR4"
        part2 = ".txt"
        kays = str(kay)
        filename = key + "_" + kays + "_" + part1 + part2
        DataFrameDict[key][kay].to_csv(filename)
