a = ['/Barbie/reel1/partA/1920x1080', '/Barbie/reel1/VFX/Hydraulx', '/Barbie/reel1/VFX/Framestore', '/Barbie/reel1/VFX/AnimalLogic', '/Barbie/reel1/partB/1920x1080', '/Barbie/pickups/shot_1ab/1920x1080', '/Barbie/pickups/shot_2b/1920x1080', '/Barbie/reel1/partC/1920x1080']
b =  ['/Barbie/reel1/partA/1920x1080', '/Barbie/reel1/VFX/Hydraulx', '/Barbie/reel1/partA/1920x1080', '/Barbie/pickups/shot_1ab/1920x1080', '/Barbie/reel1/partA/1920x1080', '/Barbie/reel1/VFX/Framestore', '/Barbie/reel1/VFX/Hydraulx', '/Barbie/reel1/partA/1920x1080', '/Barbie/reel1/partB/1920x1080', '/Barbie/reel1/VFX/AnimalLogic', '/Barbie/reel1/partB/1920x1080', '/Barbie/reel1/VFX/Hydraulx', '/Barbie/reel1/VFX/Framestore', '/Barbie/pickups/shot_2b/1920x1080', '/Barbie/reel1/partB/1920x1080', '']





def find_ranges_with_text(items):
    if not items:
        return ""

    ranges = []
    start = end = None

    for item in items:
        # Split the item into parts based on spaces
        parts = item.split()
        
        # Initialize variables to store text and numbers
        text = ""
        numbers = []

        # Separate text and numbers
        for part in parts:
            if part.isdigit():
                numbers.append(int(part))
            else:
                text += part + " "

        # Process the numbers to find ranges
        for num in numbers:
            if start is None:
                start = end = num
            elif num == end + 1:
                end = num
            else:
                if start == end:
                    ranges.append(f"{text.strip()} {start}")
                else:
                    ranges.append(f"{text.strip()} {start}-{end}")
                start = end = num

    if start is not None:
        if start == end:
            ranges.append(f"{text.strip()} {start}")
        else:
            ranges.append(f"{text.strip()} {start}-{end}")

    return ', '.join(ranges)

# Example usage:
noerr_baselight_contents = [
    "Barbie/reel1/partA/1920x1080 31 32 33 34 35",
    "Some text 67 70",
    "Another example 122-123",
    "Just a single value 155"
]

result = find_ranges_with_text(noerr_baselight_contents)
print(result)







