#! /usr/bin/env python3

#from moveit_commander import robot
import rospy
import moveit_commander
from gazebo_msgs.msg import ModelStates
from control_msgs.msg import GripperCommandAction, GripperCommandGoal
import geometry_msgs.msg
from tf.transformations import quaternion_from_euler
from std_msgs.msg import Float32
import message_filters
import os

#color.pyからカメラ座標を受け取る
def search():
    global completed
    sub_x = message_filters.Subscriber("subscribed_image_color_x", Float32)
    sub_y = message_filters.Subscriber("subscribed_image_color_y", Float32)
    sub_n = message_filters.ApproximateTimeSynchronizer([sub_x, sub_y], 100, 0.1, allow_headerless=True)
    #一度受け取ったら適当に値を入れてget関数を動かす
    if completed:
        get(finished_x, finished_y)
    else:
        sub_n.registerCallback(get)

#受け取ったカメラ座標をアーム座標に変換してアプローチする
def get(topic_x, topic_y):
    global completed, arm, flag, finished_x, finished_y
    #global robot
    inversion = -1 #カメラが逆さに付いているので
    ratio_cm = 0.05 #[cm] あるカメラ座標の値のときのアーム座標のずれ
    ratio_px_x = -177 #[px] あるアーム座標の値の時のカメラ座標の値
    ratio_px_y = -180 #ratio_px_xと同じ
    #1回目は座標変換を行う
    if completed:
        pass
    else:
        print(topic_x.data, topic_y.data)
        #座標変換
        f_x = inversion * round((ratio_cm * topic_x.data) / ratio_px_x, 7)
        f_y = inversion * round((ratio_cm * topic_y.data) / ratio_px_y, 7)
    finished_x = topic_x.data
    finished_y = topic_y.data
    print(f_x, f_y)

    #座標変換をもとにアームを動かす
    if flag:
        #フラグ処理(一度だけ以下の処理を行う)
        completed = True
        flag = False
        setup(0.7, 0.18+f_y, 0.0+f_x, 0.13)#一気にアプローチしない(安全対策)
        setup(0.7, 0.18+f_y, 0.0+f_x, 0.085)
        hand(0.16, 1.0) #掴む
        #batting.py起動
        os.popen("rosrun batting_robot batting.py ")

    print("done")


def main():
    global flag, gripper, arm, completed
    flag = True
    completed = False
    gripper = moveit_commander.MoveGroupCommander("gripper")
    arm = moveit_commander.MoveGroupCommander("arm")
    hand(1.0, 1.0) #search.pyが動いていることをわかりやすくするためハンドを大きく開く
    search() #カメラ座標取得

#アームを動かす関数
def setup(time, x, y, z):
    arm.set_max_velocity_scaling_factor(time)
    arm.set_max_acceleration_scaling_factor(1.0)

    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = x
    target_pose.position.y = y
    target_pose.position.z = z
    q = quaternion_from_euler(-3.14, 0.0, -3.14/2.0)  # 上方から掴みに行く場合
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]
    arm.set_pose_target(target_pose)  # 目標ポーズ設定
    arm.go()  # 実行

#ハンドを動かす関数
def hand(state, time):
    gripper.set_joint_value_target([state, time])
    gripper.go()

if __name__ == "__main__":
    rospy.init_node("grab")
    print("OK!!")
    main()
    rospy.spin()
