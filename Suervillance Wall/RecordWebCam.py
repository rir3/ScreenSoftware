# Python program to illustrate
# saving an operated video

# organize imports
import cv2 #opencv-python
import time

def record(video_name="WebCamVideo.avi"):
	#video_name needs .avi extension
	#Add Code to find webcam and use said webcam for VideoCapture
	# This will return video from the first webcam on your computer.
	#cap = cv2.VideoCapture(0)#For Mac
	cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)#For Windows

	#Get Webcam Max Settings Automatically Here
	cap.set(3, 1920)
	cap.set(4, 1080)
	#Will use Lowest Res if no Specified
	#cap.set(3, 1280)
	#cap.set(4, 720)
	#cap.set(3, 3840)
	#cap.set(4, 2160)

	# Define the codec and create VideoWriter object
	#fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
	#fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
	#out = cv2.VideoWriter('output.mov', fourcc, 15, (1028,720), True)#(640, 480)


	# Default resolutions of the frame are obtained.The default resolutions are system dependent.
	# We convert the resolutions from float to integer.
	#1920x1080
	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))

	out = cv2.VideoWriter(video_name,cv2.VideoWriter_fourcc('M','J','P','G'), 20, (frame_width,frame_height))

	# Set the timer to trigger after 5 seconds
	start_time = time.time()
	trigger_time = start_time + 25

	# loop runs if capturing has been initialized.
	while(True):
		#pygame.event.pump()
		# reads frames from a camera
		# ret checks return at each frame
		ret,frame = cap.read()#Removing ret will cause error

		# Converts to HSV color space, OCV reads colors as BGR
		# frame is converted to hsv
		#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		  
		# output the frame
		out.write(frame)
		
		# The original input frame is shown in the window
		#cv2.imshow('Original', frame)

		# The window showing the operated video stream
		#cv2.imshow('frame', hsv)

		
		# Wait for 'a' key to stop the program
		#if cv2.waitKey(1) & 0xFF == ord('a'):
		#	break

		if time.time() > trigger_time:
			break

	# Close the window / Release webcam
	cap.release()

	# After we release our webcam, we also release the output
	out.release()

	# De-allocate any associated memory usage
	#cv2.destroyAllWindows()

#record()