# Luca Barbas and Keagan Chasenski
# 1 October 2020
# Design Project

# import packages
from pan_tilt_tracking import *
import subprocess
import os
import time
import webbrowser

# automatically runs module

print("Welcome to SpyCamera module, please select an option:")
print("1. Start the camera/tilt module using the Face Recognition software")
print("2. Control the camera/tilt module using a webserver")

result = input()
# input value of 1: Face Recognition
if (result == "1"):
    # run Facial Recognition
    print("Starting...")
    # call pan_tilt_tracking main file
    subprocess.run('python3 pan_tilt_tracking.py --cascade haarcascade_frontalface_default.xml', shell=True)

    
# input value of 2: Webserver
elif (result == "2"):
    # run Webserver
    print("Booting web server...")
    # call webserver.py file
    # open a browser tab with a specific IP address
    os.chdir('/home/pi/Desktop/SpyCam/WebServer')
    #subprocess.run('cd WebServer', shell=True)
    subprocess.run('python3 server.py', shell=True) 
    webbrowser.get("firefox").open("http://192.168.0.107:8082/index.html")


    