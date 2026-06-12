cmake_minimum_required(VERSION 3.0.2)
project(pose_regulation_ros1)
find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  std_msgs
)

catkin_python_setup()

catkin_package(
  CATKIN_DEPENDS
  rospy
  geometry_msgs
  std_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

install(PROGRAMS
  scripts/pose_regulation_ros1
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)