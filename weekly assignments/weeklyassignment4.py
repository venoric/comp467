#Attached to the assignment is a test file: lesson4_folderexample.txtDownload lesson4_folderexample.txt
#External clients have added spaces throughout the folder names by: internal workflow conflict, user mistake,etc
#We determined the only issue is that there are spaces, but need to confirm which folders
#Write a script that removed all spaces and reports on console which ones needed fixing and which were fine.

# If there is a .txt file in the folder, read it
# Read entries and remove all whitespace - these changes are reported as an output (Store it somewhere) 
# Whatever didn't need changing - stays the same but still gets reported as an output to console (store it somewhere)


# Define the file name
file_name = '/Users/casey/Desktop/csun/comp467/weeklyassignment4/lesson4_folderexample.txt'
output_file = '/Users/casey/Desktop/csun/comp467/weeklyassignment4/modified_file.txt'

# Open file and put each line into a list called contents
with open(file_name) as f:
    contents = f.readlines()

for line in contents:
    # if has a space then recognize it
    if ' ' in line:
        print("NEEDS FIXING: " + line)
    else:
        print("THIS LINE IS OK:" + line)

with open(output_file, mode="w") as output_file:
    for line in contents:
        if ' ' in line:
        # remove white space 
            line = line.replace(' ', '')
            print("THIS SHIT WORKS NOW: " + line)

        output_file.write(line)


