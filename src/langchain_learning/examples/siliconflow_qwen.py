"""
硅基流动 Qwen/Qwen3-8B 模型集成示例
此示例展示如何使用 LangChain 1.0 集成硅基流动的 Qwen3-8B 模型
"""

import os
import sys
import requests
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import langchain

# 加载环境变量
load_dotenv()

def print_langchain_version():
    """打印当前 LangChain 版本"""
    print(f"当前 LangChain 版本: {langchain.__version__}")
    print(f"LangChain 核心包版本: {langchain.__version__}")

def list_available_models():
    """列出硅基流动平台上可用的模型"""
    api_key = os.getenv("SILICONFLOW_API_KEY")
    
    if not api_key:
        raise ValueError("未找到 SILICONFLOW_API_KEY 环境变量，请检查 .env 文件")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get("https://api.siliconflow.cn/v1/models", headers=headers)
        if response.status_code == 200:
            models = response.json().get("data", [])
            print("\n=== 可用模型列表 ===")
            for model in models:
                print(f"- {model.get('id')}")
            return models
        else:
            print(f"获取模型列表失败: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"获取模型列表时出错: {str(e)}")
        return []

def setup_siliconflow_qwen():
    """设置硅基流动的 Qwen3-8B 模型"""
    api_key = os.getenv("SILICONFLOW_API_KEY")
    
    if not api_key:
        raise ValueError("未找到 SILICONFLOW_API_KEY 环境变量，请检查 .env 文件")
    
    # 使用 ChatOpenAI 类连接硅基流动的 API
    # 硅基流动兼容 OpenAI API 格式
    model = ChatOpenAI(
        model="Qwen/Qwen3-8B",  # 使用硅基流动平台上的确切模型名称
        openai_api_base="https://api.siliconflow.cn/v1",
        openai_api_key=api_key,
        temperature=0.7,
        max_tokens=1024,
    )
    
    return model

def test_qwen_model():
    """测试 Qwen3-8B 模型"""
    print("正在初始化 Qwen 模型...")
    
    try:
        model = setup_siliconflow_qwen()
        print("✓ 模型初始化成功")
        
        # 测试简单对话
        print("\n=== 测试简单对话 ===")
        messages = [
            SystemMessage(content="你是一个有帮助的助手，请用中文回答问题。"),
            HumanMessage(content="请介绍一下你自己，你是什么模型？")
        ]
        
        response = model.invoke(messages)
        print(f"用户: {messages[1].content}")
        print(f"模型: {response.content}")
        
        # 测试代码生成
        print("\n=== 测试代码生成 ===")
        code_messages = [
            SystemMessage(content="你是一个专业的 Python 开发者，请编写简洁高效的代码。"),
            HumanMessage(content="请写一个 Python 函数，计算斐波那契数列的第 n 项。")
        ]
        
        code_response = model.invoke(code_messages)
        print(f"用户: {code_messages[1].content}")
        print(f"模型:\n{code_response.content}")
        
        # 测试流式响应
        print("\n=== 测试流式响应 ===")
        stream_messages = [
            SystemMessage(content="你是一个创意写作助手，请用中文回答。"),
            HumanMessage(content="请写一首关于春天的短诗")
        ]
        
        print("用户: 请写一首关于春天的短诗")
        print("模型: ", end="", flush=True)
        
        for chunk in model.stream(stream_messages):
            if chunk.content:
                print(chunk.content, end="", flush=True)
        print()  # 换行
        
    except Exception as e:
        print(f"✗ 模型测试失败: {str(e)}")
        return False
    
    return True

def main():
    """主函数"""
    print("=== 硅基流动 Qwen3-8B 模型集成测试 ===\n")
    
    # 打印 LangChain 版本
    print_langchain_version()
    print()
    
    # 列出可用模型
    list_available_models()
    
    # 测试模型
    success = test_qwen_model()
    
    if success:
        print("\n✓ 所有测试完成！")
    else:
        print("\n✗ 测试过程中出现问题，请检查配置。")

if __name__ == "__main__":
    main()