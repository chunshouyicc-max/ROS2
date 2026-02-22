import rclpy
from rclpy.node import Node
#TransformListener 监听TF变换的监听器
#Buffer 缓存TF变换的缓冲区，存储所有坐标系关系
from tf2_ros import TransformListener, Buffer
# 四元数转欧拉角
from tf_transformations import euler_from_quaternion
# 时间相关
import rclpy.time
import math


class TFBroadcaster(Node):
    def __init__(self):
        super().__init__('dynamic_tf_broadcaster')
        self.buffer_ = Buffer()
        self.listener_ = TransformListener(self.buffer_, self)  # 改名更合适
        self.timer_ = self.create_timer(1.0, self.get_transform)
        
    def get_transform(self):
        """
        定时查询坐标关系
        """
        try:
            # 修正1: 使用正确的方式创建时间和持续时间
            result = self.buffer_.lookup_transform(
                'base_link', 
                'bottle_link',
                rclpy.time.Time(),  # 使用空构造函数表示最新时间
                timeout=rclpy.duration.Duration(seconds=1.0)  # 修正持续时间的创建方式
            )
            
            transform = result.transform
            self.get_logger().info(f'平移: {transform.translation}')
            
            # 修正2: 正确打印旋转信息（之前打印的是平移）
            self.get_logger().info(f'旋转四元数: {transform.rotation}')
            
            # 修正3: 正确调用euler_from_quaternion函数
            # 这个函数期望接收一个包含4个元素的列表/元组
            rotation_euler = euler_from_quaternion([
                transform.rotation.x,
                transform.rotation.y,
                transform.rotation.z,
                transform.rotation.w
            ])
            
            # 修正4: 打印欧拉角结果
            self.get_logger().info(f'旋转RPY (弧度): roll={rotation_euler[0]:.3f}, pitch={rotation_euler[1]:.3f}, yaw={rotation_euler[2]:.3f}')
            
            # 转换为角度
            self.get_logger().info(f'旋转RPY (角度): roll={math.degrees(rotation_euler[0]):.1f}°, pitch={math.degrees(rotation_euler[1]):.1f}°, yaw={math.degrees(rotation_euler[2]):.1f}°')
            
        except Exception as e:
            self.get_logger().info(f'获取坐标变换失败: 原因 {str(e)}')


def main():
    rclpy.init()
    node = TFBroadcaster()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()