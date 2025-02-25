import time
from pymycobot import MyCobot280, MyCobot320

import serial
import RPi.GPIO as GPIO
# 使用此代码前请确保代码为直立状态
# Before using this code, please make sure the code is in an upright state.
#使用次脚本请注意必须使用pymycobot>=3.6.0 ，使用pip install pymycobot==3.6.8可以更新pymycobot版本库3.6.8代表了版本，具体版本信息可以去官网查看
# Please note that when using this script, pymycobot>=3.6.0 must be used. You can update the pymycobot version library by using pip install pymycobot==3.6.8. 3.6.8 represents the version. For specific version information, you can check the official website.
def list_serial_ports():
    available_ports = serial.tools.list_ports.comports()
    if available_ports:
        print("Available serial ports:")
        # Create a dictionary to hold ports and their corresponding numbers
        port_dict = {}
        for i, (port, desc, hwid) in enumerate(available_ports, 1):
            port_dict[i] = port  # Map the number to the actual port
            print(f"{i}: {port}: {desc} [{hwid}]")

        # Prompt user to select a port by number
        while True:
            try:
                selection = int(input("Select a port by number: "))
                if selection in port_dict:
                    return port_dict[selection]
                else:
                    print("Invalid selection, please choose a valid number.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        print("No available serial ports found.")
        return None


def initialize_cobot(model_number, port):
    if model_number == 1:
        return MyCobot280(port, 1000000)
    elif model_number == 2:
        return MyCobot320(port, 115200)
    else:
        raise ValueError("Invalid model number. Please select 1 for 280PI or 2 for 320PI.")


def perform_pump_test(model_number,cobot):
    print("Starting pump test (开始吸泵测试)...")
    if model_number == 1:
        #GND -> GND，5V -> 5V，G2 -> 21，G5 -> 2
        for i in range(10):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(20, GPIO.OUT)
            GPIO.setup(21, GPIO.OUT)

            GPIO.output(20, 1)
            time.sleep(0.05)
            # 打开泄气阀门
            GPIO.output(21, 0)
            time.sleep(1)
            GPIO.output(21, 1)
            time.sleep(0.05)
            GPIO.output(20,0)
            print("Pump open (吸泵打开)...")
            time.sleep(2)

            GPIO.output(20,1)
            time.sleep(0.05)
            # 打开泄气阀门
            GPIO.output(21,0)
            time.sleep(1)
            GPIO.output(21,1)
            time.sleep(0.05)
            print("Pump close (吸泵关闭)...")
            time.sleep(1)
        GPIO.cleanup()
    elif model_number == 2:
        for i in range(10):
            cobot.set_basic_output(1,0)#OUT1输出打开
            print("Pump open (吸泵打开)...")
            time.sleep(2)
            cobot.set_basic_output(1,1)#OUT1输出关闭
            print("Pump close (吸泵关闭)...")
            time.sleep(2)
    else:
        raise ValueError("Invalid model number. Please select 1 for 280PI or 2 for 320PI.")


def perform_gripping_test(cobot):
    print("Starting gripping test (开始夹爪测试)...")
    for i in range(10):
        cobot.set_gripper_value(100, 50)
        print("Gripper open (夹爪打开)...")
        time.sleep(1)
        cobot.set_gripper_value(0, 50)
        print("Gripper close (夹爪关闭)...")
        time.sleep(1)

def joint_test(cobot):
    for i in range(1,7):
        cobot.send_angle(i,0,50)
        time.sleep(1)
        cobot.send_angle(i,20,50)
        time.sleep(1)
        cobot.send_angle(i,0,50)
        time.sleep(1)


def main():
    print("Please select your myCobot model (请选择你的机型):")
    print("1: 280PI")
    print("2: 320PI")

    model_number = int(input("Enter model number (1 or 2): "))
    port = list_serial_ports()
    if not port:
        print("No serial port selected. Exiting...")
        return  # Exit if no valid port is found.

    cobot = initialize_cobot(model_number, port)
    cobot.power_on()
    print("Move to the initial point(运动到初始点)....")
    cobot.send_angles([0,0,0,0,0,0],50)
    time.sleep(5)
    if model_number == 2:
        cobot.set_gripper_mode(0)

    while True:
        print("Please select a test feature (请选择测试功能):")
        print("1: Pump Test (吸泵测试)")
        print("2: Gripping Test (夹爪测试)")
        print("3: Joint Test (关节测试)")
        feature = int(input("Enter feature number (1 or 2 or 3): "))

        if feature == 1:
            perform_pump_test(model_number,cobot)
        elif feature == 2:
            perform_gripping_test(cobot)
        elif feature == 3:
            joint_test(cobot)
        else:
            print("Invalid selection (选择无效). Please try again (请重新选择).")


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)