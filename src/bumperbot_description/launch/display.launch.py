
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
import xacro
import os

def launch_setup(context, *args, **kwargs):
    # Resolve the model path at launch time
    model_path = LaunchConfiguration("model").perform(context)
    doc = xacro.process_file(model_path)
    robot_description = doc.toxml()

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )

    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(
            FindPackageShare("bumperbot_description").perform(context),
            "rviz",
            "display.rviz"
        )]
    )

    return [robot_state_publisher, joint_state_publisher_gui, rviz_node]

def generate_launch_description():
    default_model_path = PathJoinSubstitution(
        [FindPackageShare("bumperbot_description"), "urdf", "bumperbot.urdf.xacro"]
    )

    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=default_model_path,
        description="Absolute path to robot URDF file"
    )

    return LaunchDescription([
        model_arg,
        OpaqueFunction(function=launch_setup)
    ])
