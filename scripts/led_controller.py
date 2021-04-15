#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import UInt8MultiArray
import random
import colorsys

def talker():
    pub = rospy.Publisher('leds', UInt8MultiArray, queue_size=10)
    rospy.init_node('led_controller', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    led_list = [0, 0, 0]*100
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
	led_list.append(64)
	led_list.append(0)
	led_list.append(0)
	"""led_list.append(random.randint(0, 255))
	led_list.append(random.randint(0, 255))
	led_list.append(random.randint(0, 255))
	"""
	del led_list[0]
	del led_list[0]
	del led_list[0]
	p = UInt8MultiArray()
	p.data = led_list
	pub.publish(p) 
	rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
