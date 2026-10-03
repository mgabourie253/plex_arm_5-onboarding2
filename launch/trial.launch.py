from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
    )

    joy_translator = Node(
        package='plex_arm_5',
        executable='joy_translator',
        name='joy_translator',
    )

    return LaunchDescription([
        joy_node,
        joy_translator,
    ])