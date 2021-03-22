from __future__ import print_function
import cv2 as cv

def obtainMotionVideo(videoPath):
	backgroundModel = cv.createBackgroundSubtractorMOG2()
	capture = cv.VideoCapture(cv.samples.findFileOrKeep(videoPath))
	frame_width = int(capture.get(3))
	frame_height = int(capture.get(4))
	fourcc = cv.VideoWriter_fourcc('M','J','P','G')
	out = cv.VideoWriter('motion_' + videoPath + '.avi', fourcc, 20, (frame_width,frame_height))
	if not capture.isOpened():
			print('Unable to open: ' + args.input)
			exit(0)
	while True:
			ret, frame = capture.read()
			if frame is None:
					break

			fgMask = backgroundModel.apply(frame)

			cv.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
			cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

			#cv.imshow('Frame', frame)
			#cv.imshow('FG Mask', fgMask)
			#newFrame = cv.bitwise_and(frame, frame, mask = fgMask)
			#ret, thresh1 = cv.threshold(newFrame, 120, 255, cv.THRESH_BINARY) 
			cv.imshow('MOG2', fgMask)

			out.write(cv.cvtColor(fgMask, cv.COLOR_GRAY2RGB))
			k = cv.waitKey(30) & 0xff; 
			if k == 27: 
				break; 
	out.release()