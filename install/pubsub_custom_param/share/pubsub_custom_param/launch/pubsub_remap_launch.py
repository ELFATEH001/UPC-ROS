from ast import Or
from launch import LaunchDescription
from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition, LaunchConfigurationEquals, LaunchConfigurationNotEquals
from launch.substitutions import PathJoinSubstitution, PythonExpression, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare

def launch_setup(context, *args, **kwargs):
    # Initialize Arguments
    excute_sub2 = LaunchConfiguration("excute_sub2")

    #Publisher node 1
    pub_node = Node(
        namespace='pub1',
        package='pubsub_custom_param',
        executable='publisher_class',
        output='screen'
    )
    #Publisher node 2
    pub2_node = Node(
        namespace='pub2',
        package='pubsub_custom_param',
        executable='publisher_class',
        output='screen'
    )
    #Subscriber node
    sub_node = Node(
        package='pubsub_custom_param',
        executable='subscriber_class',
        remappings=[('my_topic', 'pub1/my_topic')],
        output='screen'
    )

    #Conditional subscriber node based on a launch argument
    sub2_node = Node(
        name='subscriber_node2',
        package='pubsub_custom_param',
        executable='subscriber_class',
        remappings=[('my_topic', 'pub2/my_topic')],
        output='screen',
        condition=IfCondition(excute_sub2),
        # condition=IfCondition(
        #     # wrap the LaunchConfiguration with quotes so the final python expression is safe:
        #     PythonExpression(["'", number_of_subscribers_argument, "' in ['2','3']"])
        # )
    )

    

    nodes_to_start = [
        pub_node,
        pub2_node,
        sub_node,
        sub2_node,
    ]

    return nodes_to_start


def generate_launch_description():
    # Declare arguments
    declared_arguments = []
    # Add arguments
    declared_arguments.append(
        DeclareLaunchArgument(
            "excute_sub2",
            default_value='false',
            description='Excute the second subscriber or not according to the user choice'
            
        )
    )

    return LaunchDescription(declared_arguments + [OpaqueFunction(function=launch_setup)])
