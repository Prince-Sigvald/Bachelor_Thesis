#Creator:     Yan Gridling
#Date:        26.06.2024
#Version:     1.00
#Description: Script contains all important functinos to gurantee a smooth docking process


import numpy as np
from Class_Compute_Navigation_Docking import Compute_Navigation_Docking

#navigation_computer: object of Class Compute_Navigation_Docking
#space_lio_aruco: remaining distance Lio to aruco code
#check_aligment: flag to align Lio a second time, especially neede in the last iteration
def driving_iteration(navigation_computer, space_lio_aruco, check_alignment=0):
    navigation_computer.compute_pose_arm_to_aruco_code()
    navigation_computer.compute_navigation_values()
    #if condition to avoid a iteration if robot is already to close
    if navigation_computer.drive_distance_linear > space_lio_aruco:
        if (np.abs(navigation_computer.turn_angle)>1): #only turn robot if angle exceeds certain value
            mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
            wait(0.2)
            print("turn angle:")
            print(navigation_computer.turn_angle)
            if check_alignment: #realign robot new, if check_aligment is set, normally on 0
                navigation_computer.compute_pose_arm_to_aruco_code()
                navigation_computer.compute_navigation_values()
                if(np.abs(navigation_computer.turn_angle)>1):
                    print("turn angle:")
                    print(navigation_computer.turn_angle)
                    mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
                    wait(0.2)
        
        mobile_platform.move_platform_linear(-navigation_computer.drive_distance_linear+space_lio_aruco, speed=0.07, blocking=True)
        wait(0.2)
    else:
        print("To close for movement itertation, hence iteration will be ignored")
  

#Aligns Lio new if the aruco marker is to far twisted away from Lio
def new_alignment():
    #Computation of new aligment values
    navigation_computer.compute_starting_navigation()
    print("New alignment begins")
    #Execute movements for starting position
    mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
    mobile_platform.move_platform_linear(-navigation_computer.drive_distance_linear, speed=0.07, blocking=True)
    #turing the robot back for alignment
    mobile_platform.move_platform_angular(-navigation_computer.turn_angle + navigation_computer.pose_arm_aruco_euler_y, speed=0.07, blocking=True)
    print("New alignment finished")

#Final docking phase with check, if cart is hooked
def final_docking(navigation_computer):
    navigation_computer.compute_pose_arm_to_aruco_code()
    navigation_computer.compute_navigation_values()
    while (True):
        mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
        navigation_computer.compute_pose_arm_to_aruco_code()
        navigation_computer.compute_navigation_values()
        if (np.abs(navigation_computer.turn_angle)> 2):#compensate oversteering
            mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
        mobile_platform.move_platform_linear(-navigation_computer.drive_distance_linear, speed=0.07, blocking=True)
        #Drive forward and see if cart moved
        mobile_platform.move_platform_linear(0.1, speed=0.07, blocking=True)
        wait(1)
        navigation_computer.compute_pose_arm_to_aruco_code()
        navigation_computer.compute_navigation_values()
        if(navigation_computer.drive_distance_linear < 0.05):
            print("Docking succesfull")
            break
    
    

        
    
