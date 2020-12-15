#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState

if __name__ == "__main__":
  rospy.init_node("send_joints")
  pub = rospy.Publisher('joint_states', JointState, queue_size=1000)

  # Nombres de las articulaciones
  jnames = ("joint_0", "joint_1")
  # Configuracion articular deseada (en radianes)
  jvalues =  [1, -0.78]

  # Objeto (mensaje) de tipo JointState
  jstate = JointState()
  # Asignar valores al mensaje
  jstate.header.stamp = rospy.Time.now()
  jstate.name = jnames
  jstate.position = jvalues

  # Frecuencia del envio (en Hz)
  rate = rospy.Rate(100)
  # Bucle de ejecucion continua
  while not rospy.is_shutdown():
      # Tiempo actual (necesario como indicador para ROS)
      jstate.header.stamp = rospy.Time.now()
      # Publicar mensaje
      pub.publish(jstate)
      # Esperar hasta la siguiente iteracion
      rate.sleep()