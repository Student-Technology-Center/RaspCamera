import pygame.camera 
import pygame.image
from PIL import Image
from PIL import ImageDraw

import shutil

import __future__
import time
import datetime
import sys
import os
import shutil

pygame.camera.init()

def take_picture(webcam, directory, num):
    try:
        webcam.start()
        #take_picture(webcam, working_directory)
        #Initializes the camera for a picture
        img = webcam.get_image()

        #Gets time to write to sys out
        save_time = get_time()

        #These next few lines takes in the previous image and brightens them.
        #Using a lambda function and the PIL library
        pygame.image.save(img, "%s/%s_temp.jpg" % (directory, num))
        img_to_brighten = Image.open("%s/%s_temp.jpg" % (directory, num))
        img_brightened = img_to_brighten.point(lambda p: p * 1.5)
        draw = ImageDraw.Draw(img_brightened)
        draw.text((10, 10), get_date(), fill=(255, 255, 255, 128))
        draw.text((10, 20), get_time(), fill=(255, 255, 255, 128))
        img_brightened.save("%s/%s.jpg" % (directory, num))

        #Removes the temp (old) image file
        os.remove("%s/%s_temp.jpg" % (directory, num))

        #Logs the output to a file
        filename = directory + "/Todays_Log.txt"
        fn = open(filename, "a")
        fn.write("Output to %s/%s.jpg\n" % (directory, num))
        fn.close()

        webcam.stop()
    except Exception as y:
        print "Error in taking picture"
        print y
        webcam.stop()

def make_directory(string_date):
    '''Creates a directory for the current date'''
    directory = "temp/" + string_date
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def get_time():
    '''Wrapper function for grabbing the current time in a pleasing format.'''
    time = datetime.datetime.now()
    return "%s:%s:%s" % (time.hour, time.minute, time.second)
                      
def get_date():
    '''Wrapper function for grabbing the current date in a pleasing format.'''
    time = datetime.datetime.now()
    return "%s/%s/%s" % (time.month, time.day, time.year)

def get_date_hour():
    time = datetime.datetime.now()
    return "%s_%s_%s__%s" % (time.month, time.day, time.year, time.hour)

def main():
    '''
    Takes a picture relative to the int interval is equal to in seconds.
    Does this 10 times, then checks for updates in the git repo.
    If they don't exist, it runs again (performed by batch script on pi)
    '''
    try:
        interval = 6
        count = 0
        COUNT_LIMIT = 600
        working_directory = make_directory(get_date_hour())
        possible_cameras = pygame.camera.list_cameras()     
        webcam = pygame.camera.Camera(possible_cameras[0], (480, 270))

        starttime = time.time()
        while count < COUNT_LIMIT:
            take_picture(webcam, working_directory, count)
            count = count + 1
            time.sleep(interval - ((time.time() - starttime) % interval))

        scpScript = "scp -r -i /home/pi/.ssh/id_rsa %s rasp@140.160.191.116:~/pictures_mailbox" % (working_directory)
        os.system(scpScript)
        shutil.rmtree(working_directory)

        sys.exit()
    except Exception as e:
        print "System caught an error."
        print e
        sys.exit()

if __name__ == "__main__":
    main()
