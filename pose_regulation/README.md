# demo_20260613 - poseRegulation


## Installation

### With Docker (if on ubuntu systems)

Install the docker image with the `tiago_public_ws` folder following the guide in [this github repository](https://github.com/DIAG-Robotics-Lab/labrob_tiago_docker).

The `tiago_public_ws` folder is in the root of the docker container created with the tutorial.

### Use Windows WLS (if on Windows systems)

in this case install WLS on your Window machine and follow the install an Ubuntu 20 image. Then follow the next section

### Directy on Ubuntu 20

Make sure you have followed the installation instructions in [http://wiki.ros.org/Robots/TIAGo/Tutorials](http://wiki.ros.org/Robots/TIAGo/Tutorials).

Install catkin_tools and clone this repository in the `src` folder inside your workspace. It is preferred to keep separated the `tiago_public_ws` and the workspace in which you can put all your ROS projects.

### Build your Project 

Create your custom workspace. The path should be something like `<MY_WORKSPACE>/<PROJECT_NAME>/src/<THIS_GITHUB_REPO>`

Before compiling your project, you have to source the tiago workspace whenever is located
```
source <PATH_TO_TIAGO_WS>/tiago_public_ws/devel/setup.bash
```

Make sure you are compiling in *Release* mode by properly setting your catkin workspace by calling:
```
catkin config --cmake-args -DCMAKE_BUILD_TYPE=Release
```
Build your code by running the following command:
```
catkin build
```
note that if you are using python it is sufficient to build the package only once

After the build is completed for the first time, you have to *source the current setup.bash* that have been created into the `devel` folder
```
source ./devel/setup.bash
```


## Usage

### Starting the simulation and loading the world

To run the Gazebo simulation:
```bash
roslaunch labrob_tiago_gazebo tiago_gazebo.launch public_sim:=true end_effector:=pal-gripper world:=<WORLD>     
```
Where `<WORLD>` is one of the worlds in `labrob_gazebo_worlds/worlds`.

For example, run 
```bash
roslaunch labrob_tiago_gazebo tiago_gazebo.launch public_sim:=true end_effector:=pal-gripper world:=labrob_empty     
```

### Run the simulation

To run your node:
```bash
roslaunch pose_regulation_ros1 pose_regulation_ros1.launch
```
