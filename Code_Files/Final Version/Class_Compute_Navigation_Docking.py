#Creator:     Yan Gridling
#Date:        26.06.2024
#Version:     1.00
#Description: Class to compute every value to determine linear and angular driving values of Lio
#             in terms of certain aruco code ID

#Libraries
import numpy as np

class Compute_Navigation_Docking:
    """
    Class needs to integer values for initialisation, 
    first the specific aruco id to dock on,
    second the corresponding size of the markter in cm 
    (currently 5cm but this size will be adapted if the cart is further away)
    """
    def __init__(self, Aruco_ID, Aruco_Size):
        #Aruco Values
        self.Aruco_ID = Aruco_ID
        self.Aruco_Size = Aruco_Size #in cm
        #Position values robot to aruco code
        self.pose_arm_aruco_xyz=None
        self.pose_arm_aruco_euler_y=None#Turn angle of vertical axis of aruco marker to camera
        #Movement values robot to aruco code
        self.drive_distance_linear=None
        self.turn_angle=None
        
        #Fix Class Variables for further usage of myP functions
        self.camera_name="LioGripper"#used camera of Lio
        self.robot_arm_name="Lio"    #used robot arm
        self.distance_offset_y=710 #Linear distance from Hook to rotational point of robot
        self.distance_offet_y_base=200 #Linear distance offset of armbase to rotational point of robot
        self.deg_offset=0
        self.rectangular_distance_to_aruco_new_alignment=1100# This value determines the distance rectengular from the aruco code to a new starting position of the robot
        
    def compute_pose_arm_to_aruco_code(self):
        """
        Detects Aruco Marker, if marker was found the relativ x,y,z cordinatinon form the robot base to the 
        marker will be computed and stored in the class attributes
        else the routine will be ended early
    
        Parameters:
        -
    
        Return:
        1 if routine succeded, 0 if no marker was detected
        """
        #Get transformation from aruco code to gripper
        aruco_transform_arm=service_robot.get_aruco_transform(self.camera_name, self.Aruco_Size, self.Aruco_ID, timeout=1.0)
        #Errror Handling: if no aruco code was detected the function interrupts
        if (aruco_transform_arm == None):
            print("No Aruco Code found")
            voice.say("Ich habe momentan keine Sicht auf einen Aruco Marker")
            return 0
            
        #Transform into Working frame hence Base Frame
        pose_aruco_base=service_robot.cam_object_to_working_frame(aruco_transform_arm, self.camera_name, self.robot_arm_name, working_frame='base', O_r_Oo=None)
        
        #Get linear values from robot to aruco
        self.pose_arm_aruco_xyz = [pose_aruco_base._Transform__translation.x,
            pose_aruco_base._Transform__translation.y,
            pose_aruco_base._Transform__translation.z]
        
        #Get rotational of aruco code to robot
        euler=pose_aruco_base._Transform__orientation.to_euler()
        self.pose_arm_aruco_euler_y=euler[1]
        return 1


    def compute_navigation_values(self):
        """
        Computes linear and rotational navigation values from relativ x,y,z position and vertical rotation anlge 
        of marker to robot base.
        Computed values will be saved in attributes of class
    
        Parameters:
        -
    
        Return:
        No return value
        """
        #computes navigation values in terms of pose to aruco code
        self.drive_distance_linear=(np.sqrt(self.pose_arm_aruco_xyz[0]**2+self.pose_arm_aruco_xyz[1]**2)-self.distance_offset_y)/1000   #in meters
        self.turn_angle=np.rad2deg(np.arctan2(-self.pose_arm_aruco_xyz[0],self.pose_arm_aruco_xyz[1]))

    def compute_starting_navigation(self):
        """
        This method is needed, if the angle from Lio to the aruco marker is to steep to dock on
        The computed navigation values are for a point rectangular in front of the marker with a distance 
        stored in self.rectangular_distance_to_aruco_new_alignment
        Computed values will be saved in attributes of class
        
        Parameters:
        -
    
        Return:
        No return value
        """
        angle_aruco_code_rad=np.deg2rad(self.pose_arm_aruco_euler_y)
        starting_pos_x=self.pose_arm_aruco_xyz[0]+np.sin(angle_aruco_code_rad)*self.rectangular_distance_to_aruco_new_alignment
        starting_pos_y=self.pose_arm_aruco_xyz[1]-np.cos(angle_aruco_code_rad)*self.rectangular_distance_to_aruco_new_alignment

        self.drive_distance_linear=(np.sqrt(starting_pos_x**2+starting_pos_y**2)-self.distance_offet_y_base)/1000   #in meters
        self.turn_angle=np.rad2deg(np.arctan2(-starting_pos_x, starting_pos_y))
