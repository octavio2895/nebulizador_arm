# nebulizador_arm
Paquete para mover la herramienta de un nebulizador, atraves de un codigo de python utilizando: joint state publisher y JointTrajectoryPoint

# Conectase a la placa Tenssy y enviar mensaje jointTajectoryPoint
Este es un menasje continuo periodico para el movimiento del brazo nebulizador.
```
roslaunch nebulizador_arm arm_serial_point.launch
```