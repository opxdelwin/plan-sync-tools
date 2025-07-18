import os
import json
import re
from pathlib import Path

def process_electives_files(parent_directory):
    """
    Process all electives-scheme files in subdirectories to separate room and time information.
    """
    files_processed = 0
    files_modified = 0
    
    print(f"Starting to process files in directory: {parent_directory}")
    
    # Walk through all directories
    for root, dirs, files in os.walk(parent_directory):
        for file in files:
            if file.startswith("electives-scheme"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                
                try:
                    # Read the JSON file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    files_processed += 1
                    file_modified = False
                    
                    # Process each day in the data
                    if 'data' in data:
                        for day, entries in data['data'].items():
                            if isinstance(entries, list):
                                for entry in entries:
                                    if isinstance(entry, dict) and 'room' in entry:
                                        room_value = entry['room']
                                        
                                        # Check if room contains time format (room / time)
                                        if ' / ' in room_value:
                                            parts = room_value.split(' / ')
                                            if len(parts) == 2:
                                                room_part = parts[0].strip()
                                                time_part = parts[1].strip()
                                                
                                                # Validate time format (HH:MM - HH:MM)
                                                time_pattern = r'\d{2}:\d{2}\s*-\s*\d{2}:\d{2}'
                                                if re.match(time_pattern, time_part):
                                                    # Update the entry structure
                                                    entry['room'] = room_part
                                                    entry['time'] = time_part
                                                    file_modified = True
                    
                    # Save the file if modifications were made
                    if file_modified:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        files_modified += 1
                        print(f"  → Modified: {file}")
                    else:
                        print(f"  → No changes needed: {file}")
                
                except json.JSONDecodeError as e:
                    print(f"  → Error parsing JSON in {file}: {e}")
                except Exception as e:
                    print(f"  → Error processing {file}: {e}")
    
    print(f"\nProcessing complete:")
    print(f"Files processed: {files_processed}")
    print(f"Files modified: {files_modified}")

def main():
    # Get parent directory from user input or use current directory
    parent_dir = input("Enter parent directory path (or press Enter for current directory): ").strip()
    
    if not parent_dir:
        parent_dir = os.getcwd()
    
    if not os.path.exists(parent_dir):
        print(f"Error: Directory '{parent_dir}' does not exist.")
        return
    
    if not os.path.isdir(parent_dir):
        print(f"Error: '{parent_dir}' is not a directory.")
        return
    
    process_electives_files(parent_dir)

if __name__ == "__main__":
    main()
