import pandas as pd
import os

def split_csv_by_section(input_file, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the CSV file
    df = pd.read_csv(input_file)

    # Get unique values from the Section column
    sections = df['Section'].unique()

    # Split the dataframe by section and save to separate files
    for section in sections:
        # Filter rows for current section
        section_df = df[df['Section'] == section]
        
        # Create output filename
        output_file = os.path.join(output_dir, f'{section}.csv')
        
        # Save to CSV file
        section_df.to_csv(output_file, index=False)
        print(f"Created file: {output_file}")

if __name__ == "__main__":
    # Define input file and output directory
    input_file = "./generate-json/csv/bulk_csv/input.csv"  # Replace with your input file path
    output_dir = "./output/section_wise_csv/"     # Replace with your desired output directory
    
    try:
        split_csv_by_section(input_file, output_dir)
        print("\nProcessing completed successfully!\n")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
