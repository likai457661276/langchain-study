"""
中文聊天助手示例 - 基于硅基流动的 LangChain 1.0 应用

此示例展示如何使用 LangChain 1.0 和硅基流动平台创建一个中文聊天助手。
它演示了基本设置、消息处理和中文对话功能。
"""

import os
import sys
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

# 加载环境变量
load_dotenv()

# 初始化 Rich 控制台以美化输出
console = Console()


def initialize_siliconflow_model(model: str = "Qwen/Qwen3-8B"):
    """
    初始化基于硅基流动的聊天模型。
    
    Args:
        model: 要使用的特定模型名称
    
    Returns:
        初始化后的聊天模型
    """
    api_key = os.getenv("SILICONFLOW_API_KEY")
    
    if not api_key:
        raise ValueError("未找到 SILICONFLOW_API_KEY 环境变量，请检查 .env 文件")
    
    # 使用 ChatOpenAI 类连接硅基流动的 API
    # 硅基流动兼容 OpenAI API 格式
    chat_model = ChatOpenAI(
        model=model,
        openai_api_base="https://api.siliconflow.cn/v1",
        openai_api_key=api_key,
        temperature=0.7,
        max_tokens=1024,
        streaming=True,  # 启用流式响应
    )
    
    return chat_model


def list_available_models():
    """
    列出所有可用的模型选项。
    
    Returns:
        包含模型ID和显示名称的字典列表
    """
    return [
        {"id": "Qwen/Qwen3-8B", "name": "通义千问 Qwen3-8B (默认)"},
        {"id": "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B", "name": "DeepSeek-R1-0528-Qwen3-8B"},
        {"id": "THUDM/GLM-Z1-9B-0414", "name": "清华 GLM-Z1-9B-0414"},
        {"id": "THUDM/glm-4-9b-chat", "name": "清华 GLM-4-9B-Chat"}
    ]


def select_model():
    """
    提供模型选择界面。
    
    Returns:
        用户选择的模型ID
    """
    models = list_available_models()
    
    console.print("\n[bold]请选择要使用的模型:[/bold]\n")
    
    for i, model in enumerate(models, 1):
        console.print(f"{i}. {model['name']}")
    
    while True:
        choice = console.input(f"\n[bold]输入您的选择 (1-{len(models)})，或按回车使用默认模型:[/bold] ")
        
        if not choice:
            # 使用默认模型
            console.print(f"[green]已选择默认模型: {models[0]['name']}[/green]")
            return models[0]["id"]
        
        try:
            choice_index = int(choice) - 1
            if 0 <= choice_index < len(models):
                selected_model = models[choice_index]
                console.print(f"[green]已选择: {selected_model['name']}[/green]")
                return selected_model["id"]
            else:
                console.print(f"[red]无效选择，请输入 1 到 {len(models)} 之间的数字[/red]")
        except ValueError:
            console.print("[red]请输入有效的数字[/red]")


def chinese_chat():
    """
    运行一个中文聊天会话。
    """
    console.print(Panel.fit("🤖 中文聊天助手", style="bold blue"))
    
    # 选择模型
    selected_model = select_model()
    
    # 初始化模型
    try:
        model = initialize_siliconflow_model(selected_model)
        console.print(f"[green]✓ 已连接到模型: {selected_model}[/green]")
    except Exception as e:
        console.print(f"[red]✗ 模型初始化失败: {e}[/red]")
        console.print("[red]请确保您已在 .env 文件中设置了 SILICONFLOW_API_KEY[/red]")
        return
    
    # 开始聊天会话
    console.print("\n[bold green]聊天已开始！输入 '退出' 或 'quit' 结束对话。[bold green]\n")
    
    # 初始化消息历史
    messages: List = [
        SystemMessage(content="你是一个友好的中文助手，请用中文回答问题，保持简洁和礼貌。")
    ]
    
    while True:
        # 获取用户输入
        user_input = console.input("[bold blue]你:[/bold blue] ")
        
        if user_input.lower() in ["退出", "quit", "exit", "q"]:
            console.print("[bold green]再见！[bold green]")
            break
        
        # 添加用户消息到历史
        messages.append(HumanMessage(content=user_input))
        
        try:
            # 显示助手正在思考的提示
            console.print("[bold green]助手:[/bold green]", end=" ")
            
            # 流式获取模型响应
            full_response = ""
            for chunk in model.stream(messages):
                if hasattr(chunk, 'content') and chunk.content:
                    console.print(chunk.content, end="")
                    full_response += chunk.content
            
            # 添加完整响应到历史
            messages.append(AIMessage(content=full_response))
            
            # 添加换行符
            console.print()
        except Exception as e:
            console.print(f"\n[red]错误: {e}[/red]")


