#!/usr/bin/env python3
"""
测试脚本 - 验证LangChain 1.0智能体示例
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
sys.path.insert(0, project_root)

def test_imports():
    """测试导入是否正常"""
    print("测试导入...")
    try:
        from src.langchain_learning.examples.agent_with_tools import (
            create_agent_with_tools,
            structured_output_demo,
            middleware_demo
        )
        print("✓ 导入成功")
        return True
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_agent_creation():
    """测试智能体创建"""
    print("\n测试智能体创建...")
    try:
        from src.langchain_learning.examples.agent_with_tools import create_agent_with_tools
        agent = create_agent_with_tools()
        print("✓ 智能体创建成功")
        return True
    except Exception as e:
        print(f"✗ 智能体创建失败: {e}")
        return False

def test_agent_invoke():
    """测试智能体调用"""
    print("\n测试智能体调用...")
    try:
        from src.langchain_learning.examples.agent_with_tools import create_agent_with_tools
        from langchain_core.messages import HumanMessage
        
        agent = create_agent_with_tools()
        inputs = {"messages": [HumanMessage(content="请生成一个1到5之间的随机数")]}
        result = agent.invoke(inputs)
        
        if "messages" in result and result["messages"]:
            ai_message = result["messages"][-1]
            print(f"✓ 智能体调用成功: {ai_message.content[:50]}...")
            return True
        else:
            print("✗ 智能体调用失败: 无有效返回")
            return False
    except Exception as e:
        print(f"✗ 智能体调用失败: {e}")
        return False

def test_tools():
    """测试工具功能"""
    print("\n测试工具功能...")
    try:
        from src.langchain_learning.examples.agent_with_tools import (
            generate_random_number,
            memory_write,
            memory_read,
            get_current_time,
            calculator
        )
        
        # 测试随机数生成
        result = generate_random_number.invoke({"min_val": 1, "max_val": 10})
        print(f"✓ 随机数工具: {result}")
        
        # 测试内存写入
        result = memory_write.invoke({"key": "test", "value": "测试值"})
        print(f"✓ 内存写入工具: {result}")
        
        # 测试内存读取
        result = memory_read.invoke({"key": "test"})
        print(f"✓ 内存读取工具: {result}")
        
        # 测试时间工具
        result = get_current_time.invoke({})
        print(f"✓ 时间工具: {result}")
        
        # 测试计算器工具
        result = calculator.invoke({"expression": "2 + 3"})
        print(f"✓ 计算器工具: {result}")
        
        return True
    except Exception as e:
        print(f"✗ 工具测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("LangChain 1.0 智能体示例测试")
    print("=" * 50)
    
    # 检查API密钥
    api_key = os.getenv("SILICONFLOW_API_KEY", "")
    if not api_key:
        print("警告: 未找到 SILICONFLOW_API_KEY 环境变量")
        print("某些测试可能会失败")
    
    # 运行测试
    tests = [
        test_imports,
        test_agent_creation,
        test_agent_invoke,
        test_tools
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有测试通过！")
        return 0
    else:
        print("✗ 部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())