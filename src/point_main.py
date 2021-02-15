#!/usr/bin/env python
import numpy as np
import rospy, math, time
from std_msgs.msg import Bool
from std_msgs.msg import UInt16
from trajectory_msgs.msg import JointTrajectoryPoint
run_var = False

def run_cb(data):
    global run_var 
    rospy.loginfo(data.data)
    if data.data == True:
        run_var = True
    else:
        run_var = False

def point():
    rospy.init_node('point_control')

    pub = rospy.Publisher('/arm_twist', JointTrajectoryPoint, queue_size=10)
    rospy.Subscriber('/arm_start_stop', Bool, run_cb)

    grados_joint_azim = rospy.get_param("/grados_joint_azim")
    rospy.loginfo("%s is %s", rospy.resolve_name('grados_joint_azim'), grados_joint_azim)

    grados_joint_elev = rospy.get_param("/grados_joint_elev")
    rospy.loginfo("%s is %s", rospy.resolve_name("/grados_joint_elev"),grados_joint_elev)

    ang1 = grados_joint_azim*np.pi/180 #np.pi*2
    ang2 = grados_joint_elev*np.pi/180 #np.pi*3/4

    offset_joint_azim = rospy.get_param("/offset_joint_azim")
    rospy.loginfo("%s is %s", rospy.resolve_name("/offset_joint_azim"), offset_joint_azim)

    offset_joint_elev = rospy.get_param("/offset_joint_elev")
    rospy.loginfo("%s is %s", rospy.resolve_name("/offset_joint_elev"), offset_joint_elev)

    ang1_offset = offset_joint_azim*np.pi/180 #np.pi*2
    ang2_offset = offset_joint_elev*np.pi/180 #np.pi*3/4


    pub_period = 0.05

    vel_1 = rospy.get_param("/vel_1")
    rospy.loginfo("%s is %s", rospy.resolve_name('/vel_1'),vel_1)

    vel_2 = rospy.get_param("/vel_2")
    rospy.loginfo("%s is %s", rospy.resolve_name('/vel_2'),vel_2)

    #vel_1 = 0.25 #rad/s
    #vel_2 = 0.10

    #pas1 = 10*np.pi/180
    #pas2 = 20*np.pi/180

    #max1 = ang1 + pas2
    #max2 = ang2 + pas1

    start_time = time.time()
    time.sleep(0.01)
    next_point_time = 0
    dt = 0
    while not rospy.is_shutdown():
        #print(run_var)
        if(time.time() > next_point_time) and run_var==True:
            dt = time.time() - start_time
            p = JointTrajectoryPoint()
            i = ang1*np.sin((vel_1*dt)*2*np.pi) + ang1_offset
            j = ang2*np.sin((vel_2*dt)*2*np.pi) + ang2_offset
            k = vel_1*2*np.pi*ang1*np.cos((vel_1*(dt-pub_period))*2*np.pi)
            l = vel_2*2*np.pi*ang2*np.cos((vel_2*dt)*2*np.pi)
            p.positions = [i,j]
            p.velocities = [k,l]
            p.accelerations = [0,0]
            p.time_from_start = rospy.Time.now()

            rospy.loginfo("point \n %s ", p)
            pub.publish(p)
            # rospy.spin()
            next_point_time = time.time() + pub_period
        elif run_var == False:
            start_time = time.time() + dt

    # x1 =np.arange(-1*ang1,max1,pas2)
    # print(x1)
    # x2 =np.arange(-1*ang2,max2,pas1)
    
    # for i, j in zip(x1, x2):
    #     p = JointTrajectoryPoint()
    #     p.positions = [i,j]
    #     p.velocities = [0,0]
    #     p.accelerations = [0,0]
    #     p.time_from_start = rospy.Time.now()

    #     rospy.loginfo("point \n %s ", p)
    #     rospy.sleep(1)
    #     pub.publish(p)
    
    # #while not rospy.is_shutdown():
    # #rospy.loginfo("point \n %s ", p)
    # #rospy.sleep(1)
    # #pub.publish(p)
    # rospy.spin()

if __name__=='__main__':
    try:
        point()
    except  rospy.ROSInterruptException: pass