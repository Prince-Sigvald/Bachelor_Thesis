#Creator:     Yan Gridling
#Date:        26.06.2024
#Version:     1.00
#Description: Class to compute every value to determine linear and angular values 
#             in terms of certain aruco code ID

#Libraries
import numpy as np

class Compute_Navigation_Docking:
    #Initialisation of Class
    def __init__(self, Aruco_ID, Aruco_Size):
        self.Aruco_ID = Aruco_ID
        self.Aruco_Size = Aruco_Size
        #Position values robot to aruco code
        self.pose_arm_aruco_xyz=None
        self.pose_arm_aruco_euler_y=None
        #Movement values robot to aruco code
        self.drive_distance_linear=None
        self.turn_angle=None
        
        # Fix Class Variables for further usage of myP functions
        self.camera_name="LioGripper"
        self.robot_arm_name="Lio"
        self.distance_offset_y=710 #Linear distance from Hook to rotational point of robot
        self.distance_offet_y_base=200 #Linear distance offset for armbase to rotational point of robot
        self.deg_offset=0
        self.distance_offset_starting_navigation=1100# This value determines the distance rectengular from the aruco code to a new starting position of the robot
        
    def compute_pose_arm_to_aruco_code(self):
        #Get transformation from aruco code to gripper
        aruco_transform_arm=service_robot.get_aruco_transform(self.camera_name, self.Aruco_Size, self.Aruco_ID, timeout=1.0)
        
        #Transform into Working frame hence Base Frame
        pose_aruco_base=service_robot.cam_object_to_working_frame(aruco_transform_arm, self.camera_name, self.robot_arm_name, working_frame='base', O_r_Oo=None)
        
        #Get linear values from robot to aruco
        self.pose_arm_aruco_xyz = [pose_aruco_base._Transform__translation.x,
            pose_aruco_base._Transform__translation.y,
            pose_aruco_base._Transform__translation.z]
        
        #Get rotational of aruco code to robot
        euler=pose_aruco_base._Transform__orientation.to_euler()
        self.pose_arm_aruco_euler_y=euler[1]


    def compute_navigation_values(self):
        #cpmputes navigation values in terms of pose to aruco code
        self.drive_distance_linear=(np.sqrt(self.pose_arm_aruco_xyz[0]**2+self.pose_arm_aruco_xyz[1]**2)-self.distance_offset_y)/1000   #in meters
        self.turn_angle=np.rad2deg(np.arctan2(-self.pose_arm_aruco_xyz[0],self.pose_arm_aruco_xyz[1]))
    
    #The following function aligns Lio new, if the aruco code is to far twisted away from lio
    def compute_starting_navigation(self):
        angle_aruco_code_rad=np.deg2rad(self.pose_arm_aruco_euler_y)
        starting_pos_x=self.pose_arm_aruco_xyz[0]+np.sin(angle_aruco_code_rad)*self.distance_offset_starting_navigation
        starting_pos_y=self.pose_arm_aruco_xyz[1]-np.cos(angle_aruco_code_rad)*self.distance_offset_starting_navigation

        self.drive_distance_linear=(np.sqrt(starting_pos_x**2+starting_pos_y**2)-self.distance_offet_y_base)/1000   #in meters
        self.turn_angle=np.rad2deg(np.arctan2(-starting_pos_x, starting_pos_y))
