#!/usr/bin/evn python
import numpy as np
import rospy, math, time
from trajectory_msgs.msg import JointTrajectoryPoint

def point():
    rospy.init_node('point_control')

    pub = rospy.Publisher('/arm_twist', JointTrajectoryPoint, queue_size=10)

    ang1 = 45*np.pi/180
    ang2 = 90*np.pi/180
    ang3 = 10*np.pi/180
    ang4 = ang1 + ang3
    ang5 = ang2 + ang3

    x1 =np.arange(-1*ang2,ang5,ang3)

    for i in x1:
        p = JointTrajectoryPoint()
        p.positions = [0,i]
        p.velocities = [0,0]
        p.accelerations = [0,0]
        p.time_from_start = rospy.Time.now()

        rospy.loginfo("point \n %s ", p)
        rospy.sleep(1)
        pub.publish(p)
    
    #while not rospy.is_shutdown():
    #rospy.loginfo("point \n %s ", p)
    #rospy.sleep(1)
    #pub.publish(p)
    rospy.spin()




if __name__=='__main__':
    try:
        point()
    except  rospy.ROSInterruptException: pass