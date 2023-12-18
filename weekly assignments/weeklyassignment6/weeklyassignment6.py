#Create an Argparsescript...
# and a "verbose" option that prints each line if that option is flagged. 
#Submit the code and output from running the script with "verbose" and one without "verbose"
# import argparse
# arguments for importing a .txt file --txt "Name.txt"
# verbose flag (0 OR 1) --verbose (=1) no argument = 0 (Verbose is used to find errors so if "keyword" is in .txt FLAG IT)
import argparse, os
script_dir = os.path.dirname(os.path.abspath(__file__))
parser = argparse.ArgumentParser(description="Argparse script")
parser.add_argument("--txt", required=True, help="Import .txt file")
#will only exist when needed
parser.add_argument("--verbose", action="store_true", help="Toggle Verbose")
# parser.add_argument("--output", required=True, help="Path to the output") DONT NEED 
line_count = 0
args = parser.parse_args()
txt_path = os.path.join(script_dir, args.txt)
with open(txt_path) as f:
    txt_contents = f.read().splitlines()
    for line in txt_contents:
        # if verbose is being used and "Hello" is in line
        if args.verbose and "Hello" in line:
            print("Found 'Hello' in this line: " + line)
            line_count += 1 
print("There are: " + str(line_count) + "lines")

# now how can we mark this as verbose ? (seen in output)
# print(txt_contents)
# for each array in txt_contents, increment +1 to line_count
# if verbose is true / false 
# need to read .txt's lines 
# for line in txt:
    #line_count++
    # if verbose in line:
        #print(line)
# example - "python3 weeklyassignment6.py --txt --verbose"
# script w/ verbose and one w/o verbose 