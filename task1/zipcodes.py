
import pandas as py 
import numpy as np 
import os 

#get user input for zipcode 
zipcode_in = input("Zipcode: ") 

ucmr_file3 = "UCMR3_MichiganDataOnly.csv" 
zipcode_file3 = "UCMR3_ZipCodes_Excel.csv"

#get the working directories for this code 
input_direc = os.getcwd() + "/input/"
output_direc = os.getcwd() + "/output/"

#read in original file - change directory name 
contaminant_data = pd.read_csv((input_direc + ucmr_file3) , encoding = "ISO-8859-1")

#drop extra columns 
contaminant_data = contaminant_data.drop(['PWSName', 'Size', 'FacilityID', 'FacilityName',
                                         'FacilityWaterType', 'SamplePointID', 'SamplePointName',
                                         'SamplePointType', 'AssociatedFacilityID', 'AssociatedSamplePointID',
                                         'SampleID', 'MRL' , 'MethodID' , 'AnalyticalResultsValue',
                                         'SampleEventCode' , 'MonitoringRequirement', 'Region' , 'State'])

#create a new dataframe that only has values of contaminants over significance level
new_data = contaminant_data[~contaminant_data.AnalyticalResultsSign.str.contains("<" , na=False)]

#read in zipcode data
zipcodes = pd.read_csv(input_direc + zipcode_file3)

#merge dataframes 
full_data = pd.merge(new_data,zipcodes, on='PWSID', how="inner")

#get rid of all the row without the input zipcode 
full_data = full_data[~full_data.ZIPCODE.str.contains(zipcode_in)

#keep only the Contaminant and Date 
full_data = full_data.drop(['ZIPCODE', 'AnalyticalResultValue'])

os.chdir('output_direc')

full_data.to_csv("Zipcode_Test3.csv", index = False)
