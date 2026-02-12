/*   a.导入库文件   b.初始化客户端库
     c.新建节点       d.spin循环节点
     e.关闭客户端库
*/

//导入库
#include  "rclcpp/rclcpp.hpp"


class Man: public rclcpp::Node
{
private:
    /*data*/
public:
    Man(std::string name):Node(name)
    {
        RCLCPP_INFO(this->get_logger(),"自尊常常将人拖着，把爱都走曲折------%s",name.c_str());
    }

};
//新建节点
int main(int argc,char ** argv){
    
    //循环节点
    rclcpp::init(argc,argv);
    auto node = std::make_shared<Man>("wang3");

    
    //关闭客户端
    rclcpp::spin(node);
    rclcpp::shutdown();
    system("pause");
    return 0;
}
