#! /usr/bin/env python3

import rospy
import sys, tty, termios, select
import actionlib
import moveit_commander
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import GripperCommandAction,GripperCommandGoal
from control_msgs.msg import FollowJointTrajectoryAction,FollowJointTrajectoryActionGoal
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
        goal = FollowJointTrajectoryActionGoal()
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

    #引っ張り方向の動き
    def go_pull(self):
        global joint_values

    #流し方向の動き
    def go_sink(self):
        global joint_values

# 1文字のキーボード入力を返す関数
def getch(timeout):
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        (result_stdin, w, x) = select.select([sys.stdin], [], [], timeout)
        if len(result_stdin):
            return result_stdin[0].read(1)
        else:
            return False

        # return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)



def main():
    completed = False
    do_shutdown = False
    arm_swing = Swing()

    if completed:
        pass
    else:
        while do_shutdown is False:
        # 文字入力
            input_key = getch(0.1) # 一定時間入力がなければFalseを返す
            input_code = ""
            if input_key is not False:
                print(input_key)
                input_code = ord(input_key)

            if input_code == ord('c') or input_code == ord('C'):
                print("center")
                Swing.go_center()
                do_shutdown = True

            if input_code == ord('p') or input_code == ord('P'):
                print("pull")
                Swing.go_pull()
                do_shutdown = True

            if input_code == ord('s') or input_code == ord('S'):
                print("sink")
                Swing.go_sink()
                do_shutdown = True



if __name__ == '__main__':
    rospy.init_node("swing")
    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptExeption:
        pass