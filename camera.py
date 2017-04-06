import pygame.camera 
import pygame.image
from PIL import Image

import shutil

import __future__
import time
import datetime
import sys
import os

pygame.camera.init()

def take_picture(current_camera, directory):
    img = current_camera.get_image()
    save_time = get_time()
    pygame.image.save(img, "%s/%s_temp.jpg" % (directory, save_time))
    img_to_brighten = Image.open("%s/%s_temp.jpg" % (directory, save_time))
    img_brightened = img_to_brighten.point(lambda p: p * 1.5)
    img_brightened.save("%s/%s.jpg" % (directory, save_time))
    os.remove("%s/%s_temp.jpg" % (directory, save_time))
    total_directory = "Output to %s/%s" % (directory,save_time)
    return total_directory 

def make_directory(string_date):
    directory = "media/tDrive/rasp-camera/" + string_date
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def get_time():
    time = datetime.datetime.now()
    current_time = "%s:%s:%s" % (time.hour, time.minute, time.second)
    return current_time
                      
def get_date():
    time = datetime.datetime.now()
    date = "%s-%s-%s" % (time.month, time.day, time.year)
    return date

def main():
    try:
        working_directory = make_directory(get_date())
        possible_cameras = pygame.camera.list_cameras()     
        webcam = pygame.camera.Camera(possible_cameras[0], (480, 270))
        for i in range(0, 10):
            try:
                webcam.start()
                take_picture(webcam, working_directory)
                webcam.stop()
                time.sleep(6)
            except Exception as y:
                print "Error in taking picture"
                print y
                webcam.stop()
                time.sleep(6)
                webcam.start()
                continue
        sys.exit()
    except Exception as e:
        print "System caught an error."
        print e
        sys.exit()

if __name__ == "__main__":
    main()
