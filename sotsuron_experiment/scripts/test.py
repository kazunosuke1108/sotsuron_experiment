import os


os.system(f"rosbag play {os.environ['HOME']+'/catkin_ws/src/ytlab_rosbag/rosbag/'}_2022-12-25-17-34-13.bag")
print("hello")













# import rospy
# from sensor_msgs.msg import JointState



# def callback(data):
#     idx=data.name.index('head_pan_joint')
#     rospy.loginfo(data.name)
#     rospy.loginfo(data.position[idx])
#     pass

# rospy.init_node("test")
# rospy.Subscriber("/hsrb/joint_states",JointState,callback)
# rospy.spin()