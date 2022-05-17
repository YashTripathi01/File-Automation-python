import os
import shutil
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# from constants import*

# folder initialization
source_dir = SOURCE_DIR
destination_image = DES_IMG
destination_pdf = DES_PDF
destination_videos = DES_VID
destination_isoFile = DES_ISO
destination_textFile = DES_TEXT

# to make change filename if already exists


def make_unique(path):
    filename, extension = os.path.splitext(path)
    counter = 1
    # if file exists, add number to the end of the file
    while os.path.exists(path):
        path = filename+'('+str(counter)+')'+extension
        counter += 1

    return path


# to move the file
def move_file(dest, entry, name):
    file_exists = os.path.exists(dest+'/'+name)
    if file_exists:
        unique_name = make_unique(name)
        os.rename(entry, unique_name)

    shutil.move(entry, dest)


# THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                # ADD MORE IF STATEMENTS FOR DIFFERENT FILETYPES
                if name.endswith('.pdf'):
                    dest = destination_pdf
                    move_file(dest, entry, name)
                elif name.endswith('.mov') or name.endswith('.mp4') or name.endswith('.mkv'):
                    dest = destination_videos
                    move_file(dest, entry, name)
                elif name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png'):
                    dest = destination_image
                    move_file(dest, entry, name)
                elif name.endswith('.iso') or name.endswith('.vbox-extpack'):
                    dest = destination_isoFile
                    move_file(dest, entry, name)
                elif name.endswith('.txt') or name.endswith('.ttf'):
                    dest = destination_textFile
                    move_file(dest, entry, name)


# NO NEED TO CHANGE BELOW CODE
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
