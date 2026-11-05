import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Vector3
from std_msgs.msg import Bool


class PanTiltController(Node):
    def __init__(self):
        super().__init__('pan_tilt_controller')

        # Parameters: (name, default)
        self.declare_parameter('kp_pan', 1.0)         # rad/s per unit offset
        self.declare_parameter('kp_tilt', 1.0)
        self.declare_parameter('pan_limit', 3.14)     # generous clamp, rad
        self.declare_parameter('tilt_limit', 1.57)
        self.declare_parameter('target_timeout', 0.5) # seconds

        # State
        self.pan = 0.0
        self.tilt = 0.0
        self.target = Point()
        self.found = False
        self.last_target_time = None

        # Receivers: (type, topic, callback, queue size)
        self.create_subscription(Point, '/target', self.target_callback, 10)
        self.create_subscription(Bool, '/target_found', self.found_callback, 10)

        # Transmitter
        self.cmd_pub = self.create_publisher(Vector3, '/servo_cmd', 10)

        # Control loop
        self.dt = 1.0 / 30.0
        self.timer = self.create_timer(self.dt, self.control_loop)

    def target_callback(self, msg):
        self.target = msg
        self.last_target_time = self.get_clock().now()

    def found_callback(self, msg):
        self.found = msg.data

    def control_loop(self):
        # TODO: work out the age of the last target message, in seconds
        #       (if last_target_time is None, treat the target as stale)
        # TODO: if found is True and the target is not stale:
        #           update self.pan and self.tilt using the formulas above
        #           (read kp_pan, kp_tilt with get_parameter(...).value)
        # TODO: clamp self.pan and self.tilt to their limits
        target_age_s = self.last_target_time.nanoseconds / 1e9 if self.last_target_time is not None else None
        if self.found and target_age_s is not None:
            self.pan = self.pan + self.get_parameter('kp_pan').value * self.target.x * self.dt
            self.tilt = self.tilt + self.get_parameter('kp_tilt').value * self.target.y * self.dt
        if self.pan > self.get_parameter('pan_limit').value:
            self.pan = self.get_parameter('pan_limit').value
        elif self.pan < -self.get_parameter('pan_limit').value:
            self.pan = -self.get_parameter('pan_limit').value
        if self.tilt > self.get_parameter('tilt_limit').value:
            self.tilt = self.get_parameter('tilt_limit').value  
        elif self.tilt < -self.get_parameter('tilt_limit').value:
            self.tilt = -self.get_parameter('tilt_limit').value

        cmd = Vector3()
        cmd.x = self.pan
        cmd.y = self.tilt
        cmd.z = 0.0
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = PanTiltController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()