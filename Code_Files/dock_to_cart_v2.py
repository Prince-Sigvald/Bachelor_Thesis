#Creator:     Yan Gridling
#Date:        26.06.2024
#Version:     1.00
#Description: This script combines every important script to guarantee a smooth navigation to dock 
#             on to a laundry cart and is considered as the main file

import numpy as np
from functions_execute_docking_laundry_cart import *
from Class_Compute_Navigation_Docking import Compute_Navigation_Docking

#Variables
Aruco_ID=10
Aruco_Size=5

#Creating navigation object
navigation_computer = Compute_Navigation_Docking(Aruco_ID, Aruco_Size)

#Move Arm to position to start docking process
#move_tool(0, 334, 770, [180,-25.6,-94])
move_to_pose("Scan_Pose_Aruco_Docking_V2")

#Computing navigation values and determine if Lio is to far twisted away from cart
if(navigation_computer.compute_pose_arm_to_aruco_code()!=0):
    navigation_computer.compute_navigation_values()
    #if the aruco code is very twisted away from Lio, or Lio is to close for docking Lio will first align himself new to the marker
    if np.abs(navigation_computer.turn_angle + navigation_computer.pose_arm_aruco_euler_y) > 40 or navigation_computer.drive_distance_linear < 0.05:
        new_alignment()
    #else Lio tries to drive to the aruco marker up to 30 cm close
    else:
        driving_iteration(navigation_computer, 0.3)
        print("first iteratinon done")
    
    #the second movement iteration up to 7cm to the aruco marker
    driving_iteration(navigation_computer, 0.07)
    print("second iteratinon done")
    
    #final docking phase
    final_docking(navigation_computer)

    #docking finished
else:
    print("Docking failed no aruco marker detected")


