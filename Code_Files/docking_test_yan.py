# Function first tries to detect an aruco Code
# If an aruco Code was found it will move the robot to the right position until
# a push button is pressed
import numpy as np
from Class_Compute_Navigation_Docking import Compute_Navigation_Docking
#Move Arm to position to find aruco code   (0, 356, 828, [180,-17,-94])
move_tool(0, 334, 770, [180,-25.6,-94])


tcp = read_tcp_pose()
position = tcp[:3]
orientation = tcp[3]
#print(position)
#print(orientation)

#Work with aruco markers
tcp=service_robot.create_pose(position, orientation)

#Get transformation from aruco code to gripper
camera_name='LioGripper'  #as IP adress
marker_id = 10
marker_size= 5
aruco_transform_arm=service_robot.get_aruco_transform(camera_name, marker_size, marker_id, timeout=1.0)
#Transform into Working frame hence Base Frame
robot_arm_name="Lio"
pose_aruco_base=service_robot.cam_object_to_working_frame(aruco_transform_arm, camera_name, robot_arm_name, working_frame='base', O_r_Oo=None)

pos_xyz = [pose_aruco_base._Transform__translation.x,
    pose_aruco_base._Transform__translation.y,
    pose_aruco_base._Transform__translation.z]

pos_euler_xyz=pose_aruco_base._Transform__orientation.to_euler()

print("angle to aruco code")
print(pos_euler_xyz[1])
print("x and y to aruco code")
print(pose_aruco_base)


#Variables
Aruco_ID=10
Aruco_Size=5

#Creating navigation object
navigation_computer = Compute_Navigation_Docking(Aruco_ID, Aruco_Size)
navigation_computer.compute_pose_arm_to_aruco_code()
navigation_computer.compute_navigation_values()
print("angle to turn")
print(navigation_computer.turn_angle)
print("distance linear:")
print(navigation_computer.drive_distance_linear)


"""
#Turning of Robot
distance_offset_y=800
deg_offset=0
distance_linear=(np.sqrt(pos_xyz[0]**2+pos_xyz[1]**2)-distance_offset_y)/1000   #in meters
angle=np.rad2deg(np.arctan2(-pos_xyz[0],pos_xyz[1]))
print("Movement in x and y")
print(pos_xyz)
print("Movement linear")
print(distance_linear)
print("Angle to turn")
print(angle)
"""
#mobile_platform.move_platform_angular(angle, speed=0.07, blocking=True)
#mobile_platform.move_platform_linear(-distance_linear, speed=0.07, blocking=True)
#mobile_platform.move_platform(0, 1000, 0, block=True, relative=False,goal_importance="high", linear_speed=None, angular_speed=None)
