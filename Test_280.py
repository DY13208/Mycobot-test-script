from pymycobot import MyCobot280
import time

# 初始化机械臂
mc = MyCobot280("COM26", 115200)

def test_get_system_version():
    """测试获取主控版本"""
    print("测试获取主控版本...")
    version = mc.get_system_version()
    if version:
        print(f"获取到的版本号: {version}")
        assert version, "版本号获取失败或为空"
        print("测试通过！")
    else:
        print("测试失败，未获取到版本号！")

def test_power_on():
    """测试机械臂上电"""
    print("测试机械臂上电...")
    mc.power_on()
    time.sleep(1)  # 等待上电完成
    status = mc.is_power_on()
    if status == 1:
        print("机械臂已成功上电！")
        assert status == 1, "机械臂上电失败"
    else:
        print("机械臂上电失败！")

def test_power_off():
    """测试机械臂下电"""
    print("测试机械臂下电...")
    mc.power_off()
    time.sleep(1)  # 等待下电完成
    status = mc.is_power_on()
    if status == 0:
        print("机械臂已成功下电！")
        assert status == 0, "机械臂下电失败"
    else:
        print("机械臂下电失败！")

def test_get_angles():
    """测试获取全关节角度"""
    print("测试获取全关节角度...")
    angles = mc.get_angles()
    if angles:
        print(f"当前关节角度: {angles}")
        assert len(angles) == 6, "获取的关节角度数量不正确"
        print("测试通过！")
    else:
        print("测试失败，未获取到关节角度！")

def test_send_angles():
    """测试设置多关节角度"""
    print("测试设置多关节角度...")
    target_angles = [0, 30, -30, 45, -45, 0]  # 目标角度
    mc.send_angles(target_angles, 50)  # 设置速度为50
    time.sleep(5)  # 等待运动完成
    current_angles = mc.get_angles()
    if current_angles:
        print(f"当前关节角度: {current_angles}")
        for i in range(6):
            assert abs(current_angles[i] - target_angles[i]) <= 1, f"关节{i+1}角度未达到目标"
        print("测试通过！")
    else:
        print("测试失败，未获取到关节角度！")

def test_get_coords():
    """测试获取全关节坐标"""
    print("测试获取全关节坐标...")
    coords = mc.get_coords()
    if coords:
        print(f"当前坐标: {coords}")
        assert len(coords) == 6, "获取的坐标数量不正确"
        print("测试通过！")
    else:
        print("测试失败，未获取到坐标！")

def test_send_coords():
    """测试设置全关节坐标"""
    print("测试设置全关节坐标...")
    target_coords = [-125.5, -198.6, 297.8, -54.1, 30.31, -124.71]  # 目标坐标
    mc.power_on()  # 确保机械臂已上电
    time.sleep(1)
    mc.send_coords(target_coords, 20)  # 设置速度为20
    while mc.is_moving():  # 等待机械臂停止运动
        time.sleep(0.1)
    current_coords = mc.get_coords()
    if current_coords:
        print(f"目标坐标: {target_coords}")
        print(f"当前坐标: {current_coords}")
        for i in range(6):
            assert abs(current_coords[i] - target_coords[i]) <= 10, f"坐标{i+1}未达到目标"
        print("测试通过！")
    else:
        print("测试失败，未获取到坐标！")

def main():
    test_get_system_version()
    test_power_on()
    test_get_angles()
    test_send_angles()
    test_get_coords()
    test_send_coords()
    # test_power_off()

if __name__ == "__main__":
    main()