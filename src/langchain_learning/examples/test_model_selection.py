#!/usr/bin/env python3
"""
测试模型选择功能
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
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 导入我们的模型选择函数
sys.path.append(str(Path(__file__).resolve().parent))
from simple_chatbot import list_available_models, initialize_siliconflow_model

console = Console()

def test_model_selection():
    """
    测试模型选择功能
    """
    console.print(Panel.fit("🧪 模型选择测试", style="bold blue"))
    
    models = list_available_models()
    
    # 测试每个模型
    for i, model in enumerate(models, 1):
        console.print(f"\n[bold]测试模型 {i}/{len(models)}: {model['name']}[/bold]")
        
        try:
            # 初始化模型
            llm = initialize_siliconflow_model(model['id'])
            
            # 发送简单测试消息
            test_message = "你好，请用一句话介绍你自己。"
            console.print(f"发送消息: {test_message}")
            
            response = llm.invoke([HumanMessage(content=test_message)])
            console.print(f"[green]✓ 响应成功:[/green] {response.content[:100]}...")
            
        except Exception as e:
            console.print(f"[red]✗ 错误:[/red] {str(e)}")
    
    console.print("\n[bold green]测试完成！[/bold green]")

if __name__ == "__main__":
    test_model_selection()