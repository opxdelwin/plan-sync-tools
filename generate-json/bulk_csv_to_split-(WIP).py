import csv
import os

def split_csv(input_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the headers
        
        current_section = None
        current_rows = []
        
        for row in reader:
            if row == [''] * len(headers):  # Check for ",,,,,,,,,,," row
                if current_section:
                    # Write the current section's data
                    write_section_to_file(current_section, headers, current_rows, output_folder)
                    current_section = None
                    current_rows = []
            elif row and any(field.strip() for field in row):
                # Non-empty row
                if row[1] and row[1] != current_section:  # Check if this row starts a new section
                    current_section = row[1].replace("-", "")  # Remove hyphen for filename
                    current_rows = [row]
                else:
                    current_rows.append(row)
        
        # Write the last section if there's any data left
        if current_section:
            write_section_to_file(current_section, headers, current_rows, output_folder)

def write_section_to_file(section, headers, rows, output_folder):
    output_file = os.path.join(output_folder, f'{section}.csv')
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(headers)  # Write headers
        writer.writerows(rows)
    print(f"Created {output_file}")

# Usage
input_file = 'C:/code/plan-sync-tools/generate-json/csv/SEM 3, CSE, EFF 24_07_24.csv'  
output_folder = 'C:/code/plan-sync-tools/generate-json/csv/output/'  

split_csv(input_file, output_folder)