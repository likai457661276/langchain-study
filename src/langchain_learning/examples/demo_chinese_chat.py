#!/usr/bin/env python3
"""
中文聊天助手交互式演示
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
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# 加载环境变量
load_dotenv()

def initialize_siliconflow_model():
    """初始化硅基流动模型"""
    return ChatOpenAI(
        model="Qwen/Qwen3-8B",
        api_key=os.getenv("SILICONFLOW_API_KEY"),
        base_url="https://api.siliconflow.cn/v1",
        temperature=0.7,
        max_tokens=1024
    )

def demo_conversation():
    """演示对话功能"""
    console = Console()
    console.print(Panel.fit("🤖 中文聊天助手演示", style="bold blue"))
    
    # 初始化模型
    try:
        model = initialize_siliconflow_model()
        console.print("[green]✓ 已连接到硅基流动 Qwen3-8B 模型[/green]")
    except Exception as e:
        console.print(f"[red]✗ 模型初始化失败: {e}[/red]")
        console.print("[red]请确保您已在 .env 文件中设置了 SILICONFLOW_API_KEY[/red]")
        return
    
    # 初始化消息历史
    messages = [
        SystemMessage(content="你是一个友好的中文助手，请用中文回答问题，保持简洁和礼貌。")
    ]
    
    # 预设的演示对话
    demo_messages = [
        "你好，请介绍一下你自己",
        "你能帮我写一首关于春天的短诗吗？",
        "请解释一下什么是机器学习"
    ]
    
    console.print("\n[bold green]演示对话开始:[/bold green]\n")
    
    for user_msg in demo_messages:
        # 显示用户消息
        console.print(Panel(
            user_msg,
            title="[bold blue]用户[/bold blue]",
            border_style="blue"
        ))
        
        # 添加用户消息到历史
        messages.append(HumanMessage(content=user_msg))
        
        try:
            # 获取模型响应
            response = model.invoke(messages)
            
            # 添加 AI 响应到历史
            messages.append(response)
            
            # 显示 AI 响应
            console.print(Panel(
                response.content,
                title="[bold green]助手[/bold green]",
                border_style="green"
            ))
        except Exception as e:
            console.print(f"[red]错误: {e}[/red]")
    
    console.print("\n[bold green]演示完成！[/bold green]")
    console.print("\n[yellow]提示: 您可以运行 'simple_chatbot.py' 来进行交互式对话。[/yellow]")

if __name__ == "__main__":
    demo_conversation()