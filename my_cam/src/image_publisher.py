#!/usr/bin/python3

# import library
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

# Capture frames from a camera and publish it to the topic /image_raw
def publish_image():
    image_pub = rospy.Publisher("image_raw", Image, queue_size=10) # tao publisher image_raw
    bridge = CvBridge() # tao object CvBridge
    capture = cv2.VideoCapture("/dev/video0") # tao video_capture object doc anh tu webcam
# kiem tra xem Node có dang chay hay khong
    while not rospy.is_shutdown():
        # Capture a frame
        ret, img = capture.read()
        if not ret:
            rospy.ERROR("Could not grab a frame!")
            break
        # Publish the image to the topic image_raw
        try:
            img_msg = bridge.cv2_to_imgmsg(img, "bgr8") # chuyen thanh ROS message dang img_msg
            image_pub.publish(img_msg)
        except CvBridgeError as error:
            print(error)

# main
if __name__=="__main__":
    rospy.init_node("my_cam", anonymous=True)
    print("Image is being published to the topic /image_raw ...")
    publish_image()
    try:
        rospy.spin() # giu Node khong tat den khi nhan Ctrl+C
    except KeyboardInterrupt:
        print("Shutting down!")

