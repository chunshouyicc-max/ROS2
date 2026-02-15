/*
cpp大胃袋
*/

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/u_int32.hpp"
#include <random>
#include <string>

class DaiweidaiNode : public rclcpp::Node
{
public:
    DaiweidaiNode(std::string name) : Node(name)
    {
        // 打印初始化信息
        RCLCPP_INFO(this->get_logger(), "无论生活有多苦涩，依旧是欢乐的！我是大胃袋%s", name.c_str());

        // 创建发布者（消息类型，话题名称，队列大小）
        publisher_ = this->create_publisher<std_msgs::msg::String>("meal_topic", 10);

        // 创建订阅者
        subscriber_ = this->create_subscription<std_msgs::msg::UInt32>(
            "total_wan", 10, std::bind(&DaiweidaiNode::sub_callback, this, std::placeholders::_1));

        // 创建定时器
        timer_period_ = std::chrono::seconds(5);
        timer_ = this->create_wall_timer(timer_period_, std::bind(&DaiweidaiNode::timer_callback, this));

        // 初始化随机数生成器
        random_gen_ = std::mt19937(random_device_());
        random_dist_ = std::uniform_int_distribution<>(1, 5);

        // 初始化属性
        num1_ = 0;
        num2_ = 0;
    }

private:
    // 定时器回调函数
    void timer_callback()
    {
        // 用随机数定义num1和num2
        num1_ = random_dist_(random_gen_);
        num2_ = random_dist_(random_gen_);

        // 创建并发布消息
        auto msg = std_msgs::msg::String();
        msg.data = "餐桌上有" + std::to_string(num1_) + "碗焖子和" + std::to_string(num2_) + "碗火烧，全给造了！";
        
        publisher_->publish(msg);
        RCLCPP_INFO(this->get_logger(), "播报今日伙食:%s", msg.data.c_str());
    }

    // 订阅者的回调函数
    void sub_callback(const std_msgs::msg::UInt32::SharedPtr msg)
    {
        (void)msg;  // 消除未使用参数的警告
        // 计算当天吃的
        int today_eat = num1_ + num2_;
        RCLCPP_INFO(this->get_logger(), "今天吃了%d碗", today_eat);
    }

    // 成员变量
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::Subscription<std_msgs::msg::UInt32>::SharedPtr subscriber_;
    rclcpp::TimerBase::SharedPtr timer_;
    std::chrono::seconds timer_period_;

    // 随机数相关
    std::random_device random_device_;
    std::mt19937 random_gen_;
    std::uniform_int_distribution<> random_dist_;

    int num1_;
    int num2_;
};

int main(int argc, char **argv)
{
    // 初始化ROS2
    rclcpp::init(argc, argv);

    // 创建节点并spin
    auto node = std::make_shared<DaiweidaiNode>("Liangzi");
    rclcpp::spin(node);

    // 关闭
    rclcpp::shutdown();
    return 0;
}