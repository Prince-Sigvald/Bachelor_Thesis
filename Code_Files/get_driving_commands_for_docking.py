#Creator:     Yan Gridling
#Date:        26.06.2024
#Version:     1.00
#Description: This scrips runs parallel to the main script and uses the 
#             Compute_Navigation_Class to share the distance values with the main script

from Class_Compute_Navigation_Docking import Compute_Navigation_Docking

navigation_computer = Compute_Navigation_Docking(get_shared_variable("Aruco_ID"), get_shared_variable("Aruco_Size"))

    
while True:
    #Computational part
    navigation_computer.compute_pose_arm_to_aruco_code()
    navigation_computer.compute_navigation_values()
    #update shared variables
    set_shared_variable("angle_lio_to_aruco", navigation_computer.pose_arm_aruco_euler_xyz[1])
    set_shared_variable("movement_linear", navigation_computer.drive_distance_linear)
    set_shared_variable("angle_to_turn",  navigation_computer.turn_angle)
    """
    print("x und y werte")
    print("_________")
    print(navigation_computer.pose_arm_aruco_xyz)
    """
    """if(get_shared_variable("aligner_flag_on")):
    if(angle_lio_to_aruco > 3 or angle_lio_to_aruco< -3):
        print("Aligner adapted Lio's trajectory")
        mobile_platform.cancel_navigation_goal()
    """
print("Parallel script get_driving_commands_for_docking finsihed")
