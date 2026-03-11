import rclpy
from rclpy.node import Node
from tf_transformations import quaternion_about_axis
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from math import sin, cos, pi
import serial

class PicoInterface(Node):
    def __init__(self):
        super().__init__(node_name="pico_interface", namespace="homer")
        # Create serial communication to Pico
        self.pico_msngr = serial.Serial(
            "/dev/ttyACM0",
            115200,
            timeout=0.01,
        )  # for UART, use ttyAMA0
        self.pico_comm_timer = self.create_timer(0.0133, self.process_pico_message)  # 75 Hz
        # Create target velocity subscriber
        self.cmd_vel_listner = self.create_subscription(
            topic="cmd_vel",
            msg_type=Twist,
            callback=self.set_targ_vels,
            qos_profile=1,
        )
        # variables
        data_keys = ["enc_lin_vel", "enc_ang_vel", "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z"]
        self.motion_data = {key: 0.0 for key in data_keys}
        self.targ_lin_vel = 0.0  # target linear velocity
        self.targ_ang_vel = 0.0  # target angular velocity
        # constants
        self.get_logger().info("HomeR's motion controller is up.")

    def process_pico_message(self):
        msg_to_pico = f"{self.targ_lin_vel:.3f},{self.targ_ang_vel:.3f}\n"
        self.pico_msngr.write(msg_to_pico.encode("utf-8"))
        if self.pico_msngr.inWaiting() > 0:
            msg_from_pico = self.pico_msngr.readline().decode("utf-8", "ignore").strip()
            if msg_from_pico:
                data_strings = msg_from_pico.split(",")
                if len(data_strings) == 8:
                    try:
                        # motion_data_float = list(map(float, motion_data_str))
                        # self.enc_lin_vel = motion_data_float[0]
                        # self.enc_ang_vel = motion_data_float[1]
                        # self.accel_x = motion_data_float[2]
                        # self.accel_y = motion_data_float[3]
                        # self.accel_z = motion_data_float[4]
                        # self.gyro_x = motion_data_float[5]
                        # self.gyro_y = motion_data_float[6]
                        # self.gyro_z = motion_data_float[7]
                        self.motion_data.update(
                            zip(
                                self.motion_data.keys(),
                                map(float, data_strings),  # convert all str in list to float
                            )
                        )
                    except ValueError:
                        pass
        self.get_logger().info(
            f"Motion data:\n---\n{self.motion_data}"
        )  # debug

    def set_targ_vels(self, msg):
        targ_lin_vel = msg.linear.x
        targ_ang_vel = msg.angular.z
        self.pico_msngr.write(f"{targ_lin_vel:.3f},{targ_ang_vel:.3f}\n".encode("utf-8"))
        self.get_logger().debug(
            f"Set target velocity\nlinear: {targ_lin_vel}, angular: {targ_ang_vel}"
        )


def main(args=None):
    rclpy.init(args=args)
    pico_interface = PicoInterface()
    rclpy.spin(pico_interface)
    pico_interface.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

