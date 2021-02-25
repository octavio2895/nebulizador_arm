#!/usr/bin/env python
import numpy as np
import rospy, math, time
from std_msgs.msg import Bool
from std_msgs.msg import UInt16
from std_msgs.msg import Float64
from trajectory_msgs.msg import JointTrajectoryPoint
run_var = False
transition = False
azim = 0
elev = 0
vel_1 = 0.15
vel_2 = 0.20
ang1v = 0
ang2v = 0
vel_1v = 0
vel_2v = 0

param_change_flag = True

def run_cb(data):
    global run_var 
    rospy.loginfo(data.data)
    if data.data == True:
        run_var = True
    else:
        run_var = False
def offset_joint_azim_cb(data):
    global param_change_flag
    param_change_flag = True
    rospy.loginfo(data.data)
    global azim
    azim = data.data

def offset_joint_elev_cb(data):
    global param_change_flag
    param_change_flag = True
    rospy.loginfo(data.data)
    global elev
    elev = data.data

def vel_1_cb(data):
    global param_change_flag
    param_change_flag = True
    rospy.loginfo(data.data)
    global vel_1
    vel_1 = data.data

def vel_2_cb(data):
    global param_change_flag
    param_change_flag = True
    rospy.loginfo(data.data)
    global vel_2
    vel_2 = data.data

def point():
    global param_change_flag
    global transition
    global ang1v, ang2v, vel_1v, vel_2v

    rospy.init_node('point_control')

    pub = rospy.Publisher('/arm_twist', JointTrajectoryPoint, queue_size=10)
    pub_fp = rospy.Publisher('/arm_fp', Float64, queue_size=10)
    pub_pv1 = rospy.Publisher('/pv1', Float64, queue_size=10)
    pub_pn1 = rospy.Publisher('/pn1', Float64, queue_size=10)
    pub_mix1 = rospy.Publisher('/mix1', Float64, queue_size=10)

    rospy.Subscriber('/arm_start_stop', Bool, run_cb)

    rospy.Subscriber("/offset_joint_azim", UInt16, offset_joint_azim_cb)
    rospy.Subscriber("/offset_joint_elev", UInt16, offset_joint_elev_cb)
    
    rospy.Subscriber("/vel_1", Float64, vel_1_cb)
    rospy.Subscriber("/vel_2", Float64, vel_2_cb)

    grados_joint_azim = rospy.get_param("/grados_joint_azim", 360)
    rospy.loginfo("%s is %s", rospy.resolve_name('grados_joint_azim'), grados_joint_azim)

    grados_joint_elev = rospy.get_param("/grados_joint_elev", 45)
    rospy.loginfo("%s is %s", rospy.resolve_name("/grados_joint_elev"),grados_joint_elev)

    ang1 = grados_joint_azim*np.pi/180 #np.pi*2
    ang2 = grados_joint_elev*np.pi/180 #np.pi*3/4

    offset_joint_azim = rospy.get_param("/offset_joint_azim", 0)
    rospy.loginfo("%s is %s", rospy.resolve_name("/offset_joint_azim"), offset_joint_azim)

    offset_joint_elev = rospy.get_param("/offset_joint_elev", 0)
    rospy.loginfo("%s is %s", rospy.resolve_name("/offset_joint_elev"), offset_joint_elev)

    ang1_offset = offset_joint_azim*np.pi/180 #np.pi*2
    ang2_offset = offset_joint_elev*np.pi/180 #np.pi*3/4


    pub_period = 0.05

    #vel_1 = rospy.get_param("/vel_1")
    #rospy.loginfo("%s is %s", rospy.resolve_name('/vel_1'),vel_1)

    #vel_2 = rospy.get_param("/vel_2")
    #rospy.loginfo("%s is %s", rospy.resolve_name('/vel_2'),vel_2)
    start_time = time.time()
    time.sleep(0.01)
    next_point_time = 0
    dt = 0
    tau = 1.0
    while not rospy.is_shutdown():
        if(time.time() > next_point_time) and run_var==True:
            dt = time.time() - start_time
            if param_change_flag == True:
                param_change_flag = False
                transition = True
                dtv = dt
                
            if transition == True:
                fp = ((6/tau**5)*((dt-dtv)**5)) -((15/tau**4)*(dt-dtv)**4)+ ((10/tau**3)*(dt-dtv)**3)
                if fp < 1: #Transcion
                    p = JointTrajectoryPoint()
                    #
                    pv1 = ang1v*np.sin((vel_1v*dt)*2*np.pi) + ang1_offset
                    pn1 = ang1*np.sin((vel_1*dt)*2*np.pi) + ang1_offset

                    pvv1 = vel_1v*2*np.pi*ang1v*np.cos((vel_1v*(dt-pub_period))*2*np.pi)
                    pnv1 = vel_1*2*np.pi*ang1*np.cos((vel_1*(dt-pub_period))*2*np.pi)

                    pv2 = ang2v*np.sin((vel_2v*dt)*2*np.pi) + ang2_offset
                    pn2 = ang2*np.sin((vel_2*dt)*2*np.pi) + ang2_offset

                    pvv2 = vel_2v*2*np.pi*ang2v*np.cos((vel_2v*dt)*2*np.pi)
                    pnv2 = vel_2*2*np.pi*ang2*np.cos((vel_2*dt)*2*np.pi)
                    ##Position#
                    mix1 = fp*pn1 + (1-fp)*pv1
                    mix2 = fp*pn2 + (1-fp)*pv2
                    ##Vel##
                    mixv1 = fp*pnv1 + (1-fp)*pvv1
                    mixv2 = fp*pnv2 + (1-fp)*pvv2

                    i = mix1
                    j = mix2

                    k = mixv1
                    l = mixv2

                    p.positions = [i,j]
                    p.velocities = [k,l]
                    p.accelerations = [0,0]
                    p.time_from_start = rospy.Time.now()
                    rospy.loginfo("point trans \n %s ", p)
                    rospy.loginfo(fp)
                    pub.publish(p)
                    ### graficar ###
                    pub_pv1.publish(pv1)
                    pub_pn1.publish(pn1)
                    pub_mix1.publish(mix1)
                    pub_fp.publish(fp)
                    ###

                else:
                    transition = False
                
            else:  #Estado Estable #Dentro de transicion OJO no sabemso si la funcion es monotonica
                p = JointTrajectoryPoint()
                i = ang1*np.sin((vel_1*dt)*2*np.pi) + ang1_offset
                j = ang2*np.sin((vel_2*dt)*2*np.pi) + ang2_offset
                k = vel_1*2*np.pi*ang1*np.cos((vel_1*(dt-pub_period))*2*np.pi)
                l = vel_2*2*np.pi*ang2*np.cos((vel_2*dt)*2*np.pi)

                vel_1v = vel_1
                vel_2v = vel_2
                dtv = dt
                ang1v = ang1
                ang2v = ang2

                p.positions = [i,j]
                p.velocities = [k,l]
                p.accelerations = [0,0]
                p.time_from_start = rospy.Time.now()
                rospy.loginfo("point \n %s ", p)
                pub.publish(p)
            next_point_time = time.time() + pub_period

               

        elif run_var == False:
                start_time = time.time() + dt

if __name__=='__main__':
    try:
        point()
    except  rospy.ROSInterruptException: pass