import os
import csv
import re

pattern1 = r"(/Barbie/[^/]+/[^/]+/[^/]+)"
pattern2 = r'(/Barbie/[^/\s]+/[^/\s]+/[^/\s]+)'

extracted_xytech_directories = [] 
extracted_baselight_directories = []

# Define the file name
baselight = 'Baselight_export.txt'
xytech = 'Xytech.txt'

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the file
baselight_path = os.path.join(script_dir, baselight)
xytech_path = os.path.join(script_dir, xytech)


# Baselight import
with open(baselight_path) as f:
    baselight_contents = f.readlines()
# <null> and <err> text are ignored
errors = ['<err>', '<null>']
# empty array for later use
noerr_baselight_contents = []
for line in baselight_contents:
    for error in errors:
        # in a line in baselight_contents, if there is an error from errors[]
        # replace with blank space
        line = line.replace(error, '')
    line = line.strip()
    noerr_baselight_contents.append(line)

# Iterate through the list of file paths
# Plan here is to remove them so they are comparable with Xytech file later
for file_path_with_numbers in noerr_baselight_contents:

    # Use re.findall to extract all matching directory paths in the entry
    matches = re.findall(pattern2, file_path_with_numbers)
    
    # Join the extracted directory paths into a single string
    extracted_directory = ' '.join(matches)
    
    # Append the extracted directory to the list
    extracted_baselight_directories.append(extracted_directory)

# Extracted_baselight_directories = W/O File Path & NUMBERS








#Xytech import
with open(xytech_path) as f:
  xytech_contents = f.readlines()
# empty array for later (w/o errs)
noerr_xytech_contents = []
# Initialize a flag to indicate whether to start extracting data (This is done because there are work orders in file too)
extract_data = False

# Initialize a list to store the extracted data
extracted_xytech_data = []

for line in xytech_contents:
    # We only want the filepath after this fact and before "Notes:""
    if "Location:" in line:
        extract_data = True  # Set the flag to True when the marker is found
    elif "Notes:" in line:
        extract_data = False 
    elif extract_data:
     # Append lines to the result when the flag is True
        for error in errors:
            line = line.replace(error, '')
        line= line.strip()
        extracted_xytech_data.append(line)



# Need to display workorder on CSV too, I thought best way to do this was to do it separately in a diff. dataset
with open(xytech_path) as f:
  xytech_workorder = f.readlines()
# The phrases which indicate what is needed
extract_workorder = ["Xytech Workorder", "Producer", "Operator", "Job", "Notes"]
# Notes is separated into another line so this is needed for later use
notes_line = []
matching_lines = []
found_notes = False

for line in xytech_workorder:
    # Looking for matching 
    if any(phrase in line for phrase in extract_workorder):
        matching_lines.append(line)
    if "Notes:" in line:
        found_notes = True
        continue
    if found_notes:
        notes_line.append(line)
# Combine the two
if notes_line:
    extracted_lines = matching_lines + notes_line
else:
    extracted_lines = matching_lines


# Initialize a list to store the extracted directory parts

# Iterate through the array of file paths
for file_path in extracted_xytech_data:
    # Use re.search to find the matching part of the directory
    match = re.search(pattern1, file_path)

    # Extract the desired directory if a match is found
    if match:
        desired_directory = match.group(1)
        # Append the extracted directory to the list
        extracted_xytech_directories.append(desired_directory)




# goal is to compare extracted_directories and baselight export

# Things I need to implement
# Computation done to match shareholder request

# Main goal - Look at Xytech file (these are shots that need fixing)
# Compare with Baselight_export and find out what ranges need to be fixed - (PER LINE) (NO NUMBER SKIPPING)


# Export to CSV file ('/' indicates new column) *done* 


csv_file = "testing.csv"
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)

    for item in extracted_lines:
         row = item.split('/')
         writer.writerow(row)

    for item in extracted_xytech_directories:
            row = item.split('/')
            writer.writerow(row)

    # Line 1 will be Producer / Operator  / job / notes (Take these from xytech - Maybe grab these from file with Keywords? 

   # Line 4 frames to fix ranges 


   # for row in xytech_contents:
   #     writer.writerow(row)

