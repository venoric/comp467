#-Create a folder on your computer called "week3" 
#-Create a script that, when run,checks every second indefinitely for a new file in that folder
# Put on sleep and check every 3 seconds.
# Look for differences with new list and old list.  If it's different.  Return the things that are new. (Got rid of this)
#-If file found,report back to the user:
#1.File found 
#2.What type of file it is
#3.When it was put there

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

class CustomLoggingEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_name = event.src_path.split('/')[-1]
            file_extension = file_name.split('.')[-1]
            logging.info(f"NEW FILE FOUND: .{file_extension}")


if __name__ == "__main__":
    # Set the format for logging info
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


path = '/Users/casey/Desktop/csun/comp467/week3'

event_handler = CustomLoggingEventHandler()

observer = Observer()
observer.schedule(event_handler, path, recursive=True)

    # Start the observer
observer.start()
try:
    while True:
            # Set the thread sleep time
            time.sleep(3)
except KeyboardInterrupt:
    observer.stop()
observer.join()
