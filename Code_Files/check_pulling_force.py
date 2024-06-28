#Creator:     Yan Gridling
#Date:        28.06.2024
#Version:     1.00
#Description: This script checks if the pulling force of the cart docking mechnism is to big
#             and interrupts the current movement


#Switch on the 12V buck converter to read out the push buttons
#write_digital_tool_io(7, 1)
{"action": "write_digital_tool_io",
"bridge": "core",
"arguments": {"identifiers": 3, "values": true}}


#as long the the push button of the slider is not pushed, the movement can continue
while(read_digital_main_io(1)):
    wait(0.1)

#interrupt movement and release cart
mobile_platform.cancel_navigation_goal()
print("Current movement interrupted, cart jammed somewhere!")