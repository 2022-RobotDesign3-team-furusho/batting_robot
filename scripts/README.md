# scripts

本パッケージは[rt-net/crane_x7_ros](https://github.com/rt-net/crane_x7_ros)を元に、未来ロボティクス学科で開講された講義内でチーム
2022-RobotDesign3-team-furushoが作成したものです

---

## 実装内容

### vision.py

```
$ rosrun batting_robot vision.py
```

RealSenseから受け取った青い画像をカメラ座標に変換するプログラムです。
青い物体の中点を水色の四角で描画し、カメラ座標として画面からどのくらいずれているかを x/y 座標をパブリッシュしています。


### ready.py

```
$ rosrun batting_robot ready.py
```

カメラを下に向けバットを拾うためのプログラムです。
角度制御を用いてロボットアームを起動しています。

---


### grab.py

```
$ rosrun batting_robot grab.py
```
カメラ座標をアーム座標に変換し、バットを掴むプログラムです。位置制御でアームを動かしています。
カメラ座標を取得するため `vision.py`が動いている必要があります。

---

### batting.py

```
$ rosrun batting_robot batting.py
```

キーボード入力を受けセンター方向、引張り方向、流し方向を指定しバッティングを行うプログラムです。
一度バッティングをした後も続けてバッティングすることが出来ます。
ready.pyと同様に角度制御を用いてロボットアームを動かしています。

```
[C]:センター方向の構えに移行
[P]:引っ張り方向の構えに移行
[S]:流し方向の構えに移行
[F]:バットを置きverticalの姿勢に移行
[S]:バッティング開始
```


---


### 使用・参考にしたコード一覧
|コード|コード引用元|著作権者|元のライセンス|
|:--:|:---:|:---:|:---:|
|[vision.py](https://github.com/2022-RobotDesign3-team-furusho/batting_robot/blob/feature/recognition/scripts/vision.py)|[color.py](https://github.com/2021-RobotDesign3-team2/crane_x7_ros_test/blob/main/scripts/color.py)|[2021-RobotDesign3-team2](https://github.com/2021-RobotDesign3-team2)|[LICENSE](https://github.com/2021-RobotDesign3-team2/crane_x7_ros_test/blob/main/LICENSE)|
|[ready.py](https://github.com/2022-RobotDesign3-team-furusho/batting_robot/blob/feature/recognition/scripts/ready.py)|[ready.py](https://github.com/2021-RobotDesign3-team2/crane_x7_ros_test/blob/main/scripts/ready.py)|[2021-RobotDesign3-team2](https://github.com/2021-RobotDesign3-team2)|[LICENSE](https://github.com/2021-RobotDesign3-team2/crane_x7_ros_test/blob/main/LICENSE)|
|[grab.py](https://github.com/2022-RobotDesign3-team-furusho/batting_robot/blob/feature/recognition/scripts/grab.py)|[serch.py](https://github.com/2021-RobotDesign3-team2/crane_x7_ros_test/blob/main/scripts/search.py)|[2021-RobotDesign3-team2](https://github.com/2021-RobotDesign3-team2)|[LICENSE](https://github.com/2021-RobotDesign3-team2/crane_x7_ros_test/blob/main/LICENSE)|
|[batting.py](https://github.com/2022-RobotDesign3-team-furusho/batting_robot/blob/feature/recognition/scripts/batting.py)|[nagi_uda.py](https://github.com/8group-robotdesign3/crane_x7_ros_modified_by_group8/blob/master/crane_x7_examples/scripts/nagi_uda.py)|[8group-robotdesign3](https://github.com/8group-robotdesign3)|[LICENSE](https://github.com/8group-robotdesign3/crane_x7_ros_modified_by_group8/blob/master/LICENSE)|

