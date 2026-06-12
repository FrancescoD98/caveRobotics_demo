import numpy as np

# frequency of the ROS node
freq = 100

# desired joint angles
q_base_des = np.array([2.0, 3.0, 0.0])

# gain
k1 = 1.0
k2 = 2.5
k3 = 3.0
k_arm = 5