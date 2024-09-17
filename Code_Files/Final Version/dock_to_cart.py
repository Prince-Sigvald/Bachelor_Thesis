#Creator:     Yan Gridling
#Date:        26.06.2024
#Version:     1.07
#Description: This script combines every important script to guarantee a smooth navigation to dock 
#             on to a laundry cart and is considered as the main file
#             In addiont, this file only serves as an example usage of the modular program structure 
#             for further applications done by F&P 

import numpy as np
from Bachelorthesis_Yan.functions_execute_docking_laundry_cart import *
from Bachelorthesis_Yan.Class_Compute_Navigation_Docking import Compute_Navigation_Docking


#Variables
Aruco_ID=10 #Aruco ID on which Lio will dock on
Aruco_Size=5 #Size of previously mentiond marker in cm
steepest_docking_angle=40#if this angle to the aruco is exceeded, the Lio aligns himself new

#Creating navigation object with corresponding aruco code
navigation_computer = Compute_Navigation_Docking(Aruco_ID, Aruco_Size)

#Move Arm to position to start docking process
move_to_pose("Scan_Pose_Aruco_Docking_V2")
#Open Gripper
move_gripper(30)

#Computing navigation values and check if aruco marker was detected
if(navigation_computer.compute_pose_arm_to_aruco_code()!=0):
    navigation_computer.compute_navigation_values()
    #if the aruco code is very twisted away from Lio, or Lio is to close for docking Lio will first 
    #align himself new to the marker
    if np.abs(-navigation_computer.turn_angle + navigation_computer.pose_arm_aruco_euler_y) > steepest_docking_angle or navigation_computer.drive_distance_linear < 0.05:
        new_alignment(navigation_computer)

    #else Lio tries to drive to the aruco marker up to 30 cm close
    else:
        driving_iteration(navigation_computer, 0.4)
        print("first iteratinon done")
    #the second movement iteration up to 10cm to the aruco marker
    driving_iteration(navigation_computer, 0.10)
    print("second iteratinon done")
    
    #final docking phase
    final_docking(navigation_computer, 5)
    print("Docking finished")
    
else:
    print("No Cart found")


