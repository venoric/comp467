with open('/Users/casey/Desktop/csun/comp467/weeklyassignment2/ingest_this.txt') as f:
    contents = f.readlines()

vowels = ['a', 'e', 'i', 'o', 'u']

new_contents = []

for line in contents:
    for vowel in vowels:
        line = line.replace(vowel, '7')
    new_contents.append(line)

# Combine the modified lines into a single string
modified_text = ''.join(new_contents)

print(modified_text)