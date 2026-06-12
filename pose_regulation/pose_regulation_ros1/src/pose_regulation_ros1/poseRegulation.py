import numpy as np
import rospy
import math

from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Twist 

from pose_regulation_ros1 import params

class poseRegulation:

    def __init__(self, freq):
        
        self.n  = 3 # (x, y, theta)
        self.q  = np.zeros(self.n) 
        self.dq = np.zeros(self.n)

        # ROS subscribers
        self.base_odom_subscriber = rospy.Subscriber('/gazebo/model_states', ModelStates, self.model_state_callback)
        self.target_base_subscriber = rospy.Subscriber('/target_base', Float64MultiArray, self.target_base_callback)
        
        # ROS publishers
        self.velocity_publisher = rospy.Publisher('/mobile_base_controller/cmd_vel', Twist, queue_size=10)
        
        # time step of the node
        self.freq = freq
        self.dt = 1/self.freq

        # gains
        self.k1 = params.k1
        self.k2 = params.k2
        self.k3 = params.k3


    # callbacks from gazebos or TIAGo topics
    def model_state_callback(self, msg):
        for i in range(len(msg.name)):
            if msg.name[i] == 'tiago':
                # the position is (x, y, z)
                self.q[0] = msg.pose[i].position.x
                self.q[1] = msg.pose[i].position.y
                # the orientation is a quaternion (qx, qy, qz, qw)
                quat = msg.pose[i].orientation
                self.q[2] = math.atan2( # theta 
                    2.0 * (quat.w * quat.z + quat.x * quat.y),
                    1.0 - 2.0 * (quat.y * quat.y + quat.z * quat.z)
                )
    
    def publish_base_command(self, v_des, w_des):
        # Create a twist ROS message:
        msg_twist = Twist()
        msg_twist.linear.x = v_des
        msg_twist.linear.y = 0.0
        msg_twist.linear.z = 0.0
        msg_twist.angular.x = 0.0
        msg_twist.angular.y = 0.0
        msg_twist.angular.z = w_des
        # Publish a twist ROS message:
        self.velocity_publisher.publish(msg_twist)
        print('v: ', v_des, ' w: ', w_des)
        return
    
    def target_base_callback(self, msg):
        if len(msg.data) != 3:
            rospy.logerr('Received target base configuration has wrong size. Expected 3 of the form (x, y, theta), got ' + str(len(msg.data)) + ' of the form ' + str(msg.data))
            return
        params.q_base_des[0] = msg.data[0]
        params.q_base_des[1] = msg.data[1]
        params.q_base_des[2] = msg.data[2]
        return


    # Wrap angle to [-pi, pi):
    def wrap_angle(self, theta):
        return math.atan2(math.sin(theta), math.cos(theta))


    # simulation loop
    def start(self):
        # set the frequency of the node
        rate = rospy.Rate(self.freq) # Hz
        rospy.loginfo('Controller is running')
        rospy.loginfo('Frequency: ' + str(self.freq) + ' Hz')
        rospy.loginfo('Bring the robot in the configuration' + str(params.q_base_des))
        # control loop
        while not rospy.is_shutdown():
            # base control
            x_d = params.q_base_des[0]
            y_d = params.q_base_des[1]
            theta_d = params.q_base_des[2]
            x = self.q[0]
            y = self.q[1]
            theta = self.q[2]

            # Unicycle configuration in desired reference frame coordinates:
            x_r = math.cos(-theta_d) * (x - x_d) - math.sin(-theta_d) * (y - y_d)
            y_r = math.sin(-theta_d) * (x - x_d) + math.cos(-theta_d) * (y - y_d)
            theta_r = self.wrap_angle(-theta_d + theta)

            # Polar coordinates in relative coordinates:
            rho   = math.sqrt(math.pow(x_r, 2.0) + math.pow(y_r, 2.0))
            gamma = self.wrap_angle(math.atan2(y_r, x_r) - theta_r + math.pi)
            delta = self.wrap_angle(gamma + theta_r)

            # Feedback control:
            if abs(rho) < 1e-2:
                v_cmd = 0.0
                w_cmd = 0.0
            else:
                v_cmd = self.k1 * rho * math.cos(gamma)
                w_cmd = self.k2 * gamma + self.k1 * math.sin(gamma) * math.cos(gamma) / gamma * (gamma + self.k3 * delta)
        
            self.publish_base_command(v_cmd, w_cmd)

            # sleep until the next cycle
            rate.sleep()





def main():
    rospy.init_node('pose_regulation_ros1', log_level=rospy.INFO)
    
    motion_control_manager = poseRegulation(params.freq)
    motion_control_manager.start()