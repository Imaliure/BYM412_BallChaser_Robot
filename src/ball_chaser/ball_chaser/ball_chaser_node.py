#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge


class BallChaser(Node):
    def __init__(self):
        super().__init__('ball_chaser')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Image, '/camera_sensor/image_raw', self.image_callback, 10)
        self.bridge = CvBridge()
        self.get_logger().info("✅ Ball Chaser başlatıldı")

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f"CV Bridge hatası: {e}")
            return

        # Görüntüyü HSV renk uzayına çevir
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # Beyaz topu tespit etmek için renk aralığı
        lower_white = (0, 0, 50)
        upper_white = (180, 120, 255)

        # Maskeyi oluştur
        mask = cv2.inRange(hsv, lower_white, upper_white)
        M = cv2.moments(mask)

        move_cmd = Twist()

        # Top algılandıysa
        if M['m00'] > 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            error_x = cx - msg.width / 2

            # Hata merkezlenmemişse dön
            if abs(error_x) > 30:
                move_cmd.angular.z = -float(error_x) / 200.0
            else:
                move_cmd.linear.x = 0.2

            self.publisher_.publish(move_cmd)
            self.get_logger().info(f"🎯 Top görüldü: {cx}, {cy}")
        else:
            # Top görünmüyorsa dur
            self.get_logger().info("❌ Top görünmüyor — durduruluyor")
            self.publisher_.publish(Twist())


def main(args=None):
    rclpy.init(args=args)
    node = BallChaser()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

