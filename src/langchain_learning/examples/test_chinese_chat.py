#!/usr/bin/env python3
"""
测试中文聊天助手功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# 加载环境变量
load_dotenv()

def test_chinese_chat():
    """测试中文聊天功能"""
    print("🤖 中文聊天助手测试")
    print("=" * 50)
    
    # 初始化模型
    try:
        model = ChatOpenAI(
            model="Qwen/Qwen3-8B",
            api_key=os.getenv("SILICONFLOW_API_KEY"),
            base_url="https://api.siliconflow.cn/v1",
            temperature=0.7,
            max_tokens=1024
        )
        print("✓ 已连接到硅基流动 Qwen3-8B 模型")
    except Exception as e:
        print(f"✗ 模型初始化失败: {e}")
        print("请确保您已在 .env 文件中设置了 SILICONFLOW_API_KEY")
        return
    
    # 测试对话
    print("\n测试对话:")
    print("-" * 30)
    
    # 初始化消息历史
    messages = [
        SystemMessage(content="你是一个友好的中文助手，请用中文回答问题，保持简洁和礼貌。")
    ]
    
    # 添加测试问题
    test_questions = [
        "你好，请介绍一下你自己",
        "LangChain是什么？",
        "如何使用Python进行异步编程？"
    ]
    
    for question in test_questions:
        print(f"\n用户: {question}")
        
        # 添加用户消息到历史
        messages.append(HumanMessage(content=question))
        
        try:
            # 获取模型响应
            response = model.invoke(messages)
            
            # 添加 AI 响应到历史
            messages.append(response)
            
            # 显示 AI 响应
            print(f"助手: {response.content}")
        except Exception as e:
            print(f"错误: {e}")
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_chinese_chat()