"""
a.导入服务接口
b.创建服务端回调函数
c.声明并创建服务端
d.编写回调函数逻辑处理请求
"""

# a.导入服务接口
import rclpy
from rclpy.node import Node
# 导入话题消息类型
from std_msgs.msg import String, UInt32
# 导入服务接口
from village_interfaces.srv import BorrowMoney

class WriterNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info('大家好我是作家%s.' % name)
        
        # 声明并创建发布者
        self.pub_novel = self.create_publisher(String, "sexy_girl", 10)
        
        self.count = 0

        # 定义定时周期
        self.timer_period = 5
    
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # 创建我的账户
        self.account = 80
        # 声明并发布订阅者
        self.sub_money = self.create_subscription(UInt32, "sexy_girl_money", self.recv_money_callback, 10)

        # 创建服务端
        self.borrow_server = self.create_service(BorrowMoney, "borrow_money", self.borrow_money_callback)

    # 服务端回调函数
    def borrow_money_callback(self, request, response):
        # 根据srv定义：request有name和money，response有success和money
        self.get_logger().info(f"收到来自：{request.name}元的借钱请求，账户中有：{self.account}元")
        
        if request.money <= self.account * 0.1:
            response.success = True
            response.money = request.money
            self.account = self.account - response.money
            self.get_logger().info(f'成功借出{response.money}元，账户余额{self.account}元')
        else:
            response.success = False
            response.money = 0
            self.get_logger().info("现在手头紧，借不了")
        
        return response

    def timer_callback(self):
        msg = String()
        msg.data = "第{}回:谢东阳的{}岁".format(self.count, self.count)
        
        # 让发布者发布消息
        self.pub_novel.publish(msg)

        self.get_logger().info("发布了一个章节的小说，内容是:%s" % msg.data)
    
        self.count += 1

    # 建回调函数
    def recv_money_callback(self, money):
        self.account += money.data
        self.get_logger().info(f"收到了{money.data}的稿费，账户现有{self.account}元")

# 初始化客户端库
def main(args=None):
    rclpy.init(args=args)
    
    # 新建节点对象
    jieqian_node = WriterNode('LaoJiang')
    
    # spin循环节点
    rclpy.spin(jieqian_node)

    # 关闭客户端库
    rclpy.shutdown()

if __name__ == '__main__':
    main()


# source install/setup.bash

# ros2 service list -t

# ros2 service call /borrow_money village_interfaces/srv/BorrowMoney "{name: 'jaingguaugtou', money: 5}"