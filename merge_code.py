import pandas as pd
import os

# Step 1: Read the CSV file into a DataFrame
csv_data = pd.read_csv('final_version_camx.csv')

# Standardize the 'Date' column in the CSV data
csv_data['Date'] = pd.to_datetime(csv_data['Date'], errors='coerce')

# Define the columns to keep from the CSV file
csv_columns_to_keep = ['station_id', 'Date', 'site_latitude', 'site_longitude', 'NO3', 'SO4']

# Filter the CSV data to keep only the required columns
csv_data = csv_data[csv_columns_to_keep]

# Step 2: Iterate over each Excel file
merged_data = pd.DataFrame()  # Create an empty DataFrame to hold merged data

excel_folder = '/Users/defne/Desktop/Current_data_subset'
for file_name in os.listdir(excel_folder):
    if file_name.endswith('.xlsx'):  # Check if the file is an Excel file
        file_path = os.path.join(excel_folder, file_name)
        
        # Read each sheet in the Excel file
        xls = pd.ExcelFile(file_path)
        for sheet_name in xls.sheet_names:
            # Step 3: Read the sheet into a DataFrame
            sheet_data = xls.parse(sheet_name)
            
            # Step 4: Extract the ID (assuming it's in the first cell)
            station_id = sheet_data.iloc[1, 0]
            sheet_data['station_id'] = station_id  # Add the station_id column

            # Standardize the 'Date' column in the sheet data
            sheet_data['Date'] = pd.to_datetime(sheet_data['Date'], errors='coerce')

            
            required_columns = ['station_id', 'Date', 'NO3-', 'SO42-']
            if not all(col in sheet_data.columns for col in required_columns):
               
                continue

            # Keep only the required columns
            sheet_data = sheet_data[required_columns]

            # Step 5: Merge the Excel data with the CSV data based on the common ID and Date
            merged = pd.merge(csv_data, sheet_data, on=['station_id', 'Date'], how='inner')
            
            
            merged_data = pd.concat([merged_data, merged], ignore_index=True)

# Reorder the columns as specified
merged_data = merged_data[['station_id', 'Date', 'site_latitude', 'site_longitude', 'NO3', 'SO4', 'NO3-', 'SO42-']]

# Now 'merged_data' contains the combined data from all Excel sheets and the CSV file with the specified columns
