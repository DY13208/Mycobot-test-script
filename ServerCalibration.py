import time
from pymycobot import MyCobot280, MyCobot320
import serial
# 使用此代码前请确保代码为直立状态
# Before using this code, please make sure the code is in an upright state.
#使用次脚本请注意必须使用pymycobot>=3.6.0 ，使用pip install pymycobot==3.6.8可以更新pymycobot版本库3.6.8代表了版本，具体版本信息可以去官网查看
# Please note that when using this script, pymycobot>=3.6.0 must be used. You can update the pymycobot version library by using pip install pymycobot==3.6.8. 3.6.8 represents the version. For specific version information, you can check the official website.
#因为本程序是为了校准关节所准备，请在使用上电前手动将所有关节移动到刻度线处，否则会导致零位偏移
# As this program is prepared for calibrating joints, please manually move all joints to the scale line before powering on. Otherwise, it will lead to zero offset.
def get_user_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number（请输入有效的数字）")

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
    try:
        if model_number == 1:
            return MyCobot280(port, 115200)
        elif model_number == 2:
            return MyCobot280(port, 1000000)
        elif model_number == 3:
            return MyCobot320(port, 115200)
        elif model_number == 4:
            return MyCobot320(port, 115200)
        else:
            raise ValueError("Invalid model number.")
    except Exception as e:
        print(f"Error initializing the myCobot connection，Check whether the serial port is correct（初始化myCobot连接时出错，请检查串口是否正确）: {e}")
        return None


def calibrate_servos(cobot):
    for i in range(1,7):
        cobot.set_servo_calibration(i)
        print(f"Servo {i} calibration（校准） succeeded")
        time.sleep(0.5)


def main():
    print("Please select your myCobot model (请选择你的机型):")
    print("1: 280M5")
    print("2: 280PI/JN")
    print("3: 320M5")
    print("4: 320PI")

    model_number = get_user_input("Enter model number (1 or 2 or 3 or 4): ")
    port = list_serial_ports()
    cobot = initialize_cobot(model_number, port)

    if cobot:
        print("Starting servo calibration (开始校准关节)!")
        calibrate_servos(cobot)
    else:
        print("Program ended (程序结束)")


if __name__ == "__main__":
    main()