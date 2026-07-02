import time
from piper_sdk import C_PiperInterface

if __name__ == "__main__":
    print("=== 开始安全、低速运动测试 ===")
    
    # 1. 初始化接口 (dh_is_offset=1 适配你的 S-V1.8-8 新固件)
    piper = C_PiperInterface(can_name="can0", dh_is_offset=1)
    piper.ConnectPort()
    time.sleep(0.5)
    
    # 2. 设置控制模式，并【显著降低运动速度】
    # ctrl_mode=0x01 (CAN控制), move_mode=0x01 (关节运动 MOVE J)
    # move_spd_rate_ctrl=20 表示以 20% 的速度运动（范围0-100），动作会非常平缓
    print("1. 设置控制模式为 CAN / MOVE J，速度降至 20%...")
    piper.ModeCtrl(ctrl_mode=0x01, move_mode=0x01, move_spd_rate_ctrl=20)
    time.sleep(0.5)
    
    # 3. 使能所有电机 (7 代表所有关节)
    print("2. 使能机械臂...")
    piper.EnableArm(7)
    time.sleep(1.5) # 等待电机真正锁死并稳定
    
    # 4. 控制关节 1 转动到 15 度 (15 * 1000 = 15000)
    print("3. 关节 1 缓慢转动到 15 度... (请注意观察！)")
    piper.JointCtrl(15000, 0, 0, 0, 0, 0)
    
    # 因为是低速运动，所以等待时间要稍微长一点，确保它运动到位并完全停稳
    time.sleep(4.0) 
    
    # ==========================================
    # 🛡️ 核心改进：安全失能流程
    # ==========================================
    print("4. 【安全提示】正在将机械臂缓慢移动回安全的零位姿态...")
    print("   ⚠️ 建议：此时请用手轻轻托住机械臂的末端，以防万一。")
    
    # 发送全 0 指令，让机械臂收缩回最安全、重心最低的初始状态
    piper.JointCtrl(0, 0, 0, 0, 0, 0)
    
    # ⚠️ 
