# batting_robot

2022年度設計製作論3
本リポジトリはcrane_x7でバッティングをするROS1パッケージです。
本パッケージは[rt-net/crane_x7_ros](https://github.com/rt-net/crane_x7_ros)を元に、未来ロボティクス学科で開講された講義内でのチーム
2022-RobotDesign3-team-furushoが作成したものになります。

---

## 動作確認済み環境
  * OS: Ubuntu 20.04.5LTS
  * ROS: Noetic Ninjemys
  * Intel RealSense SDK 2.0
  * OpenCV 4.5.1

---

## セットアップ方法

* OpenCVのインストール
```
$ wget --no-check-certificate https://raw.githubusercontent.com/milq/milq/master/scripts/bash/install-opencv.sh
$ chmod +x install-opencv.sh
$ ./install-opencv.sh
```

* 本パッケージのインストール
```
$ cd ~/catkin_ws/src
$ git clone https://github.com/2022-RobotDesign3-team-furusho/batting_robot
```

* 株式会社アールティ様から配布されている crane_x7_ros をダウンロード
```
cd ~/catkin_ws/src
git clone https://github.com/rt-net/crane_x7_ros.git
```

* ビルド
```
$ cd ~/catkin_ws
$ catkin_make
```

---

## 実行方法（実機のみ）

### バットの配置

安全なバッティングを行うため以下のバットを以下の配置に置いて下さい。

<img src = "https://user-images.githubusercontent.com/85381022/208228201-0811efe5-6967-4446-a335-874f53e00f22.png" width = "40%">

### RealSenseの取り付け方法

RealSenseは以下のように取り付けます。

<img src = "https://user-images.githubusercontent.com/85381022/208228303-b1115b70-8dcb-4ab6-838f-cd98910c7edb.jpg" width = "30%">


1. PCにUSBを接続し、/dev/ttyUSB0へのアクセス
```
$ sudo chmod 666 /dev/ttyUSB0
```

2. crane_x7を起動
```
$ roslaunch crane_x7_bringup demo.launch fake_execution:=false
```

3. RealSenseを立ち上げる
```
$ roslaunch realsense2_camera rs_camera.launch
```

4. 本パッケージの以下の２つのコードを順に実行する
```
$ rosrun batting_robot vision.py
$ rosrun batting_robot ready.py
```

5. バットを掴んだ後キーボード入力から打ち方が決まる、バッティング後は`F`を入力するまでバッティングを続けられる
```
[C]:センター方向
[P]:引っ張り方向
[S]:流し方向
[F]:バットを置きverticalの姿勢に移行
```


---

## ライセンス

本リポジトリは株式会社アールティ様のライセンスに則って作成しています。本リポジトリのデータ等に関するライセンスは、[LICENSE](https://github.com/2022-RobotDesign3-team-furusho/batting_robot/blob/main/LICENSE)をご参照下さい。

