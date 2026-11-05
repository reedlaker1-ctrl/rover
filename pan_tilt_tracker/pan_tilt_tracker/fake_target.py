import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from std_msgs.msg import Bool


class FakeTarget(Node):
    def __init__(self):
        super().__init__('fake_target')

        # Two transmitters: (message type, topic name, queue size)
        self.target_pub = self.create_publisher(Point, '/target', 10)
        self.found_pub = self.create_publisher(Bool, '/target_found', 10)

        # Remember when we started, so we can compute elapsed time
        self.start_time = self.get_clock().now()

        # Call self.timer_callback every 1/30 of a second
        self.timer = self.create_timer(1.0 / 30.0, self.timer_callback)

    def timer_callback(self):
        # Seconds since the node started
        t = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

        target = Point()
        target.x = 0.8 * math.sin(2 * math.pi * 0.2 * t)
        target.y = .4 * math.sin(math.pi * 0.05 * t)
        target.z = 0.0

        found = Bool()
        found.data = True

        self.target_pub.publish(target)
        self.found_pub.publish(found)


def main(args=None):
    rclpy.init(args=args)
    node = FakeTarget()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()