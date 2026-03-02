import rclpy
from rclpy.node import Node
import yaml
import time

from geometry_msgs.msg import Twist
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped


class PatrolNode(Node):
    # 构造函数，初始化节点
    def __init__(self):
        super().__init__('patrol_node')  # 初始化节点名为 'patrol_node'

        # 创建一个发布者，用于发送速度命令到 /cmd_vel 话题，控制机器人移动
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # 创建一个 ActionClient，负责与 NavigateToPose action 服务器通信，发出导航命令
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    # 主巡逻任务，读取并执行 YAML 配置文件中的巡逻点
    def patrol(self):
        # 打开 YAML 文件，读取巡逻点数据
        with open('/root/fishbot/src/patrol_task/config/patrol_points.yaml', 'r') as file:
            points = yaml.safe_load(file)['points']

        # 遍历所有巡逻点，执行相应的动作
        for point in points:
            # 创建目标位置的 PoseStamped 消息
            pose = PoseStamped()
            pose.header.frame_id = 'map'  # 设置坐标系为地图坐标系
            pose.pose.position.x = point['x']  # 设置目标点的 x 坐标
            pose.pose.position.y = point['y']  # 设置目标点的 y 坐标
            pose.pose.orientation.w = 1.0  # 设置目标点的方向为默认方向（面向前方）

            # 根据 YAML 配置中的 action，选择相应的行动
            if point['action'] == 'stop':
                self.stop(pose, point['time'])  # 调用停止方法，停留指定时间
            elif point['action'] == 'rotate':
                self.rotate(pose, point['time'])  # 调用旋转方法，执行旋转动作
            elif point['action'] == 'speed_up':
                self.speed_up(pose, point['time'])  # 调用加速方法，加速指定时间
            elif point['action'] == 'finish':
                self.finish()  # 任务结束，调用 finish 方法，关闭 ROS2 节点

    # 停止机器人，停留指定时间
    def stop(self, pose, time_sec):
        self.get_logger().info(f'Stopping at {pose.pose.position.x}, {pose.pose.position.y}')
        self.move_robot(pose)  # 调用 move_robot 方法，使机器人移动到目标位置
        time.sleep(time_sec)  # 停留指定的时间

    # 旋转机器人，旋转指定时间
    def rotate(self, pose, time_sec):
        self.get_logger().info(f'Rotating at {pose.pose.position.x}, {pose.pose.position.y}')
        self.move_robot(pose)  # 调用 move_robot 方法，使机器人旋转
        time.sleep(time_sec)  # 旋转持续时间

    # 加速机器人，持续时间为指定的 time_sec
    def speed_up(self, pose, time_sec):
        self.get_logger().info(f'Speeding up at {pose.pose.position.x}, {pose.pose.position.y}')
        self.move_robot(pose)  # 调用 move_robot 方法，开始加速
        time.sleep(time_sec)  # 持续加速指定的时间

    # 任务完成，退出节点
    def finish(self):
        self.get_logger().info('Patrol finished') 
        rclpy.shutdown()  # 关闭 ROS2 节点

    # 控制机器人运动，向目标位置发出导航命令
    def move_robot(self, pose):
        # 创建导航目标的消息，包含目标位置
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose

        # 等待导航服务器准备好
        self.nav_client.wait_for_server()

        # 发送导航目标，控制机器人移动
        self.nav_client.send_goal_async(goal_msg)

# main 函数，初始化 ROS2 节点并开始执行巡逻任务
def main():
    rclpy.init()  # 初始化 ROS2 系统
    node = PatrolNode()  # 创建 PatrolNode 实例
    node.patrol()  # 开始执行巡逻任务
    rclpy.spin(node)  # 保持节点运行

if __name__ == '__main__':
    main()
