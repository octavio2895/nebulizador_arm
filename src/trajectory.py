#! /usr/bin/env python
import rospy
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

rospy.init_node('trajectory')
pub = rospy.Publisher('/joint_trajectory',JointTrajectory,queue_size=1000)
trajectory=JointTrajectory()
point=JointTrajectoryPoint()
trajectory.header.stamp=rospy.Time.now()
trajectory.header.frame_id = "base"

trajectory.joint_names.append("joint_1")
trajectory.joint_names.append("joint_2")
trajectory.joint_names.append("joint_3")
trajectory.joint_names.append("joint_4")
trajectory.joint_names.append("joint_5")
trajectory.joint_names.append("joint_6")

point.positions.append(0.0)
point.positions.append(0.0)
point.positions.append(0.3)
point.positions.append(0.6)
point.positions.append(0.5)
point.positions.append(10.0)

trajectory.points.append(point)
pub.publish(trajectory)