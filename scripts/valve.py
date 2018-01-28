#!/usr/bin/env python
import numpy as np
import rospy, math, time
from std_msgs.msg import Bool
from std_msgs.msg import UInt16, UInt32

valve_state_commanded = False
valve_apperture_commanded = 0
compressor_pwr_commanded = False
power_sequence_step = 0
last_apperture_sent = 0
new_apperture_ready = True
valve_locked = True
valve_apperture = 0
is_locked = False

def valve_open_cmd(data):
    global valve_state_commanded
    valve_state_commanded = data.data

def valve_apperture_cmd(data):
    global valve_apperture_commanded
    global new_apperture_ready
    valve_apperture_commanded = data.data
    new_apperture_ready = True

def compressor_pwr_cmd_cb(data):
    global compressor_pwr_commanded
    compressor_pwr_commanded = data.data

def point():
    global compressor_pwr_commanded
    global valve_apperture_commanded
    global valve_state_commanded
    global power_sequence_step
    global last_apperture_sent
    global new_apperture_ready
    global valve_locked
    global valve_apperture
    global is_locked

    compressor_state = False #TODO make this a topic published by micro

    rospy.init_node('spray_valve_control')

    spray_pub = rospy.Publisher('/spray_valve', UInt32 , queue_size=10)
    compressor_pub = rospy.Publisher("/compressor_pwr", Bool, queue_size=10)
    rospy.Subscriber('/spray_valve_open_close', Bool, valve_open_cmd)
    rospy.Subscriber("/spray_valve_apperture", UInt32, valve_apperture_cmd)
    rospy.Subscriber("/compressor_pwr_cmd", Bool, compressor_pwr_cmd_cb)

    pub_period = 0.05

    VALVE_APPERTURE_CLOSED = rospy.get_param("/valve_apperture_closed", 0) #in percentage
    VALVE_SERVO_TIMER = rospy.get_param("/valve_servo_timer", 2000) #in millisecond
    COMPRESSOR_START_TIME = rospy.get_param("/compressor_start_time", 2000) #in millisecond

    #vel_2 = rospy.get_param("/vel_2")
    #rospy.loginfo("%s is %s", rospy.resolve_name('/vel_2'),vel_2)

    start_time = time.time()
    next_point_time = 0
    dt = 0

    while not rospy.is_shutdown():
         
        if valve_state_commanded == True:
            valve_apperture = valve_apperture_commanded
        else:
            valve_apperture = VALVE_APPERTURE_CLOSED
 
        if compressor_pwr_commanded == True and compressor_state == False: #Powering up
            if power_sequence_step == 0:
                valve_locked = True
                rospy.loginfo("Closing valve...")
                valve_timer = time.time() + (VALVE_SERVO_TIMER/1000)
                power_sequence_step += 1

            elif power_sequence_step == 1:
                if(time.time() >= valve_timer):
                    power_sequence_step += 1
                    rospy.loginfo("Valve closed.")

            elif power_sequence_step == 2:
                rospy.loginfo("Compressor is starting...")
                data = Bool()
                data.data = True
                compressor_pub.publish(data)
                power_sequence_step += 1
                compressor_timer = time.time() + (COMPRESSOR_START_TIME/1000)

            elif power_sequence_step == 3:
                if(time.time() >= compressor_timer):
                    rospy.loginfo("Compressor started.")
                    compressor_state = True
                    power_sequence_step = 0
                    valve_locked = False


        elif compressor_pwr_commanded == False and compressor_state == True:
            if power_sequence_step == 0:
                rospy.loginfo("Closing valve...")
                valve_timer = time.time() + (VALVE_SERVO_TIMER/1000)
                power_sequence_step += 1
                valve_locked = True

            elif power_sequence_step == 1:
                if(time.time() >= valve_timer):
                    power_sequence_step += 1
                    rospy.loginfo("Valve closed.")

            elif power_sequence_step == 2:
                rospy.loginfo("Compressor is stopping...")
                data = Bool()
                data.data = False
                compressor_pub.publish(data)
                power_sequence_step += 1
                compressor_timer = time.time() + (COMPRESSOR_START_TIME/1000)

            elif power_sequence_step == 3:
                if(time.time() >= compressor_timer):
                    rospy.loginfo("Compressor stopped.")
                    compressor_state = False
                    power_sequence_step = 0
        
        if valve_locked == True:
            valve_apperture = VALVE_APPERTURE_CLOSED
        
        if(last_apperture_sent != valve_apperture):
            data = UInt32()
            rospy.loginfo("New apperture set: %d", valve_apperture)
            data.data = valve_apperture
            spray_pub.publish(data)
            last_apperture_sent = valve_apperture
            rospy.loginfo("New apperture sent.")



if __name__=='__main__':
    try:
        point()
    except  rospy.ROSInterruptException: pass
