from tkinter import *
import rospy, math, time
from std_msgs.msg import Bool
from std_msgs.msg import Int32
from sensor_msgs.msg import JointState

#https://likegeeks.com/es/ejemplos-de-la-gui-de-python/
#https://docs.ros.org/en/indigo/api/rviz_python_tutorial/html/
pwr_state =False

def wind():
    pub1 = rospy.Publisher('compressor_pwr', Bool, queue_size=10)
    #pub2 = rospy.Publisher('State_joint', Int32 , queue_size=10)
    pub2 = rospy.Publisher('joint_state',JointState,queue_size=10)
    rospy.init_node('pwr_cmd', anonymous=True)
    rate = rospy.Rate(10)

    window = Tk()
    window.title("Compressor_pwr")
    window.geometry('250x150')
    lbl = Label(window, text="Pwr State")
    lbl.grid(column=0, row=0)

    def clicked():
        p =Bool()
        p.data = True
        rospy.loginfo(p)
        pub1.publish(p)
        #global pwr_state
        #pwr_state = True
        #rospy.loginfo(pwr_state)
        #pub.publish(pwr_state)
        rate.sleep()
    
    btn1 = Button(window, text="True", command=clicked)
    
    def _clicked():
        global pwr_state
        pwr_state = False
        rospy.loginfo(pwr_state)
        pub1.publish(pwr_state)
        rate.sleep()

    btn2 = Button(window, text="False", command=_clicked)

    def joint1_val(val):
        val =float(val)
        s = JointState()
        s.position = [val,0]
        rospy.loginfo(s)
        pub2.publish(s)
        rate.sleep()


    w1 = Scale(window, from_=-90, to=90, orient=HORIZONTAL, command=joint1_val)


    def _joint1_val(val2):
        val2 =float(val2)
        x = JointState()
        x.position = [0,val2]
        rospy.loginfo(x)
        pub2.publish(x)
        rate.sleep()

    w2 = Scale(window, from_=-45, to=45, orient=HORIZONTAL, command=joint1_val)

    btn1.grid(column=1, row=0)
    btn2.grid(column=2, row=0)

    w1.grid(column=0, row=2)
    w2.grid(column=0, row=3)

    window.mainloop()

if __name__== '__main__':
    try:
        wind()
    except rospy.ROSInterruptException: 
        pass