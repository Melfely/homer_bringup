# homer_bringup
ROS package to start up HomeR hardware interface

## Installation
```console
# create workspace
mkdir -p ~/homer_ws/src
cd ~/homer_ws/src

# check out package
git clone https://github.com/linzhanguca/homer_bringup.git

# resolve binary dependencies and build workspace
source /opt/ros/$ROS_DISTRO/setup.bash
cd ~/homer_ws/
rosdep install -y --from-paths src --ignore-src --rosdistro $ROS_DISTRO
colcon build
source ~/homer_ws/install/local_setup.bash
echo "source ~/homer_ws/install/local_setup.bash" >> ~/.bashrc
```


## Usage
### For motion control and monitor only, start the `/pico_interface` node.

```console
ros2 run homer_bringup pico_interface
```


### For SLAM or autonomous navigation using LiDAR

```console
ros2 launch homer_bringup homer_launch.py
```
