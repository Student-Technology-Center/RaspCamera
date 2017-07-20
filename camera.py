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
    #Initializes the camera for a picture
    img = current_camera.get_image()

    #Gets time to write to sys out
    save_time = get_time()

    #These next few lines takes in the previous image and brightens them.
    #Using a lambda function and the PIL library
    pygame.image.save(img, "%s/%s_temp.jpg" % (directory, save_time))
    img_to_brighten = Image.open("%s/%s_temp.jpg" % (directory, save_time))
    img_brightened = img_to_brighten.point(lambda p: p * 1.5)
    img_brightened.save("%s/%s.jpg" % (directory, save_time))

    #Removes the temp (old) image file
    os.remove("%s/%s_temp.jpg" % (directory, save_time))

    #Logs the output to a file
    filename = directory + "/Todays_Log"
    fn = open(filename, "w")
    fn.write("Output to %s/%s" % (directory,save_time))
    fn.close()

    #Saves the output directory
    total_directory = "Output to %s/%s" % (directory,save_time)
    return total_directory 

def make_directory(string_date):
    '''Creates a directory for the current date'''
    directory = "media/tDrive/rasp-camera/" + string_date
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def get_time():
    '''Wrapper function for grabbing the current time in a pleasing format.'''
    time = datetime.datetime.now()
    current_time = "%s_%s_%s" % (time.hour, time.minute, time.second)
    return current_time
                      
def get_date():
    '''Wrapper function for grabbing the current date in a pleasing format.'''
    time = datetime.datetime.now()
    date = "%s-%s-%s" % (time.month, time.day, time.year)
    return date

def main():
    '''
    Takes a picture relative to the int interval is equal to in seconds.
    Does this 10 times, then checks for updates in the git repo.
    If they don't exist, it runs again (performed by batch script on pi)
    '''
    try:
        interval = 6
        working_directory = make_directory(get_date())
        possible_cameras = pygame.camera.list_cameras()     
        webcam = pygame.camera.Camera(possible_cameras[0], (480, 270))
        for i in range(0, 10):
            try:
                webcam.start()
                take_picture(webcam, working_directory)
                webcam.stop()
                time.sleep(interval)
            except Exception as y:
                print "Error in taking picture"
                print y
                webcam.stop()
                time.sleep(interval)
                webcam.start()
                continue
        sys.exit()
    except Exception as e:
        print "System caught an error."
        print e
        sys.exit()

if __name__ == "__main__":
    main()
