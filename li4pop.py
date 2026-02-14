"""
导入消息类型

声明并创建发布者

编写发布逻辑发布数据

"""

#导入库文件
import rclpy
from rclpy.node import Node
from std_msgs.msg import String,UInt32

class WriterNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info('大家好我是作家%s.' % name)
        
        # 声明并创建发布者
        self.pub_novel = self.create_publisher(String,"sexy_girl",10)
        
        self.count = 0

        # 定义定时周期
        self.timer_period = 5
    
        self.timer = self.create_timer(self.timer_period,self.timer_callback)

        #创建我的账户
        self.account = 80
        # 声明并发布订阅者
        self.sub_money =self.create_subscription(UInt32,"sexy_girl_money",self.recv_money_callback,10)

    def timer_callback(self):
        msg = String()
        msg.data = "第{}回:谢东阳的{}岁".format(self.count,self.count)
        
        # 让发布者发布消息
        self.pub_novel.publish(msg)

        self.get_logger().info("发布了一个章节的小说，内容是:%s" % msg.data)
    
        self.count += 1

    # 建回调函数
    def recv_money_callback(self,money):
        self.account += money.data
        self.get_logger().info(f"收到了{money.data}的稿费,账户现有{self.account}钱")

# 初始化客户端库
def main(args = None):
    rclpy.init(args = args)
    
    # 新建节点对象
    young_node = WriterNode('mao_mao')
    
    # spin循环节点
    rclpy.spin(young_node)

    # 关闭客户端库
    rclpy.shutdown()

# colcon build
# source install/setup.bash
# ros2 pkg list | grep vill
# ros2 run village_li young_node


# ros2 topic pub /sexy_girl_money std_msgs/msg/UInt32 "{data: 10}"