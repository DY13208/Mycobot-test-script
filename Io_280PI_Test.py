from datetime import datetime
import RPi.GPIO as GPIO
import time

# 使用此代码前请确保代码为直立状态
# Before using this code, please make sure the code is in an upright state.
#使用次脚本请注意必须使用pymycobot>=3.6.0 ，使用pip install pymycobot==3.6.8可以更新pymycobot版本库3.6.8代表了版本，具体版本信息可以去官网查看
# Please note that when using this script, pymycobot>=3.6.0 must be used. You can update the pymycobot version library by using pip install pymycobot==3.6.8. 3.6.8 represents the version. For specific version information, you can check the official website.

# Set the GPIO mode to BCM.
GPIO.setmode(GPIO.BCM)

pin = 23

# Get the mode input by the user.
mode = int(input("Please enter the mode (1 for input mode, 2 for output mode):"))

# Set the pin mode according to the input.
if mode == 1:
    # Set the pin as input mode and enable the internal pull-down resistor.
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
elif mode == 2:
    # Set the pin as output mode.
    GPIO.setup(pin, GPIO.OUT)
else:
    print("The input mode is invalid. Please enter 1 or 2.")
    GPIO.cleanup()
    exit()

try:
    if mode == 1:
        while True:
            # If the pin level is low (0).
            if GPIO.input(pin) == 0:
                print(f"PIN IO 23 ，time：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                pass
            else:
                print(f"PIN IO 23 change，time：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                break
            time.sleep(0.1)
    elif mode == 2:
        # 将引脚电平设置为高（1）Set the pin level to low (1).
        GPIO.output(pin, GPIO.HIGH)
        print(f"PIN IO 23 set to HIGH：{GPIO.input(pin)}")
        time.sleep(1)
        # 将引脚电平设置为低（0）Set the pin level to low (0).
        GPIO.output(pin, GPIO.LOW)
        print(f"PIN IO 23 set to LOW：{GPIO.input(pin)}")
        time.sleep(1)

except KeyboardInterrupt:
    print("The program was manually terminated")

finally:
    # Clean up GPIO settings.
    GPIO.cleanup()