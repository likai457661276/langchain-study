"""
LangChain 1.0 智能体自动演示脚本

此脚本自动演示LangChain 1.0智能体的主要功能。
"""

import os
import sys
import time

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def print_header(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f" {title} ")
    print("=" * 60)

def print_step(step):
    """打印步骤"""
    print(f"\n[步骤] {step}")
    print("-" * 40)

def run_command_with_output(command, description):
    """运行命令并显示输出"""
    print_step(f"执行: {description}")
    print(f"命令: {command}")
    print("\n输出:")
    
    # 使用os.system运行命令并捕获输出
    result = os.system(command)
    
    print(f"\n执行结果: {'成功' if result == 0 else '失败'}")
    return result == 0

def demo_basic_agent():
    """演示基础智能体"""
    print_header("基础智能体演示")
    
    print("基础智能体包含以下功能:")
    print("- 交互式对话")
    print("- 结构化输出")
    print("- 中间件功能")
    
    # 演示结构化输出
    print_step("演示结构化输出功能")
    run_command_with_output(
        'echo 2 | python src/langchain_learning/examples/agent_with_tools.py',
        "运行结构化输出示例"
    )
    
    # 演示中间件功能
    print_step("演示中间件功能")
    run_command_with_output(
        'echo 3 | python src/langchain_learning/examples/agent_with_tools.py',
        "运行中间件示例"
    )
    
    print("\n基础智能体演示完成!")

def demo_advanced_agent():
    """演示高级智能体"""
    print_header("高级智能体演示")
    
    print("高级智能体包含以下功能:")
    print("- 记忆管理")
    print("- 条件路由")
    print("- 工具链组合")
    print("- 流式处理")
    print("- 错误处理")
    
    # 演示记忆管理
    print_step("演示记忆管理功能")
    run_command_with_output(
        'echo 2 | python src/langchain_learning/examples/advanced_agent.py',
        "运行记忆管理示例"
    )
    
    # 演示工具链组合
    print_step("演示工具链组合功能")
    run_command_with_output(
        'echo 3 | python src/langchain_learning/examples/advanced_agent.py',
        "运行工具链组合示例"
    )
    
    # 演示错误处理
    print_step("演示错误处理功能")
    run_command_with_output(
        'echo 5 | python src/langchain_learning/examples/advanced_agent.py',
        "运行错误处理示例"
    )
    
    print("\n高级智能体演示完成!")

def run_all_tests():
    """运行所有测试"""
    print_header("运行所有测试")
    
    print("这将测试基础和高级智能体的所有功能")
    
    # 运行基础测试
    print_step("运行基础智能体测试")
    basic_success = run_command_with_output(
        'python src/langchain_learning/examples/test_agent.py',
        "基础智能体测试"
    )
    
    # 运行高级测试
    print_step("运行高级智能体测试")
    advanced_success = run_command_with_output(
        'python src/langchain_learning/examples/test_advanced_agent.py',
        "高级智能体测试"
    )
    
    # 总结测试结果
    print_step("测试结果总结")
    print(f"基础智能体测试: {'通过' if basic_success else '失败'}")
    print(f"高级智能体测试: {'通过' if advanced_success else '失败'}")
    print(f"总体结果: {'全部通过' if basic_success and advanced_success else '存在失败'}")

def show_examples():
    """显示示例用法"""
    print_header("示例用法")
    
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
    
    print("\n4. 工具链组合示例:")
    print("用户: 请分析销售数据: 产品A:100件, 产品B:200件, 产品C:150件")
    print("系统: [调用工具链] 数据分析 -> 排序 -> 文本生成")
    print("助手: 销量排序: 产品B(200件) > 产品C(150件) > 产品A(100件)")

def main():
    """主函数"""
    print_header("LangChain 1.0 智能体自动演示")
    
    print("此演示将自动展示LangChain 1.0智能体的主要功能")
    print("包括基础工具调用、记忆管理、条件路由等高级功能")
    
    # 显示示例用法
    show_examples()
    
    # 演示基础智能体
    demo_basic_agent()
    
    # 等待一下
    time.sleep(2)
    
    # 演示高级智能体
    demo_advanced_agent()
    
    # 等待一下
    time.sleep(2)
    
    # 运行所有测试
    run_all_tests()
    
    # 总结
    print_header("演示总结")
    print("LangChain 1.0 智能体演示已完成!")
    print("\n主要功能包括:")
    print("✓ 基础智能体 - 工具调用、结构化输出、中间件")
    print("✓ 高级智能体 - 记忆管理、条件路由、工具链、流式处理、错误处理")
    print("✓ 完整测试套件 - 验证所有功能正常工作")
    print("\n更多信息请参考README.md文档")
    print("=" * 60)

if __name__ == "__main__":
    main()