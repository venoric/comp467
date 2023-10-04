import os

# Define the file name
file_name = 'ingest_this.txt'

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the file
file_path = os.path.join(script_dir, file_name)


# Open file and put each line into a list called contents
with open(file_path) as f:
    contents = f.readlines()
    print(contents)
# Define a vowel
vowels = ['a','e','i','o','u']
# new list for later use
new_contents = []
# nested loop , file contents -> line -> vowel -> 7
for line in contents:
    for vowel in vowels:
        line = line.replace(vowel, '7')
    new_contents.append(line)
    

print(new_contents)
