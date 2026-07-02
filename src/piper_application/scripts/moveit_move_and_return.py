#!/usr/bin/env python3
import sys
import time
import rospy
import moveit_commander


def main():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node("piper_moveit_move_and_return", anonymous=True)

    group = moveit_commander.MoveGroupCommander("arm")

    # 安全速度，第一次建议慢一点
    group.set_max_velocity_scaling_factor(0.2)
    group.set_max_acceleration_scaling_factor(0.2)
    group.set_planning_time(5.0)

    print("当前规划组:", group.get_name())
    print("当前关节:", group.get_active_joints())
    print("当前关节角:", group.get_current_joint_values())

    input("确认机械臂周围安全后，按 Enter 开始执行...")

    # 目标位姿：这里先用一个保守测试位姿，单位是 rad
    target_joint_values = [
        -0.5,   # joint1
        0.6,   # joint2
        -0.68,  # joint3
        0.0,   # joint4
        0.1,  # joint5
        0.0    # joint6
    ]

    # target_joint_values = [
    #     0.2,   # joint1
    #     0.2,   # joint2
    #     -0.2,  # joint3
    #     0.3,   # joint4
    #     -0.2,  # joint5
    #     0.5    # joint6
    # ]

    print("开始移动到目标位姿...")
    group.set_joint_value_target(target_joint_values)
    success = group.go(wait=True)
    group.stop()
    group.clear_pose_targets()

    if not success:
        print("目标位姿执行失败，停止。")
        return

    print("已到达目标位姿，停顿 5 秒...")
    time.sleep(5)

    print("开始回到零位...")
    zero_joint_values = [0, 0, 0, 0, 0, 0]
    group.set_joint_value_target(zero_joint_values)
    success = group.go(wait=True)
    group.stop()
    group.clear_pose_targets()

    if success:
        print("已回到零位。")
    else:
        print("回零失败。")

    moveit_commander.roscpp_shutdown()


if __name__ == "__main__":
    main()