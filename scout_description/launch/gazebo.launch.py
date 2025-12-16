import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Include Gazebo launch file
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("gazebo_ros"), "launch", "gazebo.launch.py"]
            )
        ),
    )

    # Static transform publisher from base_link to base_footprint
    static_tf_node = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        name="tf_footprint_base",
        arguments=["0", "0", "0", "0", "0", "0", "base_link", "base_footprint"],
    )

    # Path to the URDF file
    urdf_file = PathJoinSubstitution(
        [FindPackageShare("scout_description"), "urdf", "scout_mini.urdf"]
    )

    # Spawn the robot model in Gazebo
    spawn_entity_node = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        name="spawn_model",
        arguments=[
            "-file",
            urdf_file,
            "-entity",
            "scout_description",
        ],
        output="screen",
    )

    # Publish calibrated topic
    publish_calibrated = ExecuteProcess(
        cmd=[
            "ros2",
            "topic",
            "pub",
            "/calibrated",
            "std_msgs/msg/Bool",
            "{data: true}",
            "--once",
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            gazebo_launch,
            static_tf_node,
            spawn_entity_node,
            publish_calibrated,
        ]
    )
