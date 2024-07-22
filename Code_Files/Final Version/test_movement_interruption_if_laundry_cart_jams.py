#Creator:     Yan Gridling
#Date:        28.06.2024
#Version:     1.00
#Description: This script lets Lio move in a straight line and lets the parallel script "check_pulling_force" run
#             to guarantee the movement interruption if the pulling force is to high

set_shared_variable("finished", 0)
#starting of parallel script
start_parallel_script("Bachelorthesis_Yan/check_pulling_force")

#Let Lio move 2 meters
mobile_platform.move_platform_linear(2, speed=0.07, blocking=True)

#Waits until the shared variable is True to gruarantee that the releasing process of 
#the parallel script can be finished
while((get_shared_variable("finished")==0)):
    wait(0.2)

print("Testing Routine finished and cart released")