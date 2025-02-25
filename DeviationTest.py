import time
from pymycobot import MyCobot280, MyCobot320
import serial
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
    """根据型号初始化机械臂"""
    if model_number == 1:
        return MyCobot280(port, 115200)
    elif model_number == 2:
        return MyCobot320(port, 115200)
    else:
        raise ValueError("Invalid model number. Please select 1 for 280M5 or 2 for 320M5.")

def perform_gripping_test(cobot):
    """执行夹爪测试"""
    print("Starting gripping test...")
    for i in range(10):
        cobot.set_gripper_value(100, 50)  # 打开夹爪
        print("Gripper open...")
        time.sleep(1)
        cobot.set_gripper_value(0, 50)    # 关闭夹爪
        print("Gripper close...")
        time.sleep(1)

def run_actions(cobot, angles, z_offset=-20, z_recovery=40):
    """
    执行通用的机械臂动作序列。
    包括初始化关节角度、执行预设动作、调整Z轴坐标和夹爪操作。
    """
    print("Running actions...")

    # 初始化机械臂动作
    cobot.set_gripper_value(100, 50)  # 打开夹爪
    cobot.send_angles([0, 0, 0, 0, 0, 0], 30)  # 初始化关节角度
    time.sleep(3)

    # 执行预设动作
    cobot.send_angles(angles, 30)
    time.sleep(3)
    cobot.set_gripper_value(100, 50)  # 打开夹爪
    time.sleep(1)

    # 获取当前坐标并调整
    coord_list = cobot.get_coords()
    if coord_list:
        cobot.send_coord(3, coord_list[2] + z_offset, 30)  # 调整 Z 轴
        time.sleep(1)
        cobot.set_gripper_value(0, 50)  # 关闭夹爪
        time.sleep(1)
        cobot.send_coord(3, coord_list[2] + z_recovery, 30)  # 恢复 Z 轴
        time.sleep(1)
    else:
        print("Failed to get coordinates. Skipping coordinate adjustments.")

    print("Actions completed.")

def main():
    """主函数，执行机械臂测试流程"""
    print("Please select your myCobot model:")
    print("1: 280M5")
    print("2: 320M5")

    try:
        model_number = int(input("Enter model number (1 or 2): "))

        port = list_serial_ports()

        cobot = initialize_cobot(model_number, port)

        # 执行预设动作序列
        predefined_angles = [155.21, -80.85, -1.05, 1.84, 3.51, 120.49]
        run_actions(cobot, predefined_angles)

        # 执行新增的动作序列
        additional_angles = [110.56, -52.03, -73.12, 46.66, 1.4, 132.89]
        run_actions(cobot, additional_angles)

        cobot.send_angles([0,0,0,0,0,0],50)
        time.sleep(3)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()