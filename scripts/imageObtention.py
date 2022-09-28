#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np 
from cv_bridge import CvBridge
import matplotlib.pyplot as plt

bridge_object = CvBridge() # create the cv_bridge object
image_received = 0 #Flag to indicate that we have already received an image
cv_image = 0 #This is just to create the global variable cv_image 

bridge = CvBridge()

pub=rospy.Publisher("segmented_image",Image,queue_size=10)

def filtroColor(image):
    #I resized the image so it can be easier to work with
    image = cv2.resize(image,(300,300))

    #Once we read the image we need to change the color space to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #Hsv limits are defined
    #here is where you define the range of the color youre looking for
    #each value of the vector corresponds to the H,S & V values respectively
    min_color = np.array([52,0,0])
    max_color = np.array([255,255,255])

    #This is the actual color detection 
    #Here we will create a mask that contains only the colors defined in your limits
    #This mask has only one dimension, so its black and white }
    mask_g = cv2.inRange(hsv, min_color, max_color)

    #We use the mask with the original image to get the colored post-processed image
    res_g = cv2.bitwise_and(image,image, mask= mask_g)
    return res_g

def show_image():
    image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,camera_callback)

    r = rospy.Rate(10) #10Hz 
    while not rospy.is_shutdown(): 
        if image_received:
            cv2.waitKey(1)
            r.sleep() 
    cv2.destroyAllWindows()

def camera_callback(data):
    global bridge_object
    global cv_image
    global image_received
    image_received=1
    try:
        print("received ROS image, I will convert it to opencv")
        # We select bgr8 because its the OpenCV encoding by default
        cv_image = bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        

        cv2.imshow('Normal',cv_image)
        #Add your code to save the image here
        
        image = filtroColor(cv_image)
        #Display the image in a window
        cv2.imshow('image',image)
        image_message = bridge.cv2_to_imgmsg(image, encoding="passthrough")
        pub.publish(image_message)
             
        #Save the image "img" in the current path 
        #cv2.imwrite('robot_image.jpg',cv_image)
        
    except CvBridgeError as e:
        print(e)
       

if __name__ == '__main__':
    rospy.init_node('opencv_example1', anonymous=True)
    show_image()