import argparse, os, json
import ffmpeg
script_dir = os.path.dirname(os.path.abspath(__file__))
parser = argparse.ArgumentParser(description="Argparse script")
parser.add_argument("--video", required=True, help="Import video file")

args = parser.parse_args()
video_path = os.path.join(script_dir, args.video)

try:
    (
        ffmpeg
        .input(video_path, r=1)
        .output(os.path.join(script_dir, 'frame-%04d.png'), format='image2')
        .run()
    )
except ffmpeg.Error as e:
    print("Error:", e)

try:
    video_info = ffmpeg.probe(args.video)
    print(json.dumps(video_info, indent=4))  # Print information in a readable format
except ffmpeg.Error as e:
    print("Error:", e)