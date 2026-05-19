#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped

class OdomToPath(Node):
    def __init__(self):
        super().__init__('odom_to_path')
        self.path = Path()
        self.path.header.frame_id = 'odom'
        self.sub = self.create_subscription(Odometry, '/odom', self.callback, 10)
        self.pub = self.create_publisher(Path, '/path', 10)

    def callback(self, msg):
        pose = PoseStamped()
        pose.header = msg.header
        pose.pose = msg.pose.pose
        self.path.poses.append(pose)
        self.path.header.stamp = msg.header.stamp
        self.pub.publish(self.path)

def main():
    rclpy.init()
    node = OdomToPath()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
