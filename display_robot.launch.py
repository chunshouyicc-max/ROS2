"""
这个启动文件的作用是自动找到你的 URDF 模型文件路径，并把它作为一个参数，方便后续节点加载这个机器人模型。
"""
import os#用于处理文件的路径的库，在spider中常用
import launch
import launch_ros
# 这个包可以根据文件名字找到目录，自动找到包的安装路径
from ament_index_python.packages import get_package_share_directory

# 固定不变，文件的启动函数
def generate_launch_description():
    
     # 获取urdf的路径，可以自动返回哦
    urdf_package_path = get_package_share_directory('chunshouy_description')
    
    # 拼接完整的文件路径，比如说最终得到了# 最终得到：/.../chunshouy_description/urdf/first_robot.urdf
    # 优点：这里的作用：不用写死绝对路径，不管你的工作空间在哪，都能找到正确的 URDF 文件
    default_urdf_path = os.path.join(urdf_package_path,'urdf','first_robot.urdf')
    default_rviz_config_path = os.path.join(urdf_package_path,'config','display_robot_model.rviz')


    # 声明一个urdf的目录参数，方便修改
    action_declare_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name = 'model',
        default_value=str(default_urdf_path),#默认数值是上面的urdf路径
        description='加载的模型文件路径:'
    )
    
    # 通过文件路径，获取内容，并转换成参数值对象，以供传入robot_state_publisher
    # 通过 cat <文件路径> 可以返回文件的内容                          cat后面要加空格！！！
    substitutions_command_result = launch.substitutions.Command(['cat ',launch.substitutions.LaunchConfiguration('model')])

    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(
        substitutions_command_result,
        value_type = str
    )
    

    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description':robot_description_value}]
    )
    
    action_joint_state_publisher =launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher'
    )

    action_rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d',default_rviz_config_path]
    
    )   

    return launch.LaunchDescription([
        action_declare_arg_mode_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_rviz_node
    ])

"""
运行以下命令：
source 复制setup.bash的路径
ros2 launch display_robot.launch.py
"""