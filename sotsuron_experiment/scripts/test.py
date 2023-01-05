import rospy
from sensor_msgs.msg import JointState

def callback(data):
    idx=data.name.index('head_pan_joint')
    rospy.loginfo(data.name)
    rospy.loginfo(data.position[idx])
    pass

rospy.init_node("test")
rospy.Subscriber("/hsrb/joint_states",JointState,callback)
rospy.spin()