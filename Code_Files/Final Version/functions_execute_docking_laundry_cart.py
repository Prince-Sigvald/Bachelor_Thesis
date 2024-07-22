#Creator:     Yan Gridling
#Date:        26.06.2024
#Version:     1.00
#Description: Script contains all important functinos to gurantee a smooth docking process


import numpy as np
from Bachelorthesis_Yan.Class_Compute_Navigation_Docking import Compute_Navigation_Docking

def driving_iteration(navigation_computer, space_lio_aruco):
    """
    Turns and lets Lio drive backwards a up to a certain distance to a detected aruco marker

    Parameters:
    navigation_computer: Object which contains/compute values for driving commands
    space_lio_aruco: space left to aruco marker after iteration is done in meters

    Return:
    No return value
    """
    navigation_computer.compute_pose_arm_to_aruco_code()
    navigation_computer.compute_navigation_values()
    #if condition to avoid a iteration if robot is already to close
    if navigation_computer.drive_distance_linear > space_lio_aruco:
        if (np.abs(navigation_computer.turn_angle)>1): #only turn robot if angle exceeds certain value
            mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
            wait(0.2)
            print("turn angle:")
            print(navigation_computer.turn_angle)
        mobile_platform.move_platform_linear(-navigation_computer.drive_distance_linear+space_lio_aruco, speed=0.07, blocking=True)
        wait(0.2)
    else:
        print("To close for movement itertation, hence iteration will be ignored")
  

def new_alignment(navigation_computer):
    """
    Aligns Lio new infront of the aruco marker in a rectangular distance of the marker 
    (rectangular distance can be found in Class_Compute_Navigation_Docking as self.distance_offset_starting_navigation)

    Parameters:
    navigation_computer: Object which contains/compute values for driving commands

    Return:
    No return value
    """
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
def final_docking(navigation_computer, attempts):
    """
    Lets Lio drive the last piece to the aruco marker to dock to the cart and checks if the docking worked
    by driving forward and checking if the cart also moved
    If the cart stayed at its place the steps are repeated 
    
    
    Parameters:
    navigation_computer: Object which contains/compute values for driving commands
    attempts: additional attempts if cart was not hooked

    Return:
    No return value
    """
    navigation_computer.compute_pose_arm_to_aruco_code()
    navigation_computer.compute_navigation_values()
    for i in range(attempts):
        mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
        navigation_computer.compute_pose_arm_to_aruco_code()
        navigation_computer.compute_navigation_values()
        if (np.abs(navigation_computer.turn_angle)> 2):#compensate oversteering
            mobile_platform.move_platform_angular(navigation_computer.turn_angle, speed=0.07, blocking=True)
        #Drive backwards to marker
        mobile_platform.move_platform_linear(-navigation_computer.drive_distance_linear, speed=0.07, blocking=True)
        #Drive forward and see if cart moved
        mobile_platform.move_platform_linear(0.1, speed=0.07, blocking=True)
        wait(1)
        navigation_computer.compute_pose_arm_to_aruco_code()
        navigation_computer.compute_navigation_values()
        #if cart also moved, distance is below 0.05 m
        if(navigation_computer.drive_distance_linear < 0.05):
            print("Docking succesfull")
            break
        if(i==attempts):
            print("Docking failed!")
    
    

        
    
