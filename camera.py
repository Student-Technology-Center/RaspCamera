import pygame.camera 
import pygame.image

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email import encoders
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase

import shutil

from PIL import Image
import time
import datetime
import sys
import os

pygame.camera.init()

def send_email():
    time = get_time()
    msg = MIMEMultipart()
    
    fromaddr = "stc.camera.vive@gmail.com"
    message = "Sent at %s" % time 
    password = ""
    attach = ("pictures/%s_zip" % get_date())
    directory_info = ("pictures/%s" % get_date())

    shutil.make_archive(attach, 'zip', directory_info)

    attachment = open(attach + ".zip", "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename =%s" %attach)

    msg.attach(part)
    
    msg['From'] = fromaddr
    msg['To'] = fromaddr
    msg['Subject'] = message
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr,password)
    server.sendmail(fromaddr, toaddr)

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
        webcam.start()
        while True:
            try:
                take_picture(webcam, working_directory)
                time.sleep(5)
                #send_email()
            except Exception as y:
                print "Error caught inside loop."
                print y
                webcam.stop()
                time.sleep(10)
                webcam.start()
                continue
    except Exception as e:
        print "System caught an error."
        print e
        sys.exit()

if __name__ == "__main__":
    main()