def message_types_demo():
    """
    演示 LangChain 中的不同消息类型。
    """
    console.print(Panel.fit("📝 消息类型演示", style="bold blue"))
    
    # 选择模型
    selected_model = select_model()
    
    # 初始化模型
    model = initialize_siliconflow_model(selected_model)
    
    # 创建不同类型的消息
    system_msg = SystemMessage(content="你是一个解释概念的助手，请用中文回答。")
    human_msg = HumanMessage(content="LangChain 中有哪些不同类型的消息？")
    ai_msg = AIMessage(content="LangChain 支持多种消息类型，包括 SystemMessage、HumanMessage 和 AIMessage。")
    
    # 使用这些消息创建对话
    messages = [system_msg, human_msg, ai_msg]
    
    # 添加另一个人类消息以继续对话
    messages.append(HumanMessage(content="你能给我展示如何在代码中使用它们吗？"))
    
    # 获取响应
    response = model.invoke(messages)
    
    # 显示对话
    console.print("\n[bold]对话:[bold]\n")
    
    for msg in messages:
        if isinstance(msg, SystemMessage):
            console.print(f"[bold magenta]系统:[/bold magenta] {msg.content}")
        elif isinstance(msg, HumanMessage):
            console.print(f"[bold blue]用户:[/bold blue] {msg.content}")
        elif isinstance(msg, AIMessage):
            console.print(f"[bold green]AI:[/bold green] {msg.content}")
    
    # 显示最终响应
    console.print(f"\n[bold green]AI 响应:[/bold green] {response.content}")


def streaming_demo():
    """
    演示模型的流式响应。
    """
    console.print(Panel.fit("🌊 流式响应演示", style="bold blue"))
    
    # 选择模型
    selected_model = select_model()
    
    # 初始化模型
    model = initialize_siliconflow_model(selected_model)
    
    # 获取用户输入
    prompt = console.input("[bold blue]输入一个用于流式响应的提示:[/bold blue] ")
    
    if not prompt:
        prompt = "给我讲一个关于机器人学习绘画的短故事。"
    
    console.print("\n[bold green]流式响应:[/bold green]\n")
    
    # 流式获取响应
    full_response = ""
    for chunk in model.stream([HumanMessage(content=prompt)]):
        if hasattr(chunk, 'content') and chunk.content:
            console.print(chunk.content, end="")
            full_response += chunk.content
    
    console.print("\n\n[bold]完整响应已接收！[bold]")


def show_models():
    """
    显示所有可用的模型列表。
    """
    console.print(Panel.fit("📋 可用模型列表", style="bold blue"))
    
    models = list_available_models()
    
    console.print("\n[bold]当前支持的模型:[/bold]\n")
    
    for i, model in enumerate(models, 1):
        console.print(f"{i}. [bold cyan]{model['id']}[/bold cyan]")
        console.print(f"   {model['name']}\n")
    
    console.print("[green]提示: 在选择示例时，您可以选择使用任何这些模型。[/green]")


if __name__ == "__main__":
    console.print(Panel.fit("LangChain 1.0 中文聊天助手示例", style="bold blue"))
    
    choice = console.input(
        "\n[bold]选择要运行的示例:[/bold]\n"
        "1. 中文聊天\n"
        "2. 消息类型演示\n"
        "3. 流式响应演示\n"
        "4. 查看可用模型\n"
        "[bold]输入您的选择 (1-4):[/bold] "
    )
    
    if choice == "1":
        chinese_chat()
    elif choice == "2":
        message_types_demo()
    elif choice == "3":
        streaming_demo()
    elif choice == "4":
        show_models()
    else:
        console.print("[red]无效选择。请再次运行脚本。[red]")