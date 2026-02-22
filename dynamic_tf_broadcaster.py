import rclpy
from rclpy.node import Node
# 静态坐标发布器
from tf2_ros import TransformBroadcaster
# 消息接口
from geometry_msgs.msg import TransformStamped
# 欧拉角转四元数函数
from tf_transformations import quaternion_from_euler
# 角度转弧度
import math

class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('dynamic_tf_broadcaster')
        self.broadcaster_ = TransformBroadcaster(self)
        self.timer_ = self.create_timer(0.01,self.publish_tf)
    def publish_tf(self):
        """
        发布的TF,从camera_link到bottle_link之间的坐标关系
        """
        transform = TransformStamped()
        
        #定义父类坐标系
        transform.header.frame_id = 'camera_link'
        #定义子类坐标系
        transform.child_frame_id = 'bottle_link'
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
        self.broadcaster_.sendTransform(transform)
        self.get_logger().info(f'发布TF:{transform}')

def main():
    rclpy.init()
    node = TFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()


