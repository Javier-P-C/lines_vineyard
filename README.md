# lines_vineyard
ROS package for research of crop row detection in vineyards. Worked in ROS Noetic

## WEBCAM
Model: Logitech C525

Installation:

First install the v4l-util Ubuntu package. It is a collection of command-line V4L utilities used by the usb_cam package: 

$ sudo apt-get install v4l-utils 

Then install the ROS usb_cam package: 

$ sudo apt-get install ros-$ROS_DISTRO-usb-cam  

To verify the PC recognize the camera:

$ dmesg

To connect the camera with the ROS initialize a roscore and execute:

$ rosrun usb_cam usb_cam_node _video_device:=/dev/video0 _pixel_format:=yuyv  

Parameter "/dev/video0" can change depending on where is the device detected. (/dev/video2 worked for us)

If the error "Unable to locate package ros-noetic-usb-cam" appear, clone the package to your workspace/src:

$ git clone https://github.com/bosch-ros-pkg/usb_cam.git

Finally, to visualize the video run:

$ rosrun image_view image_view image:=/usb_cam/image_raw 
