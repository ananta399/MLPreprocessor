import cv2
import sys
import numpy as np
import os

###Input arguments: filename followed by two numbers, indicating the start time and end time in seconds
###Example: python toSubmit.py DJI_0007.mov 314 362
###Takes an input RGB image and removes common false positives

def removeObstacles(src):
 currentImage = src
 radius = 17
 valueChannelHighThreshold = 130
 valueChannelLowThreshold = 0
 saturationChannelHighThreshold = 255
 saturationChannelLowThreshold = 0
 #Slowly Blur the image excluding regions of interest with increasing intensity
 for i in range(0,3):
 radius = radius + 5
 hsv = cv2.cvtColor(currentImage, cv2.COLOR_BGR2HSV)
 color_mask = cv2.inRange(hsv, (0, saturationChannelLowThreshold, valueChannelLowThreshold),
(255,saturationChannelHighThreshold,valueChannelHighThreshold))
 kernel = np.ones((2,2),np.uint8)
 #erode_color_mask = cv2.erode(color_mask,kernel,iterations = 2) ##Erosion may be helpful to better to get rid of noise
 erode_color_mask = color_mask
 ###Use either Average Blur or Median Blur
 blurred = cv2.blur(currentImage, (radius,radius))
 #blurred = cv2.medianBlur(currentImage, radius) #For Median Blur
 colorMask_opposite = cv2.bitwise_not(erode_color_mask)
 blurred_fill_holes = cv2.bitwise_and(blurred, blurred, mask = colorMask_opposite)
 cv2.imshow("removeObstacles mask", color_mask)
 maskedImg = cv2.bitwise_and(currentImage, currentImage, mask = erode_color_mask)
 temp = cv2.add(blurred_fill_holes, maskedImg)
 return temp
 
 
###Final blurring of the image before sending to the object tracker.
###src is the original RGB image while gray is the grayscale image to be sent to the tracker
def finalBlur(src, gray):
 valueChannelHighThreshold = 130
 valueChannelLowThreshold = 0
 saturationChannelHighThreshold = 255
 saturationChannelLowThreshold = 0
 radius = 500
 currentImage = src
 hsv = cv2.cvtColor(currentImage, cv2.COLOR_BGR2HSV)
 color_mask = cv2.inRange(hsv, (0, saturationChannelLowThreshold, valueChannelLowThreshold),
(255,saturationChannelHighThreshold,valueChannelHighThreshold))
 #erode_color_mask = cv2.erode(color_mask,kernel,iterations = 2) ##Erosion may be helpful to better to get rid of noise
 erode_color_mask = color_mask
 ###Use either Average Blur or Median Blur
 kernel = np.ones((4,4),np.uint8) ##Currently unused, but use this for Median Blur
 blurred = cv2.blur(gray, (radius,radius)) #For Average Blur
 #blurred = cv2.medianBlur(currentImage, radius) #For Median Blur
 colorMask_opposite = cv2.bitwise_not(erode_color_mask)
 blurred_fill_holes = cv2.bitwise_and(blurred, blurred, mask = colorMask_opposite)
 maskedImg = cv2.bitwise_and(gray,gray, mask = erode_color_mask)
 temp = cv2.add(blurred_fill_holes, maskedImg)
 return temp
 
 
##Increases Contrast and Brightness
def bright(image):
 alpha = 2
 beta = -100
 new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
 return new_image
 
 
####################### MAIN ####################################
filename = sys.argv[1] ##Filename of the input video
fps = 30 ##Frames per second of the input video
cap = cv2.VideoCapture(filename) ##Either camera or Video File
# Check if camera opened successfully
if (cap.isOpened()== False):
 print("Error opening video stream or file")
#Output Files
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out3 = cv2.VideoWriter('output_to_motion_object_tracker.avi',cv2.VideoWriter_fourcc('M','J','P','G'), int(fps), (1024,768))
out4 = cv2.VideoWriter('orgi.avi',cv2.VideoWriter_fourcc('M','J','P','G'), int(fps), (1024,768))
##Convert seconds into frames
start = int(sys.argv[2])
start = int(start*fps)
end = int(sys.argv[3])
end = int(end*fps)
##Current frame
count = 0
cap.set(1,start)

# Read until video is completed
while(cap.isOpened()):
 # Capture frame-by-frame
 ret, img = cap.read()
 if ret == True:
   count = count + 1
 if (count > end - start):
   break
 img = cv2.resize(img,(1024,768))
 originalImage = cv2.resize(img,(1024,768))
 img = removeObstacles(img)
 height, width, channels = img.shape
 upper_left = (int(width / 2) - 5, int(height / 2) - 2)
 bottom_right = (int(width / 2) + 2, int(height / 2) + 2)
 
 ##Convert to HSV and LAB color spaces
 lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
 hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
 h,s,v = cv2.split( hsv);
 l,a,b = cv2.split(lab);
 a_blur = finalBlur(img, a)
 cv2.imshow('Original',img)
 
 ##Perform linear operation on various channels, values and channels selected through experimentation
 vby4 = np.floor_divide(v,4)
 sub = np.subtract(a,vby4)
 cv2.imshow('Linear combination of Channels',sub)
 sub_blur_a_modified = bright(sub) ##Increase the contrast of the output frame
 sub_blur_a = finalBlur(img, sub_blur_a_modified) ##Increasing Contrast increases noise so get rid of them
 cv2.imshow('sub a mod',sub_blur_a_modified)
 
 ###Write output video and original video to file
 outfile3 = cv2.cvtColor(sub_blur_a_modified, cv2.COLOR_GRAY2RGB)
 out3.write(outfile3)
 out4.write(originalImage)
 # Press Q on keyboard to exit
 if cv2.waitKey(1) & 0xFF == ord('q'):
   break
 # Break the loop
 else:
   break
   
   
# When everything done, release the video capture object
cap.release()
out3.release()
out4.release()
cv2.destroyAllWindows()
