#!/usr/bin/env python3
"""
模型选择演示脚本
展示如何使用不同的模型进行对话
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 导入我们的模型选择函数
sys.path.append(str(Path(__file__).resolve().parent))
from simple_chatbot import list_available_models, initialize_siliconflow_model

console = Console()

def compare_models():
    """
    比较不同模型的响应
    """
    console.print(Panel.fit("🔍 模型比较演示", style="bold blue"))
    
    # 测试问题
    test_question = "请用中文解释什么是机器学习，并给出一个简单的例子。"
    
    models = list_available_models()
    
    # 创建比较表格
    table = Table(title="模型响应比较")
    table.add_column("模型", style="cyan", no_wrap=True)
    table.add_column("响应", style="green")
    
    # 测试每个模型
    for model in models:
        console.print(f"\n[bold]正在测试模型:[/bold] {model['name']}")
        
        try:
            # 初始化模型
            llm = initialize_siliconflow_model(model['id'])
            
            # 发送测试消息
            console.print(f"发送问题: {test_question}")
            
            response = llm.invoke([HumanMessage(content=test_question)])
            
            # 添加到表格
            table.add_row(model['name'], response.content[:200] + "..." if len(response.content) > 200 else response.content)
            
        except Exception as e:
            console.print(f"[red]✗ 错误:[/red] {str(e)}")
            table.add_row(model['name'], f"[red]错误: {str(e)}[/red]")
    
    # 显示比较表格
    console.print("\n")
    console.print(table)
    
    console.print("\n[bold green]演示完成！[/bold green]")

def interactive_model_selection():
    """
    交互式模型选择演示
    """
    console.print(Panel.fit("🤖 交互式模型选择演示", style="bold blue"))
    
    models = list_available_models()
    
    console.print("\n[bold]可用模型:[/bold]")
    for i, model in enumerate(models, 1):
        console.print(f"{i}. {model['name']}")
    
    choice = console.input("\n[bold]选择一个模型进行对话 (1-4):[/bold] ")
    
    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(models):
            selected_model = models[choice_idx]
            console.print(f"\n[green]已选择:[/green] {selected_model['name']}")
            
            # 初始化模型
            llm = initialize_siliconflow_model(selected_model['id'])
            
            # 进行简单对话
            console.print("\n[bold]开始对话 (输入 '退出' 结束):[/bold]")
            
            while True:
                user_input = console.input("\n[bold]你:[/bold] ")
                
                if user_input.lower() in ['退出', 'quit', 'exit']:
                    console.print("[green]再见！[/green]")
                    break
                
                response = llm.invoke([HumanMessage(content=user_input)])
                console.print(f"[bold]{selected_model['name']}:[/bold] {response.content}")
        else:
            console.print("[red]无效选择。[/red]")
    except ValueError:
        console.print("[red]请输入有效的数字。[/red]")

if __name__ == "__main__":
    console.print("选择演示模式:")
    console.print("1. 模型响应比较")
    console.print("2. 交互式模型选择")
    
    mode = console.input("\n[bold]输入选择 (1-2):[/bold] ")
    
    if mode == "1":
        compare_models()
    elif mode == "2":
        interactive_model_selection()
    else:
        console.print("[red]无效选择。[/red]")