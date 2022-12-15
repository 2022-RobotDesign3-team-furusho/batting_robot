#! /usr/bin/env python3

import rospy
import numpy as np
import cv2
from std_msgs.msg import Float32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

#RealSenseから色画像を取得して目標のローカル座標を出力するクラス
class ImageConvert(object):
    def __init__(self):
        self.bridge = CvBridge()
        self.subscribed_image_color = rospy.Subscriber("/camera/color/image_raw", Image, self.color_callback_and_convert)
        self.publisher_hsv_image_x = rospy.Publisher("subscribed_image_color_x", Float32, queue_size=10)
        self.publisher_hsv_image_y = rospy.Publisher("subscribed_image_color_y", Float32, queue_size=10)

    def main(self):
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("error")
            cv2.destroyAllWindows()
    
    def color_callback_and_convert(self, topic):
        global x, y, flag
        try:
            cv_image_color = self.bridge.imgmsg_to_cv2(topic, "bgr8")
        except CvBridgeError as e:
            print(e)
        
        #RGB色空間からhsv色空間に変換
        hsv_image = cv2.cvtColor(cv_image_color, cv2.COLOR_BGR2HSV)

        #hsv色空間内で設定した色を抽出
        bule_min = np.array([90, 60, 0]) #青色のしきい値
        bule_max = np.array([150, 255, 255]) #青色のしきい値
        bat_mask = cv2.inRange(hsv_image, bule_min, bule_max)

        #hsv色空間内で設定した色ｎイメージを抽出
        cv_image_2 = cv2.bitwise_and(cv_image_color, cv_image_color, mask = bat_mask)

        #グレースケールに変換(後述の処理に必要)
        gray_image = cv2.cvtColor(cv_image_2, cv2.COLOR_BGR2GRAY)

        #画像の二値化(しきい値処理)
        ret, thresh = cv2.threshold(gray_image, 125, 255, cv2.THRESH_OTSU)

        #二値化した画像の白の領域を囲む輪郭を取得
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #3000以下面積を囲まない
        contours = list(filter(lambda x: cv2.contourArea(x) > 3000, contours))

        #hsv_imageに輪郭を描画(赤色)
        cv2.drawContours(hsv_image, contours, -1, color=(0, 0, 255), thickness=6)

        #抽出した輪郭の重心を取得
        coordinates = cv2.moments(contours[0])
        x = int(coordinates["m10"]/coordinates["m00"])
        y = int(coordinates["m01"]/coordinates["m00"])

        #hsv_imageに重心を描画(水色)
        cv2.rectangle(hsv_image, (x + 10, y + 10), (x -10, y - 10), (255, 255, 0), thickness = 6)

        px_x = 640 / 2 #色画像のx座標の中心点
        px_y = 480 / 2 #色画像のy座標の中心点
        error_px_x = 70 #RealSenseの中心からのカメラズレ
        error_px_y = 90 #手前方向にフライパンがあった時にきれいにアプローチできるようにする
        neo_x = x - px_x - error_px_x #xローカル座標
        neo_y = y - px_y #yカメラ座標
        print("move_x:", neo_x, "move_y:", neo_y)

        #カメラ座標の誤差修正
        if neo_x < 0:
            self.publisher_hsv_image_x.publish(neo_x)
        elif neo_y > 75:
            self.publisher_hsv_image_y.publish(neo_y - error_px_y)
        else:
            self.publisher_hsv_image_y.publish(neo_y)

        if neo_x > 0:
            self.publisher_hsv_image_x.publish(neo_x)
        elif neo_y > 75:
            self.publisher_hsv_image_y.publish(neo_y - error_px_y)
        else:
            self.publisher_hsv_image_y.publish(neo_y)

        self.show(cv_image_color, hsv_image)

    #画像を表示する
    def show(self, image, hsv_image):
        cv2.imshow("image", image)
        cv2.imshow("image2", hsv_image)
        cv2.waitKey(3)

if __name__ == "__main__":
    global flag
    flag = True
    rospy.init_node("vision")
    image_convert = ImageConvert() #インスタンス化(色画像取得)
    image_convert.main()
    rospy.spin()
