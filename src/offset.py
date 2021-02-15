#!/usr/bin/env python

from std_msgs.msg import UInt16
import numpy as np
import rospy, math, time
azim = 0
elev = 0

def offset_joint_azim_cb(data):
    rospy.loginfo(data.data)
    global azim
    azim = data.data

def offset_joint_elev_cb(data):
    rospy.loginfo(data.data)
    global elev
    elev = data.data

def offset_joint_azim():
    rospy.init_node('offset_joint_azim', anonymous=True)
    rospy.Subscriber("/offset_joint_azim", UInt16, offset_joint_azim_cb)
    rospy.Subscriber("/offset_joint_elev", UInt16, offset_joint_elev_cb)
    
    #rospy.spin()
    #azim = UInt16()
    #print(azim.data) 
    while  not rospy.is_shutdown():
        print(azim)
        print(elev)


if __name__== '__main__':
    try:
        offset_joint_azim()
    except  rospy.ROSInterruptException: pass