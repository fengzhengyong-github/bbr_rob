# bbr_rob
Basketball Robot
## 环境
**操作系统**：Ubuntu 22.04  
**ROS 2**：Humble  
**Gazebo**：classic
## 依赖
```
sudo apt install ros-humble-robot-state-publisher
sudo apt install ros-humble-joint-state-publisher
sudo apt install ros-humble-xacro
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install ros-humble-ros2-control
sudo apt install ros-humble-ros2-controllers
sudo apt install ros-humble-gazebo-ros2-control
```
可能有多余的依赖，但不知道是哪些，全装上。
##  构建包
```
mkdir -p your_ws/src && cd your_ws/src
git clone https://github.com/fengzhengyong-github/bbr_rob.git
cd ..
colcon build --symlink-install
source install/setup.bash
ros2 launch bbr_description gazebo_sim.launch.py
```
可用ros2自带的键盘控制节点控制小车轮子，重新打开一个终端，输入以下命令
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard 
