#!/usr/bin/python3

#import lib
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

#This function is called to handle the subscribed messages
#Args: image_msg (Image): message type Image from sensor_msg
def callback(image_msg):
    try:
        cv_image=bridge.imgmsg_to_cv2(image_msg) #ROS message -> dinh dang OpenCV
        cv2.imshow('ROS Image Subscriber',cv_image) #hien thi hinh anh
        cv2.waitKey(10) #delay 10ms
    except CvBridgeError as error:
        print(error) 
           
#main         
if __name__=="__main__":
    bridge=CvBridge() #tao object CvBridge
    rospy.init_node("image_subscriber", anonymous=True) #khoi tao node image_subscriber  
    print("Subscribe image from topic /image_raw...")
    image_subscriber=rospy.Subscriber("image_raw",Image, callback) #khoi tao subscriber
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down!")    
        
        
    
  
  
