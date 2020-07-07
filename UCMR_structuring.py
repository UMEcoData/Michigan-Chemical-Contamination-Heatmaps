
import pandas as pd
import numpy as np
import os

##: EDIT: Edit this file to be the UCMR you have chosen
ucmr_file = "UMCR4_All_MichiganOnlyData.csv"
zipcode_file = "UCMR4_ZipCodes_csv.csv"

#get the working directories for this code
input_direc = os.getcwd() + "/input/"
output_direc = os.getcwd() + "/output/"


#Read in the original file - change directory name to yours with the csv file in it
contaminant_data = pd.read_csv((input_direc + ucmr_file) , encoding = "ISO-8859-1")



#EDIT: only for ucmr 4 formatting --- COMMENT OUT IF NOT UCMR 4
contaminant_data = contaminant_data.rename(columns={"AnalyticalResultValue(µg/L)":"AnalyticalResultValue"})



#EDIT: Uncomment below code to only select for the rows for Michigan
#contaminant_data = contaminant_data[contaminant_data.State.str.contains("MI")]




#EDIT: Remove the extraneous columns we don't need
#UCMR2
#contaminant_data = contaminant_data.drop(['Size', 'FacilityName','SamplePointName', 'SamplePointType', 'MethodID', 'MonitoringRequirement', 'SampleEventCode', 'DisinfectantType'], axis=1)
#UCMR3
#contaminant_data = contaminant_data.drop(['Size', 'FacilityName','SamplePointName', 'SamplePointType', 'MethodID', 'MonitoringRequirement', 'SampleEventCode'], axis=1)
#UCMR4
contaminant_data = contaminant_data.drop(['Size', 'FacilityName','SamplePointName', 'SamplePointType', 'MethodID', 'MonitoringRequirement', 'SampleEventCode'], axis=1)





#create a new dataframe that only has values of contaminants over significance level
new_data = contaminant_data[~contaminant_data.AnalyticalResultsSign.str.contains("<" , na=False)]





#EDIT: read in the zipcodes to a dataframe - change directory name to yours with the csv file in it
#UCMR 2 or 3
#zipcodes = pd.read_csv(input_direc + zipcode_file)
#UCMR 4
zipcodes = pd.read_csv(input_direc + zipcode_file)




#connect the zipcodes to our previous dataframe to create our combined dataframe of full_data with zipcodes to contaminant levels
full_data=pd.merge(new_data,zipcodes, on='PWSID', how="inner")




#EDIT: Uncomment the below code to grab singular PFAS contaminants and store in data frame, you can edit contaminant names in line below
#PFAS_triggers = ["PFOS", "PFOA", "PFNA", "PFHxS", "PFHpA", "PFBS"]
#full_data = full_data[full_data["Contaminant"].isin(PFAS_triggers)]



#generate the counts of each contaminant
counts = full_data.groupby(['Contaminant']).count()




#EDIT: Uncomment the code to generate the counts of each state
#state_counts = full_data.groupby(['State']).count()


#change directory to ouput folder for  csv
os.chdir('output_direc')


#EDIT: Save your full data as well as the counts into their own csv files
full_data.to_csv('Michigan_UCMR4.csv')
counts.to_csv('Michigan_UCMR4_counts.csv')
#state_counts = ('Full_UCMR3_state_counts.csv')