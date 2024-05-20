import os
import json
import pandas as pd

# Define the paths
input_folder = 'output/events'
output_csv = 'output/summary.csv'

# Initialize a list to store data
data = []

# Initialize app name variable
app_name = None

# Function to extract app name from package
def extract_app_name(package):
    return package.split('.')[-1] if package else "NULL"

# Iterate over all JSON files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        filepath = os.path.join(input_folder, filename)
        
        with open(filepath, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            
            # Extract relevant data from JSON
            event = json_data.get('event', {})
            view = event.get('view', {})
            package = view.get('package', "")
            
            if app_name is None and package:
                app_name = extract_app_name(package)
            
            event_type = event.get('event_type', "NULL")
            resource_id = view.get('resource_id', "NULL")
            text = view.get('text', "NULL")
            signature = view.get('signature', "NULL")
            content_free_signature = view.get('content_free_signature', "NULL")
            event_str = json_data.get('event_str', "NULL")

            # Append data to the list
            data.append({
                'Tag': json_data.get('tag', "NULL"),
                'Event Type': event_type,
                'Package': package if package else "NULL",
                'Resource ID': resource_id,
                'Text': text,
                'Signature': signature,
                'Content Free Signature': content_free_signature,
                'Event String': event_str,
            })

# If no package was found in any file, set a default app name
if app_name is None:
    app_name = "App_Name_Not_Found"

# Create a DataFrame
df = pd.DataFrame(data)

# Create headers
headers = ['Tag', 'Event Type', 'Package', 'Resource ID', 'Text', 'Signature', 'Content Free Signature', 'Event String']

# Add app name at the top
app_name_row = pd.DataFrame([[app_name] + [''] * (len(headers) - 1)], columns=headers)
df = pd.concat([app_name_row, df], ignore_index=True)

# Separate attributes with space and ||
df = df.applymap(lambda x: str(x).replace(',', ' ').replace('||', ' '))

# Save the DataFrame to CSV
df.to_csv(output_csv, index=False, header=headers)

print(f'CSV file has been created at {output_csv}')
