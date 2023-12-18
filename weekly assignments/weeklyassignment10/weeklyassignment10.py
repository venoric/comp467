import subprocess
import shlex

# Enclose the path in quotes
command = 'ls -l "/Users/casey/Desktop/csun/comp467/weekly assignments/weeklyassignment10"'
process = subprocess.Popen(
    shlex.split(command),
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT, 
)

max_size = 0
largest_file = ""

for line in iter(process.stdout.readline, b''):
    line_decoded = line.decode()
    #print(line_decoded)
    parts = line_decoded.split()
    #print(parts)
    if len(parts) > 4 and parts[4].isdigit():
        size = int(parts[4])
        #print(size)
        filename = " ".join(parts[8:])
        if size > max_size:
            max_size = size
            largest_file = filename

print(f"The largest file is '{largest_file}' with a size of {max_size} bytes.")
