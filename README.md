# batting_robot

2022年度設計製作論3
本リポジトリはcrane_x7でバッティングをするROS1パッケージです。
本パッケージは[crane_x7](https://rt-net.jp/products/crane-x7/)を元に、未来ロボティクス学科で開講された講義内でのチーム
2022-RobotDesign3-team-furushoが作成したものになります。

---

## 動作確認済み環境
  * OS: Ubuntu 20.04.5LTS
  * ROS: Noetic Ninjemys

---

## 環境構築

ROS1のインストール
```
$ git clone https://github.com/ryuichiueda/ros_setup_scripts_Ubuntu20.04_desktop.git
$ cd ros_setup_scripts_Ubuntu20.04_desktop/
$ sudo apt update
$ sudo apt upgrade
$ ./locale.ja.bash
$ ./step0.bash
$ ./step1.bash
```

動作確認
```
$ source ~/.bashrc
$ roscore
```

ワークスペースを作成し~/.bashrcを編集
```
$ cd
$ mkdir -p catkin_ws/src
$ cd catkin_ws/src
$ catkin_init_workspace
Creating symlink "/home/ueda/catkin_ws/...
$ cd ..
$ catkin_make
$ vim ~/.bashrc
...
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash       #この行を追加
export ROS_MASTER_URI=http://localhost:11311
...
$ source ~/.bashrc
$ cd ~/catkin_ws/
$ catkin_make
```

CRANE-X7のROS1パッケージのインストール
```
$ cd ~/catkin_ws/src
$ git clone https://github.com/rt-net/crane_x7_ros.git
$ git clone https://github.com/rt-net/crane_x7_description.git
$ git clone https://github.com/roboticsgroup/roboticsgroup_gazebo_plugins.git
$ rosdep install -r -y --from-paths --ignore-src crane_x7_ros
$ cd ~/catkin_ws/ 
$ catkin_make
```

RVIZの動作確認
```
$ source ~/.bashrc
$ roscore &
$ rviz
```

GAZEBOの動作確認
```
$ mkdir ~/.ignition/fuel
$ vi config.yaml
config.yamlに以下を追加
servers:
-
  name: osrf
  url: https://api.ignitionrobotics.org
$ roslaunch crane_x7_gazebo crane_x7_with_table.launch
```

本パッケージのインストール
```
$ cd ~/catkin_ws/src
$ git clone https://github.com/2022-RobotDesign3-team-furusho/batting_robot
$ cd ~/catkin_ws
$ catkin_make
```

---

## 実行方法（実機のみ）

PCにUSBを接続し、/dev/ttyUSB0へのアクセス
```
$ sudo chmod 666 /dev/ttyUSB0
```

crane_x7を起動
```
$ roslaunch crane_x7_bringup demo.launch fake_execution:=false
```

---

## ライセンス

本リポジトリは株式会社アールティ様のライセンスに則って作成しています。本リポジトリのデータ等に関するライセンスは、[LICENSE](https://rt-net.jp/products/crane-x7/)をご参照下さい。

