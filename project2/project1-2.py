import pandas
import numpy























import csv, argparse, pymongo
from datetime import date, datetime
print("Autobots, roll out")
parser = argparse.ArgumentParser(description="Process Baselight and Xytech files")
parser.add_argument("--files", dest="files", nargs="+", help= "Import Baselight or Flames file")
parser.add_argument("--xytech", dest="xytech", help="Path to Xytech file")
# parser.add_argument("--output", dest="output", help="Path to the output CSV file")
parser.add_argument("--c", dest="c", help="Path to the output CSV file")
parser.add_argument("--db", dest="db", action="store_true", help="Path to MongoDB")
parser.add_argument("--verbose", action="store_true", help="Toggle Verbose")
args = parser.parse_args()

import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
first_database = mydb["first_database"]
second_database = mydb["second_database"]

#first_dict = {"User who ran script" : "", "Machine" : "", "User on file:" : "", "Date of file" : "", "Submitted Date:" : ""}
# file_names are broken down into User who ran script: Machine: User on file: Date of file: Submitted Date: 

# to get User who ran script: 

#second_dict = {"User on File" : "", "Date of File" : "", "Location" : "", "Frames/Ranges:" : ""}
# 2nd insert Name of User on File: Date of File: Location: Frame/Ranges: 
import os

xytech = args.xytech
files = args.files
c = args.c
db = args.db

# Xytech import
with open(xytech) as f:
    xytech_file = f.read().splitlines()

with open(xytech) as f:
    xytech_workorder = f.readlines()
# The phrases which indicate what is needed
extract_workorder = ["Xytech Workorder", "Producer", "Operator", "Job", "Notes"]
# Notes is separated into another line so this is needed for later use
notes_line = []
matching_lines = []
found_notes = False
#-------
for line in xytech_workorder:
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


# Baselight import

# Check the value of the "files" argument
    output_data = []

if args.files:
    output_data = []  # Initialize the output_data list

    for file in args.files:
        if "Baselight_" in file:
            if args.verbose:
                print(f"Processing Baselight file: {file}")

            with open(file, "r") as baselight_file:
                for currentReadLine in baselight_file:
                    if args.verbose:
                        print(f"Processing line: {currentReadLine}")

                    parseLine = currentReadLine.split()
                    currentFolder = parseLine.pop(0)
                    parseFolder = currentFolder.split("/")
                    parseFolder.pop(1)
                    newFolder = "/".join(parseFolder)
                    # Use a flag to track if a match was found in xytech_file
                    match_found = False

                    for techfile in xytech_file:
                        if newFolder in techfile:
                            currentFolder = techfile.strip()
                            match_found = True
                            break  # Exit the loop when a match is found

                    if not match_found:
                        continue  # Skip to the next iteration if no match was found

                    # Initialize variables to track the range
                    tempStart = 0
                    tempLast = 0

                    for number in parseLine:
                        if not number.isnumeric():
                            continue

                        number = int(number)

                        if tempStart == 0:
                            tempStart = number
                            tempLast = number
                        elif number == tempLast + 1:
                            tempLast = number
                        else:
                            output_data.append([currentFolder, f"{tempStart}-{tempLast}" if tempStart != tempLast else tempStart])
                            tempStart = number
                            tempLast = number

                    if tempStart != tempLast:
                        output_data.append([currentFolder, f"{tempStart}-{tempLast}"])
                    else:
                        output_data.append([currentFolder, tempStart])

        elif "Flame_" in file:
            if args.verbose:
                print(f"Processing Flames file: {file}")
        
            with open(file, "r") as flames_file:
                for currentReadLine in flames_file:
                    if args.verbose:
                        print(f"Processing line: {currentReadLine}")
                    
                    parseLine = currentReadLine.split()
                    currentFolder = parseLine.pop(1)
                    #print(currentFolder)
                    parseFolder = currentFolder.split("/")
                   #print(parseFolder)
                    #parseFolder.pop(1)
                    #print(parseFolder)
                    #sub_folder = "/".join(parseFolder)
                    #sub_folder = sub_folder.replace("/net/flame-archive Avatar", "")
                    newFolder = "/".join(parseFolder)

                    # Use a flag to track if a match was found in xytech_file
                    match_found = False

                    for techfile in xytech_file:
                        if newFolder in techfile:
                            currentFolder = techfile.strip()
                            match_found = True
                            break  # Exit the loop when a match is found

                    if not match_found:
                        continue  # Skip to the next iteration if no match was found

                    # Initialize variables to track the range
                    tempStart = 0
                    tempLast = 0

                    for number in parseLine:
                        if not number.isnumeric():
                            continue

                        number = int(number)

                        if tempStart == 0:
                            tempStart = number
                            tempLast = number
                        elif number == tempLast + 1:
                            tempLast = number
                        else:
                            output_data.append([currentFolder, f"{tempStart}-{tempLast}" if tempStart != tempLast else tempStart])
                            tempStart = number
                            tempLast = number

                    if tempStart != tempLast:
                        output_data.append([currentFolder, f"{tempStart}-{tempLast}"])
                    else:
                        output_data.append([currentFolder, tempStart])


            with open(file, "r") as flames_file:
                for currentReadLine in flames_file:
                    if args.verbose:
                        print(f"Processing line: {currentReadLine}")



        else:
            print(f"Unsupported file format for file: {file}")

    # Process the output_data as needed after processing all files
else:
    print("No files specified. Please provide files using the --files argument.")

