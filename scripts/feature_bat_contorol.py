#! /usr/bin/env python3

import rospy
import sys
import actionlib
import math
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import GripperCommandAction,GripperCommandGoal
from control_msgs.msg import FollowJointTrajectoryAction,FollowJointTrajectoryGoal
#from moveit_msgs.msg import GetCartesianPath

class Swing(object):
    #コンストラクタ
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

    #センター方向の動き
    def go_center(self):
        global joint_values
    
        print("GO!!")

        self.gripper_goal.command.position = math.radians(12.12)

        print("構え")
        self.setup()
        joint_values = [0.0, math.radians(-10), 0.0, math.radians(-110), 0.0, math.radians(-59), math.radians(-90)] #角度指定部
        self.setup2(3.0, 100.0, 1)

        print("スイング")
        self.setup()
        joint_values = [1.0, math.radians(-10), 0.0, math.radians(-110), 0.0, math.radians(-59), math.radians(-90)] #角度指定部
        self.setup2(0.7, 100.0, 0.5)

        self.setup()
        joint_values = [-1.0, math.radians(-10), 0.0, math.radians(-110), 0.0, math.radians(-59), math.radians(-90)] #角度指定部
        self.setup2(0.7, 100.0, 1)


        self.setup()
        joint_values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] #角度指定部
        self.setup2(3.0, 100.0, 1)

        return self._client.get_result()

    #引っ張り方向の動き
    def go_pull(self):
        global joint_values

        print("GO!!")

        self.gripper_goal.command.position = math.radians(12.12)

        print("構え")
        self.setup()
        joint_values = [math.radians(5), math.radians(-10), 0.0, math.radians(-110), 0.0, math.radians(-59), math.radians(-70)] #角度指定部
        self.setup2(3.0, 100.0, 1)

        print("スイング")
        self.setup()
        joint_values = [1.0, math.radians(-10), 0.0, math.radians(-110), 0.0, math.radians(-59), math.radians(-70)] #角度指定部
        self.setup2(0.7, 100.0, 0.5)

        self.setup()
        joint_values = [-1.0, math.radians(-10), 0.0, math.radians(-110), 0.0, math.radians(-59), math.radians(-70)] #角度指定部
        self.setup2(0.7, 100.0, 1)


        self.setup()
        joint_values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] #角度指定部
        self.setup2(3.0, 100.0, 1)

        return self._client.get_result()

    #流し方向の動き
    def go_sink(self):
        global joint_values

        print("GO!!")

        self.gripper_goal.command.position = math.radians(12.12)

        print("構え")
        self.setup()
        joint_values = [math.radians(-5), math.radians(-10), 0.0, math.radians(-110), 0.0, math.radians(-59), math.radians(-110)] #角度指定部
        self.setup2(3.0, 100.0, 1)

        print("スイング")
        self.setup()
        joint_values = [1.0, math.radians(-10), 0.0, math.radians(-110), 0.0, math.radians(-59), math.radians(-110)] #角度指定部
        self.setup2(0.7, 100.0, 0.5)

        self.setup()
        joint_values = [-1.0, math.radians(-10), 0.0, math.radians(-110), 0.0, math.radians(-59), math.radians(-110)] #角度指定部
        self.setup2(0.7, 100.0, 1)


        self.setup()
        joint_values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] #角度指定部
        self.setup2(3.0, 100.0, 1)

        return self._client.get_result()

    def feedback(self,msg):
        print("feedback callback")

def main():
    completed = False
    arm_swing = Swing()

    if completed:
        pass
    else:
        print("[c]: センター返し, [p]: 引っ張り, [s]:流し打ち")
        # 文字入力
        input_key = input() # 一定時間入力がなければFalseを返す

        if input_key == 'c':
            print("center")
            arm_swing.go_center()

        if input_key == 'p':
            print("pull")
            arm_swing.go_pull()

        if input_key == 's':
            print("sink")
            arm_swing.go_sink()


if __name__ == '__main__':
    print("start")
    rospy.init_node("swing")
    main()
