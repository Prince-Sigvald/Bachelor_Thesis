#Creator:     Yan Gridling
#Date:        26.06.2024
#Version:     1.00
#Description: This script combines every important script to guarantee a smooth navigation to dock 
#             on to a laundry cart and is considered as the main file

#shared Variables through Scripts
set_shared_variable("Aruco_Size", 5)#important if Aruco Size would be changed
set_shared_variable("Aruco_ID", 10)# This ID determines on which cart Lio dock on
set_shared_variable("movement_linear", 0)
set_shared_variable("angle_to_turn", 0)
set_shared_variable("angle_lio_to_aruco", 0)

#Time duration for every linera movement iteration of the docking process in terms of the distance
dt=1

#Move Arm to position to start docking process
move_tool(0, 334, 770, [180,-25.6,-94])

#Starting of parallel script to compute navigation values
start_parallel_script("get_driving_commands_for_docking")


while(get_shared_variable("angle_to_turn")==0):#Waiting for first computation of relativ positon of Lio to aruco code
    wait(0.1)

#if(0):#wenn winkel von marker zu lio zu gross, dann fahren wir ausrichtungsposition and!

#First time getting shared navigation variables
#mobile_platform.move_platform_angular(angle, speed=0.07, blocking=True)
distance=get_shared_variable("movement_linear")
angle=get_shared_variable("angle_to_turn")


while (distance>0.4):
    print("Current distance to aruco code")
    print(distance)
    print("Current turn angle")
    print (angle)
    #adapt dt
    if(distance > 0.5):
        dt=distance*2
    else:
        dt=1
    
    if(angle >2 or angle <-2):
        mobile_platform.move_platform_angular(angle, speed=0.07, blocking=True)#turning of Lio
    mobile_platform.send_cmd_vel(-0.2, 0, dt, blocking=True)
    #get computed driving values
    angle=get_shared_variable("angle_to_turn")
    distance=get_shared_variable("movement_linear")
    wait(0.2)

distance=get_shared_variable("movement_linear")
print("Distance less than 0.4m")
print("last driving iteration linear")
print(distance)
#last movement iteration of Lio    
mobile_platform.move_platform_angular(angle, speed=0.07, blocking=True)
#mobile_platform.move_platform_linear(-distance, speed=0.07, blocking=True)
 
#docking finished


