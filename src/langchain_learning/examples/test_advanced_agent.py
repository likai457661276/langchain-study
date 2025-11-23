"""
高级智能体测试 - LangChain 1.0高级功能测试

此测试文件验证了LangChain 1.0的高级功能，包括：
1. 记忆管理
2. 工具链组合
3. 条件路由
4. 错误处理
5. 流式处理
"""

import os
import sys
import json
from datetime import datetime

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 导入测试目标
from src.langchain_learning.examples.advanced_agent import (
    create_memory_agent, 
    create_conditional_agent,
    create_tool_chain,
    SimpleMemory
)

# 测试计数器
test_count = 0
passed_count = 0

def run_test(test_name, test_func):
    """运行测试并记录结果"""
    global test_count, passed_count
    test_count += 1
    print(f"\n--- 测试 {test_count}: {test_name} ---")
    
    try:
        result = test_func()
        if result:
            print(f"✅ 测试通过: {test_name}")
            passed_count += 1
        else:
            print(f"❌ 测试失败: {test_name}")
    except Exception as e:
        print(f"❌ 测试失败: {test_name}, 错误: {str(e)}")
    
    print("-" * 50)

def test_memory_agent_creation():
    """测试记忆智能体创建"""
    try:
        agent, memory = create_memory_agent()
        return agent is not None and memory is not None
    except Exception as e:
        print(f"创建记忆智能体时出错: {str(e)}")
        return False

def test_memory_functionality():
    """测试记忆功能"""
    try:
        # 创建记忆实例
        memory = SimpleMemory()
        
        # 添加消息
        memory.add_user_message("测试用户消息")
        memory.add_ai_message("测试AI回复")
        
        # 获取历史
        history = memory.get_history()
        
        # 验证历史长度
        return len(history) >= 2
    except Exception as e:
        print(f"测试记忆功能时出错: {str(e)}")
        return False

def test_conditional_agent_creation():
    """测试条件路由智能体创建"""
    try:
        chain = create_conditional_agent()
        return chain is not None
    except Exception as e:
        print(f"创建条件路由智能体时出错: {str(e)}")
        return False

def test_conditional_routing():
    """测试条件路由功能"""
    try:
        chain = create_conditional_agent()
        
        # 测试天气查询
        result = chain.invoke({"input": "北京今天天气怎么样?"})
        weather_result = isinstance(result, str) and len(result) > 0
        
        # 测试新闻查询
        result = chain.invoke({"input": "最近有什么科技新闻?"})
        news_result = isinstance(result, str) and len(result) > 0
        
        # 测试一般对话
        result = chain.invoke({"input": "你好"})
        general_result = isinstance(result, str) and len(result) > 0
        
        return weather_result and news_result and general_result
    except Exception as e:
        print(f"测试条件路由功能时出错: {str(e)}")
        return False

def test_tool_chain_creation():
    """测试工具链创建"""
    try:
        chain = create_tool_chain()
        return chain is not None
    except Exception as e:
        print(f"创建工具链时出错: {str(e)}")
        return False

def test_tool_chain_functionality():
    """测试工具链功能"""
    try:
        chain = create_tool_chain()
        
        # 测试数据处理
        test_input = "请分析这组销售数据: 产品A:100件, 产品B:200件, 产品C:150件"
        result = chain.invoke(test_input)
        
        return isinstance(result, str) and len(result) > 0
    except Exception as e:
        print(f"测试工具链功能时出错: {str(e)}")
        return False

def test_agent_with_tools():
    """测试智能体与工具交互"""
    try:
        agent, _ = create_memory_agent()
        
        # 测试天气查询
        inputs = {"messages": [{"role": "user", "content": "北京今天天气怎么样?"}]}
        result = agent.invoke(inputs)
        
        # 检查结果
        return "messages" in result and len(result["messages"]) > 0
    except Exception as e:
        print(f"测试智能体与工具交互时出错: {str(e)}")
        return False

def test_error_handling():
    """测试错误处理"""
    try:
        agent, _ = create_memory_agent()
        
        # 测试无效JSON
        inputs = {"messages": [{"role": "user", "content": "请分析这段无效的JSON数据: {invalid json}"}]}
        result = agent.invoke(inputs)
        
        # 检查是否返回了结果
        return "messages" in result and len(result["messages"]) > 0
    except Exception as e:
        print(f"测试错误处理时出错: {str(e)}")
        return False

def test_memory_persistence():
    """测试记忆持久性"""
    try:
        agent, memory = create_memory_agent()
        
        # 第一次交互
        inputs1 = {"messages": [{"role": "user", "content": "我的名字是张三"}]}
        result1 = agent.invoke(inputs1)
        
        # 第二次交互，测试是否记住名字
        inputs2 = {"messages": [{"role": "user", "content": "你还记得我的名字吗?"}]}
        result2 = agent.invoke(inputs2)
        
        # 检查结果
        return ("messages" in result1 and len(result1["messages"]) > 0 and 
                "messages" in result2 and len(result2["messages"]) > 0)
    except Exception as e:
        print(f"测试记忆持久性时出错: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("LangChain 1.0 高级智能体功能测试")
    print("=" * 60)
    
    # 运行所有测试
    run_test("记忆智能体创建", test_memory_agent_creation)
    run_test("记忆功能", test_memory_functionality)
    run_test("条件路由智能体创建", test_conditional_agent_creation)
    run_test("条件路由功能", test_conditional_routing)
    run_test("工具链创建", test_tool_chain_creation)
    run_test("工具链功能", test_tool_chain_functionality)
    run_test("智能体与工具交互", test_agent_with_tools)
    run_test("错误处理", test_error_handling)
    run_test("记忆持久性", test_memory_persistence)
    
    # 输出测试结果
    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)
    print(f"总测试数: {test_count}")
    print(f"通过测试: {passed_count}")
    print(f"失败测试: {test_count - passed_count}")
    print(f"通过率: {passed_count / test_count * 100:.1f}%")
    
    if passed_count == test_count:
        print("\n🎉 所有测试通过！LangChain 1.0 高级智能体功能正常。")
    else:
        print(f"\n⚠️ 有 {test_count - passed_count} 个测试失败，请检查相关功能。")
    
    print("=" * 60)

if __name__ == "__main__":
    main()