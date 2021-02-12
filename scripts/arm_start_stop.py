#!/usr/bin/env python

from tkinter import *
import rospy, math, time
from std_msgs.msg import Bool

run_var =False

def wind():
    rospy.init_node('start_stop', anonymous=True)
    pub = rospy.Publisher('/arm_start_stop', Bool, queue_size=10)
    rate = rospy.Rate(10)

    window = Tk()
    window.title("/arm_star_stop'")
    window.geometry('250x50')
    lbl = Label(window, text="start_stop")
    lbl.grid(column=0, row=0)

    def clicked():
        global run_var
        run_var = True
        rospy.loginfo(run_var)
        pub.publish(run_var)
        rate.sleep()
    
    btn1 = Button(window, text="Start", command=clicked)
    
    def _clicked():
        global run_var
        run_var = False
        rospy.loginfo(run_var)
        pub.publish(run_var)
        rate.sleep()

    btn2 = Button(window, text="Stop", command=_clicked)

    btn1.grid(column=1, row=0)
    btn2.grid(column=2, row=0)
    window.mainloop()

if __name__== '__main__':
    try:
        wind()
    except rospy.ROSInterruptException: 
        pass