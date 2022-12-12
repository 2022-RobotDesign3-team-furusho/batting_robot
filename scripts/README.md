# scripts

本パッケージは<a href= "https://github.com/rt-net/crane_x7_ros.html" >rt-net/crane_x7_ros</a    >を元に、未来ロボティクス学科で開講された講義内でチーム
2022-RobotDesign3-team-furushoが作成したものです

---

## 実装内容

### ready.py

```
$ rosrun batting_robot ready.py
```

カメラを下に向けバットを拾うためのプログラムです。
角度制御を用いてロボットアームを起動しています。

---

### batting.py

```
$ rosrun batting_robot batting.py
```

センター方向、引張り方向、流し方向を指定しバッティングを行うプログラムです。
ready.pyと同様に角度制御を用いてロボットアームを動かしています。

---

### 使用・参考にしたコード一覧
|コード|コード引用元|著作権者|元のライセンス|
|:--:|:---:|:---:|:---:|

