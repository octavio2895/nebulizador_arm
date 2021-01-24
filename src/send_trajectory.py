#!/usr/bin/env python

import rospy, math, time

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

def jointTrajectoryCommand():
    # Initialize the node
    rospy.init_node('joint_control')

    print rospy.get_rostime().to_sec()
    while rospy.get_rostime().to_sec() == 0.0:
        time.sleep(0.1)
        print rospy.get_rostime().to_sec()

    pub = rospy.Publisher('/arm_twist', JointTrajectory, queue_size=10)
    jt = JointTrajectory()

    jt.header.stamp = rospy.Time.now()
    jt.header.frame_id = "arm"

    jt.joint_names.append("joint_azim" )
    jt.joint_names.append("joint_elev" )
    
    n = 15
    dt = 0.01
    rps = 0.05
    for i in range (n):
        p = JointTrajectoryPoint()
        theta = rps*2.0*math.pi*i*dt
        x1 = -0.5*math.sin(2*theta)
        x2 =  0.5*math.sin(1*theta)

        p.positions.append(x1)
        p.positions.append(x2)
        
        jt.points.append(p)

        # set duration
        jt.points[i].time_from_start = rospy.Duration.from_sec(dt)
        rospy.loginfo("test: angles[%d][%f, %f]",n,x1,x2)

    pub.publish(jt)
    rospy.spin()

if __name__ == '__main__':
    try:
        jointTrajectoryCommand()
    except rospy.ROSInterruptException: pass