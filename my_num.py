"""
这是我照猫画虎写的大胃袋良子的发布与订阅，放心食用
"""
import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import String,UInt32

# 创建大胃袋类，继承Node类
class DaiweidaiNode(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info(f"无论生活有多苦涩，依旧是欢乐的！我是大胃袋{name}")

        #建立发布者(消息类型，话题名称，队列大小，也叫缓冲10)
        self.publisher = self.create_publisher(String,"meal_topic",10)

         # 建立订阅者
        self.subscriber = self.create_subscription(UInt32,'total_wan',self.sub_callback,10)
        
         # 定义一个计时器
        self.timer_period = 5
        self.timer = self.create_timer(self.timer_period,self.timer_callback)
        
        # 初始化属性
        self.num1 = 0
        self.num2 = 0

    #定义回调函数，传到上面create_timer()，时间一到自动调用 
    def timer_callback(self):
        
        # 用随机数定义num1和num2
        self.num1 = random.randint(1,5)
        self.num2 = random.randint(1,5)
        
        msg = String()
        msg.data = '餐桌上有{}碗焖子和{}碗火烧，全给造了！'.format(self.num1,self.num2)

         # 发布者发送消息
        self.publisher.publish(msg)
        self.get_logger().info(f'播报今日伙食:{msg.data}')

    # 接受者的回调函数
    def sub_callback(self,msg):
        # 只计算当天吃的（即当次触发时的数量），不进行累计
        today_eat = self.num1 + self.num2
        self.get_logger().info(f'今天吃了{today_eat}碗，收到消息：{msg.data}')

# 初始化客户端
def main(args = None):
    rclpy.init(args = args)

    # 新建节点对象
    liangzi_node = DaiweidaiNode('liangzi')

    # spin循环节点
    rclpy.spin(liangzi_node)

    # 关闭客户端
    rclpy.shutdown()

