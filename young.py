"""
village_li.village_li.young 的 Docstring
a.导入库文件      b.初始化客户端库
c.新建节点对象    d.spin循环节点
e.关闭客户端库
"""
#导入库文件
import rclpy
from rclpy.node import Node

# 初始化客户端库
def main(args = None):
    rclpy.init(args = args)
    
    # 新建节点对象
    young_node = Node('YOUNG') 
    young_node.get_logger().info('hello ,I am Young') 
    # spin循环节点
    rclpy.spin(young_node)

    # 关闭客户端库
    rclpy.shutdown()

# 在town_li目录下面进行编译
# colcon build
# source install/setup.bash
# ros2 pkg list | grep vill
# ros2 run village_li young_node


# CTRL+SHIFT+5打开一并列终端
# ros2 node list------/YOUNG
# ros2 node info /YOUNG ------查看节点信息