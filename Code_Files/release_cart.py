#Creator:     Yan Gridling
#Date:        26.06.2024
#Version:     1.00
#Description: Release the cart

def release_cart(distance_drive_back):
    #Switch on 5V Buck and move hook
    write_digital_outputs([True], [5])
    write_digital_outputs([True], [1])
    #Drive Back
    mobile_platform.move_platform_linear(distance_drive_back, speed=0.07, blocking=True)
    #Drive forward
    mobile_platform.move_platform_linear(0.15, speed=0.07, blocking=True)
    #Switch everything off and end driving routine
    write_digital_outputs([False], [5])
    write_digital_outputs([False], [1])
    write_digital_outputs([False], [7])
    print("Cart released")

release_cart(-0.05)