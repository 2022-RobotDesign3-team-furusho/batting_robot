#! /usr/bin/python3

import rospy
import sys
import actionlib
import math
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import GripperCommandAction,GripperCommandGoal
from control_msgs.msg import FollowJointTrajectoryAction,FollowJointTrajectoryGoal
import input_blue
import time

class Swing(object):

    def __init__(self):
        self._client = actionlib.SimpleActionClient("/crane_x7/arm_controller/follow_joint_trajectory", FollowJointTrajectoryAction)

        rospy.sleep(0.1)
        if not self._client.wait_for_server(rospy.Duration(secs=5)):
            rospy.logerr("Action Server Not Found")
            rospy.signal_shutdown("Action Server Not Found")
            sys.exit(1)

        self.gripper_client = actionlib.SimpleActionClient("/crane_x7/gripper_controller/gripper_cmd",GripperCommandAction)
        self.gripper_goal = GripperCommandGoal()
        self.gripper_client.wait_for_server(rospy.Duration(5.0))

        if not self.gripper_client.wait_for_server(rospy.Duration(5.0)):
            rospy.logerr("Exiting - Gripper Action Server Not Found.")
            rospy.signal_shutdown("Action Server not found.")
            sys.exit(1)
    
    def setup(self):
        global point
        global goal
        point = JointTrajectoryPoint()
        goal = FollowJointTrajectoryGoal()
        goal.trajectory.joint_names = ["crane_x7_shoulder_fixed_part_pan_joint","crane_x7_shoulder_revolute_part_tilt_joint","crane_x7_upper_arm_revolute_part_twist_joint","crane_x7_upper_arm_revolute_part_rotate_joint","crane_x7_lower_arm_fixed_part_joint","crane_x7_lower_arm_revolute_part_joint","crane_x7_wrist_joint"]

    def setup2(self,secs2,time,sleep):
        for i, p in enumerate(joint_values):
            point.positions.append(p)
        
        point.time_from_start = rospy.Duration(secs = secs2)
        goal.trajectory.points.append(point)
        self._client.send_goal(goal)
        self._client.wait_for_result(timeout=rospy.Duration(time))
        self.gripper_client.send_goal(self.gripper_goal,feedback_cb=self.feedback)
        rospy.sleep(sleep)

    def setup3(self,secs2,time,sleep):
        for i, p in enumerate(joint_values):
            point.positions.append(p)
        
        point.time_from_start = rospy.Duration(secs = secs2)
        goal.trajectory.points.append(point)
        self._client.send_goal(goal)
        self.gripper_client.send_goal(self.gripper_goal,feedback_cb=self.feedback)
        rospy.sleep(sleep)

    #バット探索の動き
    def search_bat(self):

        global joint_values
        self.gripper_goal.command.position = math.radians(12.12)

        print("探索開始")
        self.setup()
        joint_values = [math.radians(90), math.radians(-10), 0.0, math.radians(-110), 0.0, math.radians(-59), math.radians(-90)] #角度指定部
        self.setup2(6.0, 100.0, 1)

        print("探索中")
        self.setup()
        joint_values = [math.radians(-90), math.radians(-10), 0.0, math.radians(-90), 0.0, math.radians(-80), math.radians(-90)] #角度指定部
        self.setup3(6.0, 100.0, 1)
        print("探索終了")

        #print("とまれええ")
        #time.sleep(2)
        #self._client.cancel_all_goals()


    def feedback(self,msg):
        print("feedback callback")

def main():
    completed = False
    arm_swing = Swing()

    if completed:
        pass
    else:
        arm_swing.search_bat()


if __name__ == '__main__':
    print("start")
    rospy.init_node("swing")
    main()
    rospy.spin()
