import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
 
def generate_launch_description():
    package_name = 'robot'
    robot_name = 'robot'
 
    # Package path
    pkg_path = get_package_share_directory(package_name)
    pkg_parent = os.path.dirname(pkg_path)
 
    # URDF path
    urdf_file = os.path.join(pkg_path, 'urdf', 'robot.urdf')
    with open(urdf_file, 'r') as file:
        robot_description = file.read()
 
    # Config paths
    bridge_yaml = os.path.join(pkg_path, 'config', 'gz_bridge.yaml')
    rviz_config = os.path.join(pkg_path, 'config', 'robot.rviz')
 
    # Allow Gazebo to find meshes
    gazebo_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=pkg_parent
    )
 
    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'robot_description': robot_description,
                'use_sim_time': True
            }
        ],
        output='screen'
    )
 
    # Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': '-r empty.sdf'
        }.items(),
    )
 
    # Spawn Robot
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', robot_name,
            '-string', robot_description,
            '-z', '0.25'
        ],
        output='screen'
    )
 
    # Bridge pakai YAML
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['--ros-args', '-p', f'config_file:={bridge_yaml}'],
        output='screen'
    )
 
    # Static TF untuk imu_link -> base
    static_tf_imu = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0.02', '0', '0', '0', 'base', 'imu_link'],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )
 
    # RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config] if os.path.exists(rviz_config) else [],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )
 
    return LaunchDescription([
        gazebo_resource_path,
        gazebo,
        robot_state_publisher,
        spawn_robot,
        bridge,
        static_tf_imu,
    ])

