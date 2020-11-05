# Inspired by Adrian Rosebrock of PyImageSearch.com
# Luca Barbas and Keagan Chasenski
# 1 October 2020
# Design Project

# package imports 
import time

# DOC: This PID Class controls the servo motors using a PID Compensator Control technique
# P = Proportional control (increasing by a certain gain)
# I = Integral of signal control (helps predict using future preditions)
# D = Derivative of the signal control (helps predict using past values)
# The values set for kP, kI and kD have been custom-tuned for our application but 
# should be tested and changed to suit your needs.

class PID:

	# initializing the controller values (need some personal tuning)
	def __init__(self, kP=100, kI=150, kD=1):
		"""Initializes the controller values (need some personal tuning)."""
		# initialize gains
		self.kI = kI
		self.kD = kD
		self.kP = kP


	def initialize(self):
		"""Intialization all the variables to be used in the update() function."""

		# initialize the current and previous time variables
		# this will be used as timing variables for the control system
		self.currTime = time.time()
		self.prevTime = self.currTime

		# system's previous error so that there is no OutOfBoundsException
		self.prevError = 0

		# initialize the PID term result
		self.cI = 0
		self.cD = 0
		self.cP = 0

	def update(self, error, sleep=0.2):
		"""Updating all the variables to be used."""
		# minor sleep so that we don't overload processing for the 
		# Raspberry Pi
		time.sleep(sleep)

		# calculate the difference in time (delta time)
		self.currTime = time.time()
		deltaTime = self.currTime - self.prevTime

		# calculate the change in error
		deltaError = error - self.prevError

		# integral term
		self.cI += error * deltaTime

		# derivative term and prevent divide by zero
		self.cD = (deltaError / deltaTime) if deltaTime > 0 else 0

		# proportional term
		self.cP = error

		# save previous time and error for the next update
		self.prevTime = self.currTime
		self.prevError = error

		# sum the terms and return
		return sum([
			self.kP * self.cP,
			self.kI * self.cI,
			self.kD * self.cD])