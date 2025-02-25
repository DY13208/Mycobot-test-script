import time
from pymycobot import MyCobot280, MyCobot320
import serial
# 使用此代码前请确保代码为直立状态
# Before using this code, please make sure the code is in an upright state.
#使用次脚本请注意必须使用pymycobot>=3.6.0 ，使用pip install pymycobot==3.6.8可以更新pymycobot版本库3.6.8代表了版本，具体版本信息可以去官网查看
# Please note that when using this script, pymycobot>=3.6.0 must be used. You can update the pymycobot version library by using pip install pymycobot==3.6.8. 3.6.8 represents the version. For specific version information, you can check the official website.
def initialize_cobot(model_number, port):
    if model_number == 1:
        return MyCobot280(port, 115200)
    elif model_number == 2:
        return MyCobot320(port, 115200)
    else:
        raise ValueError("Invalid model number. Please select 1 for 280M5 or 2 for 320M5.")

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

def write_servo_status_to_file(file, cobot):
    servo_status_messages = [
        (1, "Servo enable 1:"),
        (2, "Servo enable 2:"),
        (3, "Servo enable 3:"),
        (4, "Servo enable 4:"),
        (5, "Servo enable 5:"),
        (6, "Servo enable 6:")
    ]

    for servo_id, message in servo_status_messages:
        status = cobot.is_servo_enable(servo_id)
        file.write(f"{message} {status}\n")

def write_info_to_file(cobot):
    print("写入中....")
    with open('output.txt', 'w') as file:
        system_version = cobot.get_system_version()
        file.write(f"atom version: {system_version}\n")

        basic_version = cobot.get_basic_version()
        file.write(f"basic version: {basic_version}\n")

        error_info = cobot.get_error_information()
        file.write(f"error information: {error_info}\n")

        next_error = cobot.read_next_error()
        file.write(f"read next error: {next_error}\n")

        servo_status = cobot.get_servo_status()
        file.write(f"Servo status : {servo_status}\n")

        servo_voltages = cobot.get_servo_voltages()
        file.write(f"Servo voltages : {servo_voltages}\n")

        write_servo_status_to_file(file, cobot)

        servo_indices = [i for i in range(70) if
                         i not in {10, 12, 25, 29, 32, 43, 49, 50, 51, 52, 53, 54, 57, 58, 59, 61, 67, 68}]
        for i in range(1, 7):
            file.write(f"Servo {i} data: ")
            for j in servo_indices:
                servo_data = cobot.get_servo_data(i, j)
                file.write(f"[{j}]: {servo_data}  ")
            file.write("\n")

def main():
    print("Please select your myCobot model (请选择你的机型):")
    print("1: 280M5 (280M5)")
    print("2: 320M5 (320M5)")

    model_number = int(input("Enter model number (1 or 2): "))
    port = list_serial_ports()
    if not port:
        print("No serial port selected. Exiting...")
        return  # Exit if no valid port is found.
    cobot = initialize_cobot(model_number, port)
    write_info_to_file(cobot)
    print("Information write completed! (信息写入完成！)")

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)