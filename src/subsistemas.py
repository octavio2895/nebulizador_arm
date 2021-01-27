#!/usr/bin/env python
from getkey import getkey, keys
import rospy, math, time
from std_msgs.msg import UInt32
from std_msgs.msg import Bool
from std_msgs.msg import Float32


def startneb():
    pub = rospy.Publisher('compressor_pwr', Bool, queue_size=10)
    rospy.init_node('pwr_cmd', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        key = getkey()
        if key == 'q':
            pwr_state = False
        elif key =='a':
            pwr_state = True
        else:
            break
            #rospy.spin()
        rospy.loginfo(pwr_state)
        pub.publish(pwr_state)
        rate.sleep()
    rospy.spin()

if __name__== '__main__':
    try:
        startneb()
    except rospy.ROSInterruptException: 
        pass