from InstagramAPI import InstagramAPI
import time
import sys
import os
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import Image

INSTAGRAM_USERNAME = "user" # CHANGE USERNAME
INSTAGRAM_PASSWORD = "psswd" # CHANGE PASSWORD

InstagramAPI = InstagramAPI(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)  # Make sure to change user and psswd.
InstagramAPI.login() # login


class FolderWatcher:
    # Initiating and running a watcher for designated folder
    def __init__(self, folderToWatch):
        self.folderToWatch = folderToWatch
        self.observer = Observer()

    def run(self):
        f_event_handler = FolderHandler()
        self.observer.schedule(f_event_handler, self.folderToWatch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "watchdog Error"

        self.observer.join()


class FolderHandler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            print event.src_path
            # Show image for autorization
            image = Image.open(event.src_path)
            image.show()
            inputFlag = False
	# TODO change this authorization method..
            while (inputFlag == False):
                auth_answer = raw_input("Do you authorize this pic, buddy?\n")
                if auth_answer == 'yes':
                    caption = raw_input("enter caption:\n")
                    InstagramAPI.uploadPhoto(photo=event.src_path, caption=caption)
                    inputFlag = True
                    break
                elif auth_answer == 'no':
                    inputFlag = True
                    break
                print "wrong answer."

        elif event.event_type == 'modified':
            print "file modified"
            return None


if __name__ == '__main__':
	# Change watchdog to watch the folder you want.
    w = FolderWatcher("./photosFolder/")
    w.run()

print "test done."
