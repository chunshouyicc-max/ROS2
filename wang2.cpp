/*   a.导入库文件   b.初始化客户端库
     c.新建节点       d.spin循环节点
     e.关闭客户端库
*/

//导入库
#include  "rclcpp/rclcpp.hpp"

//新建节点
int main(int argc,char ** argv){
    
    //循环节点
    rclcpp::init(argc,argv);
    auto node = std::make_shared<rclcpp::Node>("wang2");
    
    
    RCLCPP_INFO(node->get_logger(),"遇见她如春水应梨花");
    
    
    //关闭客户端
    rclcpp::spin(node);
    rclcpp::shutdown();
    system("pause");
    return 0;
}


// 要在CMakeList.txt文件中添加东西

 /*添加可执行文件
add_executable(wang2_node src/wang2.cpp)

# 设置依赖
ament_target_dependencies(wang2_node rclcpp)

# 安装可执行文件 - ✅ 修正：空格分隔，不是下划线
install(TARGETS
  wang2_node
  DESTINATION lib/${PROJECT_NAME}  # 这里是空格！不是下划线！
)

# ✅ 将ament_package移到最末尾！
ament_package()
*/

// 指定功能包进行build
// colcon build --packages-select village_wang

/*
source install/setup.bash
ros2 run village_wang wang2_node 
*/