#Creator:     Yan Gridling
#Date:        26.06.2024
#Version:     1.00
#Description: Release the cart

def release_cart(distance_drive_back):
    """
    Lets Lio drive backwards a certain distance and enables certain GPIO's to lift up the hook
    of the cart docking Add-On to release the cart

    Parameters:
    distance_drive_back: linear driving distance in meters (must be negativ to drive back)

    Return:
    No return value
    """
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

release_cart(-0.05)#Testing of function