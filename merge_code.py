#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os

def merge_data(csv_path, folder_path):
    # Load the CSV data
    model_data = pd.read_csv(csv_path)
    
    # Convert the 'Datetime' column to just date without time
    model_data['Datetime'] = pd.to_datetime(model_data['Datetime']).dt.date

    # Placeholder list for Excel data
    all_excel_data = []

    # Iterate over all Excel files in the given folder
    for file in os.listdir(folder_path):
        if file.endswith(".xlsx"):
            xls_path = os.path.join(folder_path, file)
            xls = pd.ExcelFile(xls_path)
            
            # Iterate over all sheets in the Excel file
            for sheet_name in xls.sheet_names:
                sheet_data = pd.read_excel(xls, sheet_name=sheet_name)
                
                # Extract the ID from the second row of the first column
                sheet_data['ID'] = sheet_data.iloc[1,0]
                
                #print( sheet_data.iloc[1,0])
                #break
                
                # Only append data if the required columns are present
                if all(col in sheet_data.columns for col in ["Station Name", "SO42-", "NO3-", "Date"]):
                    # Convert 'Date' column from 'dd.mm.yyyy' format to 'yyyy-mm-dd'
                    sheet_data['Date'] = pd.to_datetime(sheet_data['Date'], format='%d.%m.%Y').dt.date
                    all_excel_data.append(sheet_data)

    # Concatenate all the sheets' data into one dataframe
    measurements_data = pd.concat(all_excel_data, axis=0, ignore_index=True)

    # Merge the dataframes based on ID and Date
    merged_data = pd.merge(model_data, measurements_data, left_on=['station_id', 'Datetime'], right_on=['ID', 'Date'], how='inner')

    # Select relevant columns
    merged_data = merged_data[['Datetime', 'station_id','site_latitude','site_longitude', 'SO4', 'NO3', 'SO42-', 'NO3-']]
    
    # Save the merged dataframe to a new CSV
    merged_data.to_csv('merged_output_FOUR.csv', index=False)

    print("Data merged and saved to 'merged_output_FOUR.csv'.")

# Specify the path to the CSV and folder containing Excel files
csv_path = '/Users/defne/Desktop/CAMx_Inorganic_extract_2019 2.csv'
folder_path = '/Users/defne/Desktop/psi/Current_data_subset'

merge_data(csv_path, folder_path)

