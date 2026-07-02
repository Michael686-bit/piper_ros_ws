import time
from piper_sdk import C_PiperInterface

def safe_shutdown():
    print("=== 开始执行 Piper 机械臂安全关机流程 ===")
    
    # 1. 初始化接口
    piper = C_PiperInterface(can_name="can0", dh_is_offset=1)
    piper.ConnectPort()
    time.sleep(0.5)
    
    # 2. 检查机械臂当前是否处于使能(通电锁死)状态
    enable_status = piper.GetArmEnableStatus()
    
    if any(enable_status):
        print("⚠️ 检测到机械臂当前处于使能状态，正在执行安全归零...")
        print("   请确保机械臂周围 1 米内无障碍物，建议用手轻轻托住末端以防万一。")
        
        # 切换到关节控制模式，并设置较低的速度 (例如 30%) 保证动作平缓
        piper.ModeCtrl(ctrl_mode=0x01, move_mode=0x01, move_spd_rate_ctrl=30)
        time.sleep(0.5)
        
        # 发送全 0 指令，让机械臂收缩回重心最低、最安全的初始零位姿态
        piper.JointCtrl(0, 0, 0, 0, 0, 0)
        
        # ⚠️ 关键：必须等待足够长的时间，确保机械臂完全回到零位并且彻底停稳！
        # 如果没停稳就失能，残余的惯性依然会导致它晃动或砸落。
        print("   等待机械臂完全停稳 (约 4 秒)...")
        time.sleep(4.0) 
    else:
        print("✅ 机械臂当前已处于失能(松弛)状态，跳过归零步骤。")

    # 3. 执行软件失能操作 (安全切断电机保持力)
    print("🔌 正在执行软件失能 (DisableArm)...")
    piper.DisableArm(7) # 7 代表失能所有 6 个关节
    time.sleep(1.0)
    
    # 4. 关闭 CAN 端口，释放系统资源
    print("📡 正在关闭 CAN 通信端口...")
    piper.DisconnectPort()
    
    print("=== 软件安全停机完成！机械臂关节已完全松弛。 ===")
    print("👉 现在您可以安全地关闭机械臂底座的物理电源开关了。")

if __name__ == "__main__":
    safe_shutdown()
