#!/usr/bin/env python
import numpy as np
import rospy, math, time
from std_msgs.msg import Bool
from std_msgs.msg import UInt16
from std_msgs.msg import Float64
from sensor_msgs.msg import Joy
from trajectory_msgs.msg import JointTrajectoryPoint
run_var = False
joy_dz = 0.2
joy_r_v = [0]
joy_r_h = [0]
joy_meas_id = 0
joy_r_v_avg = 0
joy_r_h_avg = 0
joy_r_prev_v = 0
joy_r_prev_h = 0
dt = 0
previous_t = 0
commanded_elev = 0
commanded_azim = 0
def run_cb(data):
    global run_var 
    rospy.loginfo(data.data)
    if data.data == True:
        run_var = False
    else:
        run_var = True

def joy_cb(data):
    global dt
    global joy_dz
    global previous_t
    global joy_r_v
    global joy_r_prev_v
    global joy_r_h
    global joy_r_prev_h
    global joy_r_v_avg
    global joy_r_h_avg
    global joy_meas_id

    dt = (float(data.header.stamp.secs)+(float(float(data.header.stamp.nsecs)/1000000000))) - previous_t
    previous_t = (float(data.header.stamp.secs)+(float(float(data.header.stamp.nsecs)/1000000000)))
    joy_raw_r_v = data.axes[3]
    joy_raw_r_h = data.axes[2]

    #rospy.loginfo(dt)

    if abs(joy_raw_r_v) < joy_dz:
        joy_raw_r_v = 0
    elif joy_raw_r_v > 0:
        joy_raw_r_v -= joy_dz
    else:
        joy_raw_r_v += joy_dz
    if abs(joy_raw_r_h) < joy_dz:
        joy_raw_r_h = 0
    elif joy_raw_r_h > 0:
        joy_raw_r_h -= joy_dz
    else:
        joy_raw_r_h += joy_dz

    if joy_meas_id < len(joy_r_v):
        
        joy_r_v[joy_meas_id] = joy_raw_r_v 
        joy_r_h[joy_meas_id] = joy_raw_r_h 
        joy_meas_id += 1

    else:
        joy_meas_id = 0

    joy_r_v_avg = joy_r_prev_v
    joy_r_h_avg = joy_r_prev_h
    joy_r_prev_v = sum(joy_r_v)/len(joy_r_v)
    joy_r_prev_h = sum(joy_r_h)/len(joy_r_h)
    
def point():
    global joy_r_v_avg
    global joy_r_h_avg
    global commanded_elev
    global commanded_azim
    rospy.init_node('manual_arm_control')

    pub = rospy.Publisher('/arm_twist', JointTrajectoryPoint, queue_size=10)
    rospy.Subscriber('/arm_start_stop', Bool, run_cb)
    rospy.Subscriber("/joystick_local", Joy, joy_cb)

    MAX_AZIM = rospy.get_param("/max_azimuth", np.pi*2)
    MIN_AZIM = rospy.get_param("/min_azimuth", -np.pi*2)
    MAX_ELEV = rospy.get_param("/max_elevation", np.pi/4)
    MIN_ELEV = rospy.get_param("/min_elevation", -np.pi/4)
    AZIM_MAX_SPEED = rospy.get_param("/max_azimuth_speed", np.pi/2)
    ELEV_MAX_SPEED = rospy.get_param("/max_elev_speed", np.pi/16)

    while not rospy.is_shutdown():
        
        if run_var==True:
            
            commanded_elev_speed = joy_r_v_avg*ELEV_MAX_SPEED
            commanded_elev += commanded_elev_speed*dt
            commanded_azim_speed = joy_r_h_avg*AZIM_MAX_SPEED
            if commanded_azim_speed > 0:
                commanded_azim = 100
            else:
                commanded_azim = -100
            
            if commanded_azim > MAX_AZIM:
                commanded_azim = MAX_AZIM
                #commanded_azim_speed = 0
            elif commanded_azim < MIN_AZIM:
                commanded_azim = MIN_AZIM
                #commanded_azim_speed = 0
            if commanded_elev > MAX_ELEV:
                commanded_elev = MAX_ELEV
                #commanded_elev_speed = 0
            elif commanded_elev < MIN_ELEV:
                commanded_elev = MIN_ELEV
                #commanded_elev_speed = 0
            
            p = JointTrajectoryPoint()
            azim = commanded_azim 
            elev = commanded_elev 
            azim_speed = commanded_azim_speed 
            elev_speed = commanded_elev_speed 
            p.positions = [commanded_azim, commanded_elev]
            p.velocities = [commanded_azim_speed*8, commanded_elev_speed*2]
            p.accelerations = [0,0]
            p.time_from_start = rospy.Time.now()
            rospy.loginfo("%s ", p)
            pub.publish(p)
        
        '''elif run_var == False:''' #TODO Set zero to current joint positions to avoid jumps


if __name__=='__main__':
    try:
        point()
    except  rospy.ROSInterruptException: pass
