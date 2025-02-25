from pymycobot import ElephantRobot
import time

# Change the IP address to the real IP address of the P630 Raspberry Pi
# Please ensure that the gripper is in the open state before using the code.
# If you are currently switching from IO mode to passthrough mode,
# you need to execute the code twice. That is, you need to execute this code once, then restart and execute it again.

elephant_client = ElephantRobot("192.168.1.31", 5001,debug=True)

# Necessary commands to start the robot
elephant_client.start_client()
time.sleep(1)

print(elephant_client.get_angles())
# elephant_client.set_gripper_mode(0)
# time.sleep(1)
# elephant_client.set_gripper_calibrate()
# time.sleep(1)
