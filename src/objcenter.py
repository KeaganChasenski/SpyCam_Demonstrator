# Inspired by Adrian Rosebrock of PyImageSearch.com
# Luca Barbas and Keagan Chasenski
# 1 October 2020
# Design Project

# import packages
import imutils	# image utitlity package
import cv2		# openCV package

# this class is intended to process the face detection and computer vision
# calculations that are used in the Pan/Tilt class

class ObjCenter:
	"""Loads the Haar Cascade Computer Vision Model using OpenCV."""
	def __init__(self, haarPath):
		self.detector = cv2.CascadeClassifier(haarPath)
	
	# OpenCV processing 
	def update(self, frame, frameCenter):
		"""Returns the bounding boxes for the faces that appear in the frame."""
		# GrayScale conversion from OpenCV
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# call the detector for the multiple faces from the input 
		rects = self.detector.detectMultiScale(gray, scaleFactor=1.05,
			minNeighbors=9, minSize=(30, 30),
			flags=cv2.CASCADE_SCALE_IMAGE)

		# If a face was detected
		if len(rects) > 0:
			# Extracts bounding box coordinates
			(x, y, w, h) = rects[0]
			faceY = int(y + (h / 2.0))
			faceX = int(x + (w / 2.0))


			# returns the center coordinates found and the bounding box
			return ((faceX, faceY), rects[0])

		# else no faces were found and do nothing
		return (frameCenter, None)