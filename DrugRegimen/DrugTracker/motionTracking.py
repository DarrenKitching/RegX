from __future__ import print_function
import cv2 as cv
import numpy as np
from scipy.stats import sem, t
from scipy import mean

def obtainMotionVideo(videoPath):
	backgroundModel = cv.createBackgroundSubtractorMOG2()
	capture = cv.VideoCapture(cv.samples.findFileOrKeep(videoPath))
	frame_width = int(capture.get(3))
	frame_height = int(capture.get(4))
	#fourcc = cv.VideoWriter_fourcc('M','J','P','G')
	#out = cv.VideoWriter('motion_' + videoPath + '.avi', fourcc, 20, (frame_width,frame_height))
	confidenceScore = 0
	totalFrames = 0
	totalBlack = 0
	isFirst = True
	if not capture.isOpened():
			print('Unable to open: ' + videoPath)
			exit(0)
	while True:
			ret, frame = capture.read()
			if frame is None:
					break

			fgMask = backgroundModel.apply(frame)
			newFrame  = cv.cvtColor(fgMask, cv.COLOR_GRAY2RGB)
			blackPixels = (frame_width * frame_height) - cv.countNonZero(cv.cvtColor(newFrame, cv.COLOR_BGR2GRAY))
			if not isFirst:
				totalBlack += blackPixels
				totalFrames += 1
			isFirst = False
			k = cv.waitKey(30) & 0xff; 
			if k == 27: 
				break; 
	percentageNonBlack = 1 - (totalBlack / totalFrames) / (frame_width * frame_height) # average number of non black pixels per frame divided by resolution
	lowerInterval = 0.085
	higherInterval = 0.225
	mean = 0.155
	if percentageNonBlack > higherInterval or percentageNonBlack < lowerInterval:
		print(5)
	else:
		difference = abs(mean - percentageNonBlack) # between 0 and 0.07
		multiples = difference / 0.01
		print (round(95 - (10 * multiples)))