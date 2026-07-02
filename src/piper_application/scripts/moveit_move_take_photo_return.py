#!/usr/bin/env python3
import os
import time
import rospy
import moveit_commander
import cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge


def take_photo(image_topic="/camera/color/image_raw"):
    bridge = CvBridge()

    rospy.loginfo("等待相机图像: %s", image_topic)
    msg = rospy.wait_for_message(image_topic, Image, timeout=5.0)

    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

    save_dir = os.path.expanduser("~/piper_photos")
    os.makedirs(save_dir, exist_ok=True)

    filename = time.strftime("piper_photo_%Y%m%d_%H%M%S.jpg")
    save_path = os.path.join(save_dir, filename)

    cv2.imwrite(save_path, cv_image)

    rospy.loginfo("拍照完成，图片已保存: %s", save_path)
    return save_path


def main():
    rospy.init_node("moveit_move_take_photo_return", anonymous=True)
    moveit_commander.roscpp_initialize([])

    arm = moveit_commander.MoveGroupCommander("arm")

    # 当前位姿作为返回点
    home_joint = arm.get_current_joint_values()
    rospy.loginfo("记录当前位置作为返回点")

    # ===== 目标位置：这里先用示例关节角 =====
    target_joint = home_joint[:]

    target_joint[0] = -0.5
    target_joint[1] = 0.6
    target_joint[2] = -0.68
    target_joint[3] = 0.0
    target_joint[4] = 0.1
    target_joint[5] = 0.0

        #     -0.5,   # joint1
        # 0.6,   # joint2
        # -0.68,  # joint3
        # 0.0,   # joint4
        # 0.1,  # joint5
        # 0.0    # joint6

    rospy.loginfo("开始运动到目标位置")
    arm.go(target_joint, wait=True)
    arm.stop()

    rospy.sleep(1.0)
    rospy.loginfo("机械臂已到达目标位置并停稳")

    photo_path = take_photo("/camera/color/image_raw")

    rospy.loginfo("开始返回初始位置")
    arm.go(home_joint, wait=True)
    arm.stop()

    rospy.loginfo("执行完成：机械臂已拍照并返回")
    print("执行完成：机械臂已到达目标位置、完成拍照、并返回初始位置")
    print("照片路径:", photo_path)


if __name__ == "__main__":
    main()
