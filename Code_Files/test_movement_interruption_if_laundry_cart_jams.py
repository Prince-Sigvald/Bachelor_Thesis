#Creator:     Yan Gridling
#Date:        28.06.2024
#Version:     1.00
#Description: This script lets Lio move a certein trajectory and lets the parallel script "check_pulling_force" run
#             to guarantee the movement interruption if the pulling force is to high

#starting of parallel script
start_parallel_script("check_pulling_force")

mobile_platform.move_platform_linear(2, speed=0.07, blocking=True)