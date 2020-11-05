# Inspired by Adrian Rosebrock of PyImageSearch.com
# Luca Barbas and Keagan Chasenski
# 1 October 2020
# Design Project

# python3 pan_tilt_tracking.py --cascade haarcascade_frontalface_default.xml

# import packages
from multiprocessing import Manager
from multiprocessing import Process
from imutils.video import VideoStream
from pyimagesearch.objcenter import ObjCenter
from pyimagesearch.pid import PID
import pantilthat as pth
import argparse
import signal
import time
import sys
import cv2

# define values for the range for the servo motors
servoRange = (-90, 90)


def interrupt_handler(sig, frame):
	"""This is a function to handle system interrupts for signals."""

	# prints system message
	print("[MESSAGE] You cancelled the system process! Now Exiting...")

	# disable the servos
	# DOC: servo_enable has two arguments: servo number, state (True/False) 
	pth.servo_enable(1, False)
	pth.servo_enable(2, False)

	# exit program
	sys.exit()


# function centers the box in the middle of the screen"
def obj_center(args, objX, objY, centerX, centerY):
	"""Centers the box in the middle of the screen."""

	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, interrupt_handler)

	# video stream started to display the face detection working on
	# the monitor
	vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	# initializes the Object Center function using the Haar-Cascade
	# Detection software
	obj = ObjCenter(args["cascade"])

	# loop indefinitely
	while True:
		# Take each frame processed from the video stream and flip the 
		# camera's video stream vertically because our stream was upside
		# down
		frame = vs.read()
		frame = cv2.flip(frame, 0)

		# using the height and width, get the center coordinates of the video
		# feed to determine where the object center should be 
		(H, W) = frame.shape[:2]
		centerX.value = W // 2
		centerY.value = H // 2

		# find the face detection location
		objectLoc = obj.update(frame, (centerX.value, centerY.value))
		((objX.value, objY.value), rect) = objectLoc

		# use openCV to draw the bounding box rectangle around the detected
		# location of the face
		# DOC: cv2.rectangle (frame input, center coordinates, outer coords,
		# RGB colour, line thickness)
		if rect is not None:
			(x, y, w, h) = rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)	

		# use OpenCV to show heading, frame 
		cv2.imshow("Pan-Tilt Face Tracking", frame)
		cv2.waitKey(1)


# function to handle the Control Mechanism of the Pan and Tilt servo Arm 
# this uses a PID compensator 
def pid_control(output, p, i, d, objCoord, centerCoord):
	""" 
	Returns the PID error based on the current PID values, Object Coords and
	 Center Coords
	
	Keyword arguments: 
	output -- output variable
	p -- proportional controller variable
	i -- integral controller variable
	d -- differential controller variable
	objCoord - Objects X and Y coordinates
	centerCoord - X and Y coordinate of the center of the frame.
	
	"""

	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, interrupt_handler)

	# initialize the PID Controller
	p = PID(p.value, i.value, d.value)
	p.initialize()

	# loop indefinitely
	while True:
		# find the error function
		error = centerCoord.value - objCoord.value

		# update the output value based on the error
		# DOC: The output.value variable will keep updating with a change 
		# in error value as long as the servo is moving, otherwise the 
		# error will be zero
		output.value = p.update(error)


# function which specifies the range
def set_range(val, start, end):
	"""States the range of movement."""

	# determine the input vale is in the supplied range
	return (val >= start and val <= end)


# function which controls the movement of the camera by moving the servos
# mechanical mechanism of the system
def set_servos(pan, tlt):
	"""Initializes the servo motors before computation begins."""

	# signal trap to handle keyboard interrupt
	signal.signal(signal.SIGINT, interrupt_handler)

	# loop indefinitely
	while True:
            
		# reverse the Pan angle because the camera is inversed horizontally
		panAngle = -1 * pan.value
		# reverse the Tilt angle because the camera is inversed vertically
		tltAngle = -1 * tlt.value

		# check if pan angle is within range
		if set_range(panAngle, servoRange[0], servoRange[1]):
			pth.pan(panAngle)	# pan

		# check if tilt angle is within range 
		if set_range(tltAngle, servoRange[0], servoRange[1]):
			pth.tilt(tltAngle)	# tilt

# System run: 
if __name__ == '__main__':
	# read in cmd line arguments through arg parser
	ap = argparse.ArgumentParser()
	ap.add_argument("-c", "--cascade", type=str, required=True,
		help="path to input Haar cascade for face detection")
	args = vars(ap.parse_args())

	# parallel threading manager for thread-safe processes
	with Manager() as manager:
		# start the servos 
		pth.servo_enable(1, True)
		pth.servo_enable(2, True)

		# set default integer value for calibration of camera's x,y coords
		centerX = manager.Value("i", 0)
		centerY = manager.Value("i", 0)

		# set default integer value for calibration of object x,y coords
		objX = manager.Value("i", 0)
		objY = manager.Value("i", 0)

		# set pan and tilt integer values will be managed by independed PIDs
		pan = manager.Value("i", 0)
		tlt = manager.Value("i", 0)

		# set PID float values for panning
		panP = manager.Value("f", 0.09)
		panI = manager.Value("f", 0.08)
		panD = manager.Value("f", 0.002)

		# set PID float values for tilting
		tiltP = manager.Value("f", 0.11)
		tiltI = manager.Value("f", 0.10)
		tiltD = manager.Value("f", 0.002)

		# 4 Independent processes will be processed
		# first: objectCenter - finds/localizes the object
		processObjectCenter = Process(target=obj_center,
			args=(args, objX, objY, centerX, centerY))

		# second: panning - PID control loop determines panning angle
		processPanning = Process(target=pid_control,
			args=(pan, panP, panI, panD, objX, centerX))

		# third: tilting - PID control loop determines tilting angle
		processTilting = Process(target=pid_control,
			args=(tlt, tiltP, tiltI, tiltD, objY, centerY))
		
		# fourth: setServos - drives the servos to proper angles based on PID
		# ...feedback to keep object in center
		processSetServos = Process(target=set_servos, args=(pan, tlt))

		# start the parallel processes
		processObjectCenter.start()
		processPanning.start()
		processTilting.start()
		processSetServos.start()

		# join the parallel processes
		processObjectCenter.join()
		processPanning.join()
		processTilting.join()
		processSetServos.join()

		# disable the servos when the system is finished 
		pth.servo_enable(1, False)
		pth.servo_enable(2, False)
