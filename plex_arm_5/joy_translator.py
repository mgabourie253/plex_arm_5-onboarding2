import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import Joy


# Publishing to servo_node/delta_twist_cmds?
# Finished otherwise
class JoyTranslator(Node):
    def __init__(self):
        super().__init__('joy_translator')
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10)
        self.subscription  # Avoid non-existant variable errors

        self.publisher_ = self.create_publisher(TwistStamped, 'servo_node/delta_twist_cmds', 10)

    # Reference frame called 'base_link'? Found in plex_arm_5.urdf
    # get_logger formatting is yuck, Published output missing 
        # (if msg_out timestamp is different than msg_in timestamp then should be included)
    def joy_callback(self, msg_in):
        timestamp_in = msg_in.header.stamp
        stick_values = msg_in.axes  # Values between -1.0 and 1.0
        leftx = stick_values[0]
        lefty = stick_values[1]
        righty = stick_values[3]
        button_values = msg_in.buttons  # Unused
        stick_scaling = 1  # Max velocity 1m/s from config/pilz_cartesian_limits.yaml

        msg_out = TwistStamped()
        msg_out.header.stamp = timestamp_in
        msg_out.header.frame_id = 'base_link'  # Found in plex_arm_5.urdf
        msg_out.twist.linear.x = stick_scaling * leftx
        msg_out.twist.linear.y = stick_scaling * lefty
        msg_out.twist.linear.z = stick_scaling * righty

        self.publisher_.publish(msg_out)

        self.get_logger().info(
            '\nReceived:'+
            '\n   Timestamp: %s.%ss' % (timestamp_in.sec, timestamp_in.nanosec)+
            '\n   Left stick:'+
            '\n      x: %s' % leftx+
            '\n      y: %s' % lefty+
            '\n   Right stick:'+
            '\n      y: %s' % righty+
            '\nPublished TwistStamped message.'
            )

def main(args=None):
    rclpy.init(args=args)

    joy_translator = JoyTranslator()

    try:
        rclpy.spin(joy_translator)
    except KeyboardInterrupt:
        pass
    finally:
        joy_translator.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()