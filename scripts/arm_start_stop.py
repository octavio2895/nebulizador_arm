#!/usr/bin/env python
#Arm v0.1
from tkinter import *
import rospy, math, time
from std_msgs.msg import Bool
from std_msgs.msg import Float64

run_var =False
pwr_state = False
home = False

def wind():
    rospy.init_node('start_stop', anonymous=True)
    pub = rospy.Publisher('/arm_start_stop', Bool, queue_size=10)
    pub1 = rospy.Publisher('/vel_1', Float64, queue_size=10)
    pub2 = rospy.Publisher('/vel_2', Float64, queue_size=10)
    pub3 = rospy.Publisher('/compressor_pwr', Bool, queue_size=10)
    pub4 = rospy.Publisher('/home_axis', Bool, queue_size=10)
    rate = rospy.Rate(10)

    window = Tk()
    window.title("Arm Start and Stop")
    window.geometry('300x250')
    lbl1 = Label(window, text="Start stop")
    lbl2 = Label(window, text="Compressor pwr")
    lbl1.grid(column=0, row=0)
    lbl2.grid(column=0, row=2)

    def clicked1():
        global run_var
        run_var = True
        rospy.loginfo(run_var)
        pub.publish(run_var)
        rate.sleep()
    
    btn1 = Button(window, text="Start", command=clicked1)
    
    def clicked2():
        global run_var
        run_var = False
        rospy.loginfo(run_var)
        pub.publish(run_var)
        rate.sleep()

    btn2 = Button(window, text="Stop", command=clicked2)
    
    def clicked3():
        global pwr_state
        pwr_state = True
        rospy.loginfo(pwr_state)
        pub3.publish(pwr_state)
        rate.sleep()
    
    btn3 = Button(window, text="Start", command=clicked3)
    
    def clicked4():
        global pwr_state
        pwr_state = False
        rospy.loginfo(pwr_state)
        pub3.publish(pwr_state)
        rate.sleep()

    btn4 = Button(window, text="Stop", command=clicked4)

    def clicked5():
        global home
        home = True
        rospy.loginfo(home)
        pub4.publish(home)
        rate.sleep()

    btn5 = Button(window, text="Home", command=clicked5)

    vel_1s = DoubleVar()
    vel_1s.set(0.15)
    def vel_1_c(vel_1):
        rospy.loginfo("vel_1: %s", vel_1)
        pub1.publish(float(vel_1))
        rate.sleep()

    w1 = Scale(window, from_=0, to=0.30, 
                       digits= 2, 
                       label= "Velo_1" , 
                       resolution=0.01, 
                       orient=HORIZONTAL, 
                       variable=vel_1s, 
                       command=vel_1_c)

    vel_2s = DoubleVar()
    vel_2s.set(0.20)
    def vel_2_c(vel_2):
        rospy.loginfo("vel_2: %s", vel_2)
        pub2.publish(float(vel_2))
        rate.sleep()


    w2 = Scale(window, from_=0, to=0.30,
                       digits= 2, 
                       label= "Velo_2", 
                       resolution=0.01, 
                       orient=HORIZONTAL, 
                       variable=vel_2s, 
                       command=vel_2_c)


    btn1.grid(column=1, row=0)
    btn2.grid(column=2, row=0)
    btn3.grid(column=1, row=2)
    btn4.grid(column=2, row=2)
    btn5.grid(column=2, row=4)

    w1.grid(column=0, row=3)
    w2.grid(column=0, row=4)
    window.mainloop()

if __name__== '__main__':
    try:
        wind()
    except rospy.ROSInterruptException: 
        pass