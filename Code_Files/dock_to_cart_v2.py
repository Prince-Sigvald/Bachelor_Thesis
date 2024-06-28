#Creator:     Yan Gridling
#Date:        26.06.2024
#Version:     1.00
#Description: This script combines every important script to guarantee a smooth navigation to dock 
#             on to a laundry cart and is considered as the main file
import numpy as np
from Class_Compute_Navigation_Docking import Compute_Navigation_Docking

#Variables
Aruco_ID=10
Aruco_Size=5

#Creating navigation object
navigation_computer = Compute_Navigation_Docking(Aruco_ID, Aruco_Size)

def driving_iteration(navigation_computer, space_lio_aruco):
    navigation_computer.compute_pose_arm_to_aruco_code()
    navigation_computer.compute_navigation_values()
    mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
    mobile_platform.move_platform_linear(-navigation_computer.drive_distance_linear+space_lio_aruco, speed=0.07, blocking=True)
      


#Time duration for every linera movement iteration of the docking process in terms of the distance
dt=0.5

#Move Arm to position to start docking process
move_tool(0, 334, 770, [180,-25.6,-94])

#Computing navigation values
navigation_computer.compute_pose_arm_to_aruco_code()
navigation_computer.compute_navigation_values()

#if the aruco code is very twisted away from Lio, or Lio is to close for docking Lio will first align himself new to the marker
if(navigation_computer.turn_angle + navigation_computer.pose_arm_aruco_euler_y) > 40 or navigation_computer.drive_distance_linear < 0.05:
    navigation_computer.compute_starting_navigation()
    print("neu ausrichtung beginnt")
    print(navigation_computer.pose_arm_aruco_euler_y)
    #Execute movements for starting position
    mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
    mobile_platform.move_platform_linear(-navigation_computer.drive_distance_linear, speed=0.07, blocking=True)
    print("zurückdrehen beginnt")
    #turing the robot back for alignment
    mobile_platform.move_platform_angular(-navigation_computer.turn_angle + navigation_computer.pose_arm_aruco_euler_y, speed=0.07, blocking=True)
    print("zurückdrehen fertig")
#else Lio tries to drive to the aruco marker up to 20 cm close
else:
    driving_iteration(navigation_computer, 0.2)
    """
    navigation_computer.compute_pose_arm_to_aruco_code()
    navigation_computer.compute_navigation_values()
    mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
    mobile_platform.move_platform_linear(-navigation_computer.drive_distance_linear+0.20, speed=0.07, blocking=True)
    """
#the second movement iteration up to 6cm to the aruco marker
driving_iteration(navigation_computer, 0.07)
"""
navigation_computer.compute_pose_arm_to_aruco_code()
navigation_computer.compute_navigation_values()
mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
mobile_platform.move_platform_linear(-navigation_computer.drive_distance_linear+0.06, speed=0.07, blocking=True)
"""

#the third movement iteration 
driving_iteration(navigation_computer, 0)
"""
navigation_computer.compute_pose_arm_to_aruco_code()
navigation_computer.compute_navigation_values()
mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
mobile_platform.move_platform_linear(-navigation_computer.drive_distance_linear, speed=0.07, blocking=True)
"""
"""
while (navigation_computer.drive_distance_linear>0.02):

    print("Current distance to aruco code")
    print(navigation_computer.drive_distance_linear)
    print("Current turn angle")
    print (navigation_computer.turn_angle)

    print("Angle to aruco")
    print(navigation_computer.pose_arm_aruco_euler_y)
    

    if(navigation_computer.turn_angle >1.5 or navigation_computer.turn_angle <-1.5):
        if navigation_computer.turn_angle <0:
            angular_speed=-0.1
        else:
            angular_speed=0.1
        #angular_speed=np.deg2rad(navigation_computer.turn_angle)/dt
        #mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)#turning of Lio
    else:
        angular_speed=0
        
    
    mobile_platform.send_cmd_vel(-0.2, angular_speed, dt, blocking=True)
    #get computed driving values
    navigation_computer.compute_pose_arm_to_aruco_code()
    navigation_computer.compute_navigation_values()
"""
print("last iteration happend by")
print(navigation_computer.drive_distance_linear)

#docking finished


