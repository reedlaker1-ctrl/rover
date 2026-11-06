import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3


class ServoSim(Node):
    def __init__(self):
        super().__init__('servo_sim')

        self.declare_parameter('pan_limit', 1.57)   # rad
        self.declare_parameter('tilt_limit', 0.79)  # rad
        self.declare_parameter('max_rate', 2.0)    # rad/s


        # State
        self.pan = 0.0
        self.tilt = 0.0
        self.cmd = Vector3()

        self.create_subscription(Vector3, '/servo_cmd', self.cmd_callback, 10)
        self.state_pub = self.create_publisher(Vector3, '/servo_state', 10)

        self.dt = 1.0 / 30.0
        self.timer = self.create_timer(self.dt, self.update)

    def cmd_callback(self, msg):
        self.cmd = msg

    def clamp(self, value, low, high):
        return max(low, min(high, value))

    def update(self):
        max_rate = self.get_parameter('max_rate').value
        pan_limit = self.get_parameter('pan_limit').value
        tilt_limit = self.get_parameter('tilt_limit').value
        step_x = self.clamp(self.cmd.x - self.pan, -max_rate * self.dt, +max_rate * self.dt)
        step_y = self.clamp(self.cmd.y - self.tilt, -max_rate * self.dt, +max_rate * self.dt)
        self.pan = self.clamp(self.pan + step_x, -pan_limit, +pan_limit)
        self.tilt = self.clamp(self.tilt + step_y, -tilt_limit, +tilt_limit)
        state = Vector3()
        state.x = self.pan
        state.y = self.tilt
        state.z = 0.0
        self.state_pub.publish(state)


def main(args=None):
    rclpy.init(args=args)
    node = ServoSim()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()