# Write the output data to a CSV file
if args.c:
    with open(c, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(extracted_lines)
        csv_writer.writerows(output_data)

#if args.database:
 #   first_dict["User who ran script"] = os.environ.get('USER', "")
  

# how to get machine name for one line
#zipped_data = list(zip(output_data, files))
#print(zipped_data)
if args.db:
    for file_path in files:
        filename = os.path.basename(file_path)
        split_file_name = filename.split("_")
        machine_file = split_file_name[0] # Machine
        final_file = split_file_name[1]  # Use index 1 to get the user name
        day_files = split_file_name[2].replace(".txt", "")  # Process the date as before
      #  for data in output_data:

    # Create a dictionary for the current data
        first_dict = {
            "User who ran script": os.environ['USER'],
            "Machine": machine_file,
            "User on file": final_file,
            "Date of file": day_files,
            "Submitted Date": str(date.today())
        }

        data_list = []
        data_list.append(first_dict)
        print(data_list)
        first_database.insert_many(data_list)


    # Print the current data
    #print(output_data)
    #print(current_data)
#first_dict = {"User who ran script" : "", "Machine" : "", "User on file:" : "", "Date of file" : "", "Submitted Date:" : ""}
# first_dict[0] = print(os.environ['USER'])
# first_dict[1] = would be the first part of the output_data (split by ("/") - ddnsata3)
# first_dict[2] = would be split filename (Baselight / Flame) by ("/"), and in array pop(1) to get Name
# first_dict[3] = date of file would be also splititng filename into parts ("/") - 20230327 pop(2)
# first_dict[4] = submitted date would just be date_submitted = str(date.today())


    #print(frames)
    
    # Create a dictionary for the current data
    #current_data = {
     #   "Location": location,
       # "Frames/Ranges": frames
    #}

    #print(current_data)
    # Do something with the current_data, like storing it in a list or database

# Process the file data
if args.db:
    for filename in files:
        split_file_name = filename.split("_")
        user_file = split_file_name[1]  # Use index 1 to get the user name
        day_files = split_file_name[2].replace(".txt", "")  # Process the date as before
    
    
    #file_data = {
    #    "User on File": user_file,
     #   "Date of File": day_files
    #}

    #print(file_data)
    
        for machine_data in output_data:
    # Process machine_data as you did before
            location = machine_data[0]
            frames = machine_data[1]

            second_dict = {
            "User on File" : user_file,
            "Date of File" : day_files, 
            "Location" : location, 
            "Frames/Ranges:" : frames}

        #print(second_dict)
    
            data_list = []
            data_list.append(second_dict)
            #print(data_list)
            second_database.insert_many(data_list)

# QUERIES TIME


user_name = "BBonds"

query1 = {
    "User on File": user_name
}

projection = {
    "_id": 0,  # Exclude the _id field
    "User on File": 1,
    "Location": 1,
    "Frames/Ranges:": 1,
}

result1 = second_database.find(query1, projection)

for doc in result1:
    print(doc)

query2 = {
    "Machine": "Flame",
    "Date of File": {"$regex": "202303\\d{2}"}
}

projection2 = {
    "_id": 0,  # Exclude the _id field
    "Machine": 1,
    "User on File": 1,
    "Date of File": 1
}

finished2 = first_database.find(query2,projection2)

for document in finished2:
    print(document)


query4 = {
    "Date of File": {"$regex": "20230323"},
    "Location": {"$regex": "/ddnsata7"}
}

# Define the projection to select specific fields from matching documents
projection4 = {
    "_id": 0,  # Exclude the _id field
    "User on File": 1,
    "Date of File": 1,
    "Location": 1,
    "Frames/Ranges:": 1,
}

# Find and retrieve the matching documents
finished4 = second_database.find(query4, projection4)

# Loop through the matching documents
for document in finished4:
   print(document)


# Define the machine name you want to query
machine_name = "Flame"

# Create the query to find all Autodesk Flame users
query3 = {
    "Machine": machine_name
}

flameusers = first_database.distinct("User on file", query3)
for user in flameusers:
    print("User: " + user)


#print(output_data)
#print(files)
#second_database.insert_many(data_list)

#second_dict = {"Name of user on file" : "", "Date of File" : "", "Location:" : "", "Frames/Ranges:" : ""}
# second_dict[0] = would be split filename (Baselight / Flame) by ("/"), and in array pop(1) to get Name

# second_dict[1] = date of file would be also splititng filename into parts ("/") - 20230327 pop(2)
# second_dict[2] = full file path
# second_dict[3] = ranges

#python3 project1-2.py --files Baselight_JJacobs_20230323.txt Flame_MFelix_20230323.txt Flame_DFlowers_20230323.txt --xytech Xytech_20230323.txt --c 20230323.csv --db

#python3 project1-2.py --files Baselight_TDanza_20230324.txt --xytech Xytech_20230324.txt --c 20230324.csv --db

#python3 project1-2.py --files Baselight_GLopez_20230325.txt --xytech Xytech_20230325.txt --c 20230325.csv --db

#python3 project1-2.py --files Baselight_BBonds_20230326.txt Flame_DFlowers_20230326.txt  --xytech Xytech_20230326.txt --c 20230326..csv --db

#python3 project1-2.py --files Baselight_THolland_20230327.txt Flame_BBonds_20230327.txt --xytech Xytech_20230327.txt --c 20230327.csv --db



# Project 3 Notes
# I'm going to have to convert framing into timecode (another column as well ? Or timecode instead of frame ranges now?)
#
#