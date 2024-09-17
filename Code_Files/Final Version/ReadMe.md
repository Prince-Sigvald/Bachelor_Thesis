## Creator:     Yan Gridling
## Date:        22.07.2024
## Version:     1.00

---------------------------------------------------------------------------------
This ReadMe file gives an overview of the files used
to dock on to a laundry cart which is equipped with an aruco marker.
All files can be found in this folder and were created by Yan Gridling.
A more detailed explanations can be found in the respective files.

Note: Error handling was only implemented to a very limited extent, 
as entire applications are implemented for specific cases in the field of F&P and 
therefore specific error handling is only applied to these applications.


---------------------------------------------------------------------------------
# File: dock_to_cart

### Description: 
Combines all important files to let Lio dock onto a laundry cart 
which equppied with an aruco marker.
The Docking process happens iterative, currently with three iterations.

### Note: 
This file serves only as an example usage and should present how the class, scripts and functions
interact with each other.


---------------------------------------------------------------------------------
# File: Class_Compute_Navigation_Docking

### Description: 
The class is needed to compute all important linear and angular navigation values for Lio
to dock to a laundry cart with an aruco marker.
The computed values are stored as members of the class.

### Note: 
The class members from row 28 should not be changed, especially all the distance values were optimised
during the whole development process.
The exact mathematical composition of the formulas is documented in the bachelor's report.


---------------------------------------------------------------------------------
# File: functions_execute_docking_laundry_cart

### Description: 
The file contains all functions to execute the driving commands which were computed 
by the previously described class.

### Note: 
It is recommended to first have a look at Class_Compute_Navigation_Docking to understand
how the methods and members interact with eachother.


---------------------------------------------------------------------------------
# File: release_cart

### Description: 
The script lets Lio drive a certain distance back, then lifts the hook of the Add-On and then lets Lio drive forward again to release the cart.

---------------------------------------------------------------------------------
# File: check_pulling_force

### Description: 
This script is a parallel script and enables the 12V buck converter on the electric interface
to make the integrated push button of the Cart-Docking Add-On usable.
If the mechanis is pulled out to far, a overlap will push the push button and will interrupt the current 
movement of Lio and will also release the cart.

### Note: 
The shared variable in the script is only used for testing reasons.


---------------------------------------------------------------------------------
# File: test_movement_interruption_if_laundry_cart_jams

### Description: 
The script lets Lio drive two meters forward and lets the parallel script check_pulling_force run
to check if the movement interruption operates well

### Note: 
The shared variable guarantees, that the releasing routine can be finsihed in the parallel script

