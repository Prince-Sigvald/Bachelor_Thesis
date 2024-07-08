#Creator:     Yan Gridling
#Date:        28.06.2024
#Version:     1.00
#Description: This script checks if the pulling force of the cart docking mechnism is to big
#             and interrupts the current movement

from release_cart import release_cart
print("Parallel Script started")

#Switch on the 12V buck converter to read out the push buttons
write_digital_outputs([True], [7])


#as long the the push button of the slider is not pushed, the movement can continue
while(read_digital_inputs(1)==0):
    wait(0.1)

#interrupt movement and release cart
mobile_platform.cancel_navigation_goal()
wait(0.5)

release_cart(-0.08)

print("Current movement interrupted, cart jammed somewhere!")
set_shared_variable("finished", 1)