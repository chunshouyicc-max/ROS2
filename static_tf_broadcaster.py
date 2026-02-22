import rclpy
from rclpy.node import Node
# 静态坐标发布器
from tf2_ros import StaticTransformBroadcaster
# 消息接口
from geometry_msgs.msg import TransformStamped
# 欧拉角转四元数函数
from tf_transformations import quaternion_from_euler
# 角度转弧度
import math

class StaticTFBroadcaster(Node):
    def __init__(self):
        super().__init__('static_tf_broadcaster')
        self.static_broadcaster_ = StaticTransformBroadcaster(self)
        self.publish_static_tf()

    def publish_static_tf(self):
        """
        发布静态的TF,从base_link到camera_link之间的坐标关系
        """
        transform = TransformStamped()
        
        #定义父类坐标系
        transform.header.frame_id = 'base_link'
        #定义子类坐标系
        transform.child_frame_id = 'camera_link'
        # 这是时间戳
        transform.header.stamp = self.get_clock().now().to_msg()

        # 平移部分，子在父的什么地方
        transform.transform.translation.x = 0.5
        transform.transform.translation.y = 0.3
        transform.transform.translation.z = 0.6 

        # 欧拉角转四元数
        # 设置旋转部分：绕X轴旋转180度（欧拉角转四元数）
        # quaternion_from_euler(roll, pitch, yaw) 参数顺序：横滚角、俯仰角、偏航角
        q = quaternion_from_euler(math.radians(180),0,0)
        
        # 旋转部分进行赋值
        transform.transform.rotation.x = q[0]
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]

        # 将静态坐标发布出去
        self.static_broadcaster_.sendTransform(transform)
        self.get_logger().info(f'发布静态TF:{transform}')

def main():
    rclpy.init()
    node = StaticTFBroadcaster()
    rclpy.spin(node)
    rclpy.shundown()


"""
要在setup.py中添加:
     'console_scripts': [
            # 可执行文件的名字=可执行文件上一级文件夹的名字.节点名：调用什么函数
            'static_tf_broadcaster=demo_python_tf.static_tf_broadcaster:main'
        ],
    ”“”
"""