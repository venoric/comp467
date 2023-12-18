#Project 1 and 2 delt with frames, let's turn some
#Into timecode.
#Write a script that takes a frame and turns it into
#Working timecode at 24 fps.
#Use frame examples: 35, 1569, 14000


def frames_to_timecode(frame_number, fps=1):
    # Calculate the total seconds and frames
    total_seconds = frame_number / fps
    total_minutes, total_seconds = divmod(total_seconds, 60)
    total_hours, total_minutes = divmod(total_minutes, 60)
    total_frames = frame_number % fps

    # Format the timecode
    timecode = f"{int(total_hours):02d}:{int(total_minutes):02d}:{int(total_seconds):02d}:{total_frames:02d}"

    return timecode


frames = [35,1569,14000]

for frame in frames:
    timecode = frames_to_timecode(frame)
    print(f"Frame {frame} is equivalent to Timecode {timecode} at 24 fps")