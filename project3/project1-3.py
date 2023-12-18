import csv, argparse, pymongo, ffmpeg, xlsxwriter, os.path
from frameioclient import FrameioClient
#client = FrameioClient(""")
#me = client.users.get_me()
#project_id = ""
# Set up the argument parser
parser = argparse.ArgumentParser(description="Process video files")
parser.add_argument("--process", dest="videos", nargs="+", help="Import Video File")
#parser.add_argument("--csv", dest="c", help="Path to the output CSV file")
parser.add_argument("--xlsx", dest="xlsx_filename", help="Path to the output CSV file")

# thumbnail_folder = ''

args = parser.parse_args()

# Retrieve command line arguments
videos = args.videos
#c = args.csv
# Process videos if provided
def frames_to_timecode(frame_number, fps):
    total_seconds = frame_number // fps
    total_minutes, total_seconds = divmod(total_seconds, 60)
    total_hours, total_minutes = divmod(total_minutes, 60)
    remaining_frames = frame_number % fps

    timecode = f"{int(total_hours):02d}:{int(total_minutes):02d}:{int(total_seconds):02d}:{int(remaining_frames):02d}"
    return timecode

if videos:
    for video in videos:
        probe = ffmpeg.probe(video)
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        #print(video_info)
        video_fps = eval(video_info['r_frame_rate'])
        num_frames= eval(video_info['nb_frames'])
        #ff = ffmpeg.input(video)
        #ff = ffmpeg.output(ff, 'thumbnailframe%d.png', vf='scale=96:74', vsync='vfr')
        #ffmpeg.run(ff)

        timecodes = []
        # Iterate over each frame and print the timecode
        for frame in range(num_frames):
            timecode = frames_to_timecode(frame, video_fps)
            timecodes.append(timecode)
            max_timecode = timecodes[-1]
            #print(f"Frame {frame} is equivalent to Timecode {timecode}")
    
print(f"Max time code is {max_timecode}")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["database"]
first_database = mydb["first_database"]
second_database = mydb["second_database"]

workbook = xlsxwriter.Workbook(args.xlsx_filename)
worksheet = workbook.add_worksheet()

def calculate_middle_frame(frames_range):
    frames_range = str(frames_range)

    if "-" in frames_range:
        start_frame, end_frame = map(int, frames_range.split("-"))
        return start_frame + (end_frame - start_frame) // 2
    else:
        return int(frames_range)

def process_frames_range(frames_range, fps, max_timecode):
    frames_range = str(frames_range)

    if "-" in frames_range:
        start_frame, end_frame = map(int, frames_range.split("-"))
        start_timecode = frames_to_timecode(start_frame, fps)
        end_timecode = frames_to_timecode(end_frame, fps)

        # Check if either timecode exceeds the max_timecode
        if max_timecode and (start_timecode > max_timecode or end_timecode > max_timecode):
            return None
        return f"{start_timecode}-{end_timecode}"
    else:
        frame = int(frames_range)
        timecode = frames_to_timecode(frame, fps)

        if max_timecode and timecode > max_timecode:
            return None
        return timecode

if args.xlsx_filename:
    data = list(second_database.find({}, {'_id': 0}))
    if data:
        headers = list(data[0].keys()) + ["Timecode", "Thumbnail"]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
    
    valid_row = 1

    for document in data:
        frames_range = document.get("Frames/Ranges:", "")  # frames /ranges stuff
        timecode_range = process_frames_range(frames_range, video_fps, max_timecode) if frames_range else None

        thumbnail_frame = calculate_middle_frame(frames_range) if frames_range else None
        thumbnail_file = f"thumbnailframe{thumbnail_frame}.png" if thumbnail_frame is not None else ""
        thumbnail_path = os.path.join(thumbnail_folder, thumbnail_file)

        # Write the row only if there is a valid timecode
        if timecode_range and os.path.exists(thumbnail_path): 
            for col, header in enumerate(headers):
                worksheet.write(valid_row, col, document.get(header, ''))
            worksheet.write(valid_row, len(headers) - 2, timecode_range)
            #worksheet.write(valid_row, len(headers) - 1, thumbnail_file)

            image_col = len(headers) - 1  # Column for the thumbnail

            # commented out since I already did it and don't want to upload the same files again
            # project = client.projects.get(project_id)
            #root_asset_id = project.get('root_asset_id')
            #client.assets.upload(root_asset_id,thumbnail_path)

            worksheet.insert_image(valid_row, image_col, thumbnail_path, {'x_scale': 0.5, 'y_scale': 0.5})
            
            valid_row += 1


# For each entry in "Frames/Ranges" print out that value
    workbook.close()

# Upload a file 
# client.assets.upload(destination_id, "video.mp4")