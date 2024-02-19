## required packages
 - python3 -m pip install pandas
 - python3 -m pip install openpyxl

## Operation Flow
 - generate `.xlsx` file for each section (using WPS Office -> Split Workbook)
 - convert each `.xlsx` file to `.csv` (using `[xlsx_to_csv.py]`)
 - generate required JSON from the script (using `[json_gen.py]`).

## NOTE
 - required folders are created automatically
 - WPS export should be to directory `$py-script-root/xls`
