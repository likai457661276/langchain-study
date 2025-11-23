"""
LangChain 1.0 智能体演示脚本

此脚本提供了一个简单的界面，用于演示LangChain 1.0智能体的主要功能。
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def print_header():
    """打印标题"""
    print("=" * 60)
    print("LangChain 1.0 智能体演示")
    print("=" * 60)
    print("此演示展示了LangChain 1.0智能体的主要功能")
    print("包括基础工具调用、记忆管理、条件路由等高级功能")
    print("=" * 60)

def print_menu():
    """打印菜单"""
    print("\n请选择演示类型:")
    print("1. 基础智能体演示")
    print("2. 高级智能体演示")
    print("3. 运行所有测试")
    print("4. 退出")
    print("-" * 40)

def run_basic_demo():
    """运行基础智能体演示"""
    print("\n正在启动基础智能体演示...")
    print("基础智能体包含以下功能:")
    print("- 交互式对话")
    print("- 结构化输出")
    print("- 中间件功能")
    print("\n请在新的终端窗口中运行以下命令:")
    print("python src/langchain_learning/examples/agent_with_tools.py")
    input("\n按Enter键返回主菜单...")

def run_advanced_demo():
    """运行高级智能体演示"""
    print("\n正在启动高级智能体演示...")
    print("高级智能体包含以下功能:")
    print("- 记忆管理")
    print("- 条件路由")
    print("- 工具链组合")
    print("- 流式处理")
    print("- 错误处理")
    print("\n请在新的终端窗口中运行以下命令:")
    print("python src/langchain_learning/examples/advanced_agent.py")
    input("\n按Enter键返回主菜单...")

def run_all_tests():
    """运行所有测试"""
    print("\n正在运行所有测试...")
    print("这将测试基础和高级智能体的所有功能")
    print("\n请在新的终端窗口中运行以下命令:")
    print("python src/langchain_learning/examples/test_agent.py")
    print("\n然后运行:")
    print("python src/langchain_learning/examples/test_advanced_agent.py")
    input("\n按Enter键返回主菜单...")

def show_examples():
    """显示示例用法"""
    print("\n=== 示例用法 ===")
    print("\n1. 基础智能体交互示例:")
    print("用户: 北京今天天气怎么样?")
    print("助手: [调用weather_search工具] 北京当前天气: 温度15°C, 晴朗, 湿度45%, 风速5km/h")
    
    print("\n2. 高级智能体记忆示例:")
    print("用户: 我喜欢蓝色")
    print("助手: 我记住了，你喜欢蓝色。")
    print("用户: 我喜欢什么颜色?")
    print("助手: 根据之前的对话，你喜欢蓝色。")
    
    print("\n3. 条件路由示例:")
    print("用户: 请帮我安排一个会议")
    print("系统: [识别为任务调度意图] 转到任务调度处理链")
    print("助手: 任务已调度: ID=TASK-1234, 任务=安排会议, 优先级=medium, 调度时间=2023-11-15 14:30:00")
    
    input("\n按Enter键返回主菜单...")

def main():
    """主函数"""
    while True:
        print_header()
        print_menu()
        
        choice = input("请输入选项 (1-4): ")
        
        if choice == "1":
            run_basic_demo()
        elif choice == "2":
            run_advanced_demo()
        elif choice == "3":
            run_all_tests()
        elif choice == "4":
            print("\n感谢使用LangChain 1.0智能体演示!")
            print("更多信息请参考README.md文档")
            break
        else:
            print("\n无效选项，请重新输入。")
            input("按Enter键继续...")

if __name__ == "__main__":
    main()