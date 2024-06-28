# Function first tries to detect an aruco Code
# If an aruco Code was found it will move the robot to the right position until
# a push button is pressed
import numpy as np
#Move Arm to position to find aruco code
move_tool(0, 356, 828, [180,-17,-94])


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
pose_aruco_base=service_robot.cam_object_to_working_frame(aruco_transform_arm, camera_name, robot_arm_name,
 working_frame='base', O_r_Oo=None)

pos_xyz = [pose_aruco_base._Transform__translation.x,
    pose_aruco_base._Transform__translation.y,
    pose_aruco_base._Transform__translation.z]

pos_euler_xyz=pose_aruco_base._Transform__orientation.to_euler()

print("Aruco Position")
print(pose_aruco_base)


#Turning of Robot
distance_offset_y=800
deg_offset=0
distance_linear=(np.sqrt(pos_xyz[0]**2+pos_xyz[1]**2)-distance_offset_y)/1000
angle=np.rad2deg(np.arctan2(-pos_xyz[0],pos_xyz[1]))
print("Movement in x and y")
print(pos_xyz)
print("Movement linear")
print(distance_linear)
print("Angle to turn")
print(angle)
mobile_platform.move_platform_angular(angle, speed=0.07, blocking=True)
mobile_platform.move_platform_linear(-distance_linear, speed=0.07, blocking=True)
#mobile_platform.move_platform(0, 1000, 0, block=True, relative=False,goal_importance="high", linear_speed=None, angular_speed=None)
