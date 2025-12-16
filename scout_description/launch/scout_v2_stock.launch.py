import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare launch arguments
    robot_namespace_arg = DeclareLaunchArgument(
        "robot_namespace",
        default_value="/",
        description="Robot namespace",
    )

    urdf_extras_arg = DeclareLaunchArgument(
        "urdf_extras",
        default_value=PathJoinSubstitution(
            [FindPackageShare("scout_description"), "urdf", "empty.urdf"]
        ),
        description="Path to URDF extras file",
    )

    # Get URDF via xacro with arguments
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("scout_description"), "urdf", "scout_v2.xacro"]
            ),
            " ",
            "robot_namespace:=",
            LaunchConfiguration("robot_namespace"),
            " ",
            "urdf_extras:=",
            LaunchConfiguration("urdf_extras"),
        ]
    )

    robot_description = {"robot_description": robot_description_content}

    # Robot State Publisher Node (to publish the robot description)
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
        namespace=LaunchConfiguration("robot_namespace"),
    )

    return LaunchDescription(
        [
            robot_namespace_arg,
            urdf_extras_arg,
            robot_state_publisher_node,
        ]
    )
