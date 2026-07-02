#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真正的即停脚本：立即切断机械臂所有电机动力的。
不做任何运动，不做任何等待，只做一件事：失能！
"""
import time
from piper_sdk import C_PiperInterface

def emergency_stop():
    print("🚨🚨🚨 紧急即停！正在立即切断电机动力！🚨🚨🚨")
    
    try:
        # 1. 连接 CAN（这是唯一必要的初始化）
        piper = C_PiperInterface(can_name="can0", dh_is_offset=1)
        piper.ConnectPort()
        time.sleep(0.1)  # 只等 100ms，不能再多了
        
        # 2. 立即失能所有关节（切断动力，电机抱闸锁死或释放）
        piper.DisableArm(7)  # 7 = 所有 6 个关节 + 夹爪
        print("✅ 所有关节已失能！电机动力已切断！")
        
        # 3. 关闭通信
        time.sleep(0.2)
        piper.DisconnectPort()
        
    except Exception as e:
        print(f"⚠️ 即停过程中出现异常: {e}")
        print("👉 请立即按下物理急停按钮或关闭电源！")

if __name__ == "__main__":
    emergency_stop()