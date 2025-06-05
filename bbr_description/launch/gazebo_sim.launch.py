import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # 获取默认路径
    robot_name_in_model = "bbr_rob"
    urdf_tutorial_path = get_package_share_directory('bbr_rob')
    default_model_path = urdf_tutorial_path + '/bbr_description/urdf/bbr_rob.xacro'
    default_rviz_config_path = urdf_tutorial_path + '/bbr_description/config/rviz/gazebo_launch.rviz'
    default_world_path = urdf_tutorial_path + '/bbr_description/world/custom_room.world'
   
    # 为 Launch 声明参数
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model', default_value=str(default_model_path),
        description='URDF 的绝对路径')
   
    # 获取文件内容生成新的参数
    robot_description = launch_ros.parameter_descriptions.ParameterValue(
        launch.substitutions.Command(
            ['xacro ', launch.substitutions.LaunchConfiguration('model')]),
        value_type=str)
  	
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', default_rviz_config_path]
    )

    # 通过 IncludeLaunchDescription 包含另外一个 launch 文件
    launch_gazebo = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'gazebo_ros'), '/launch', '/gazebo.launch.py']),
      	# 传递参数
        launch_arguments=[('world', default_world_path),('verbose','true')]
    )
  
    # 请求 Gazebo 加载机器人
    spawn_entity_node = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', '/robot_description',
                   '-entity', robot_name_in_model, ])
    
    load_joint_state_controller = launch.actions.ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'bbr_joint_state_broadcaster'],
        output='screen')

    load_effort_controller = launch.actions.ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'bbr_effort_controller'], 
        output='screen')

    load_diff_drive_controller = launch.actions.ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'bbr_diff_drive_controller'], 
        output='screen')

    close_evt1 =  launch.actions.RegisterEventHandler( 
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=spawn_entity_node,
                on_exit=[load_joint_state_controller],
            )
    )

    close_evt2 =  launch.actions.RegisterEventHandler( 
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[load_diff_drive_controller],
            )
    )
    
    return launch.LaunchDescription([
        close_evt1,
        close_evt2,
        action_declare_arg_mode_path,
        robot_state_publisher_node,
        rviz_node,
        launch_gazebo,
        spawn_entity_node,
        
    ])
# ros2 run teleop_twist_keyboard teleop_twist_keyboard 
