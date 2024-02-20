# Plan Sync Tools v1

## Preview
This tool helps college faculty convert schedules into the required JSON format for the app. Follow the steps below to use the tool effectively.

## Implementation
Required scripts are written in python, and data are stored in CSV format.

## NOTE
 - required folders are created automatically
 - WPS export should be to directory `$py-script-root/xls`
 - modified and raw schedule data is available under `/data/` directory.

## Operation Flow
 - generate `.xlsx` file for each section (using WPS Office -> Split Workbook)
 - convert each `.xlsx` file to `.csv` (using `[xlsx_to_csv.py]`)
 - generate required JSON from the script (using `[json_generator.py]`).

## Required packages
 - python3 -m pip install pandas

## Workflow (With Demo Data)

<details>
 <summary>1. Formatting required data from college provided schedule</summary>

 - This is an example of schedule data provided to SEM3 students
   <details>
    <summary>See Image</summary>
    
    ![image](https://github.com/opxdelwin/plan-sync-tools/assets/84124091/60ce3076-a623-4e46-9421-ae55bc9e2894)

   </details>

 - Removing blank rows, and repeated headers, newly sanitized file would be so
   <details>
    <summary>See Image</summary>
    
    ![image](https://github.com/opxdelwin/plan-sync-tools/assets/84124091/41b82b92-7a3a-430e-8ef4-28d52f8b9f11)

   </details>
- Note how headers were changed from (as they're required by code)
   - `Day` --> `day`
   - `Section` --> `section`
 
</details>



<details>
 <summary>2. Generating xlsx for each section</summary>

 - Using WPS's Split Sheet by Content, we'll generate separate `.xlsx` files for each section with headers.
   <details>
    <summary>See Image</summary>
    
    ![image](https://github.com/opxdelwin/plan-sync-tools/assets/84124091/99a8b05b-25c0-480e-b48a-d8d8d624c0a1)

    ![image](https://github.com/opxdelwin/plan-sync-tools/assets/84124091/3a29b3af-80f9-474a-b31c-eaabb0936821)

   </details>

 - Note how
   - "My data has headers" is checked
   - "Split Worksheet" is set to "Save as New File"
   - "New Files" are saved to `$python-script/xls` directory
   
 - Click on start and new `.xlsx` for each section would be generated.
</details>



<details>
 <summary>3. Converting `.xlsx` to `.csv` files</summary>

 - `xlsx_to_csv.py` python script can be run to convert all files in `/xls/` directory to `csv` format.
 - New csv files are saved to `/csv/` directory, as required by next script.

 - Note how
   - new directory `/csv/` was created and populated with files.

   <details>
    <summary>See Image</summary>
   
    ![image](https://github.com/opxdelwin/plan-sync-tools/assets/84124091/b401c313-5b0e-4156-9f70-2b11c2f9dd30)

   </details>
</details>



<details>
 <summary>4. Generating JSON files</summary>

- Open `json_generator.py` python script
- Modify `academic_year` and `sem` variables to reflect the schedule we're woring on, (here `2023-2024` and `SEM3` respectievely)
- Run the script.
- All JSON files would be generated at `output/$academic_year/$semester/`
- This JSON can be directly uploaded to Git servers to be used by Plan Sync

<details>
 <summary>See image</summary>

![image](https://github.com/opxdelwin/plan-sync-tools/assets/84124091/107ff1a9-a9db-495f-a156-cf29d1273f8d)

</details>
 
</details>
