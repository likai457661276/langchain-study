"""
带工具的智能体示例 - 高级LangChain 1.0用法

此示例演示如何使用LangChain 1.0创建带有工具的智能体。
它展示了如何定义自定义工具并创建能够使用它们的智能体。
"""

# 导入必要的库
import os
import random
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# LangChain 核心组件
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

# LangChain OpenAI 集成
from langchain_openai import ChatOpenAI

# 简单的内存存储
memory_store = {}

# 获取API密钥
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "")
if not SILICONFLOW_API_KEY:
    raise ValueError("未找到 SILICONFLOW_API_KEY 环境变量，请检查 .env 文件")

@tool
def generate_random_number(min_val: int = 1, max_val: int = 100) -> str:
    """生成一个指定范围内的随机数"""
    num = random.randint(min_val, max_val)
    return f"生成的随机数是: {num}"

@tool
def memory_write(key: str, value: str) -> str:
    """将信息存储到内存中"""
    memory_store[key] = value
    return f"已将信息 '{value}' 存储到键 '{key}'"

@tool
def memory_read(key: str) -> str:
    """从内存中读取信息"""
    if key in memory_store:
        return f"键 '{key}' 的值是: {memory_store[key]}"
    else:
        return f"键 '{key}' 不存在"

@tool
def get_current_time() -> str:
    """获取当前时间"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"当前时间是: {now}"

@tool
def calculator(expression: str) -> str:
    """执行简单的数学计算"""
    try:
        # 安全地评估表达式
        allowed_chars = "0123456789+-*/(). "
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            return f"计算结果: {result}"
        else:
            return "错误: 表达式包含不允许的字符"
    except Exception as e:
        return f"计算错误: {str(e)}"

def create_agent_with_tools():
    """创建带有工具的智能体"""
    # 初始化模型
    llm = ChatOpenAI(
        model="THUDM/GLM-Z1-9B-0414",
        base_url="https://api.siliconflow.cn/v1",
        api_key=SILICONFLOW_API_KEY,  # 直接使用字符串而不是环境变量
        temperature=0.7
    )
    
    # 定义工具列表
    tools = [generate_random_number, memory_write, memory_read, get_current_time, calculator]
    
    # 创建系统提示
    system_prompt = """你是一个有用的AI助手，可以使用以下工具来帮助用户:
    
1. generate_random_number: 生成指定范围内的随机数
2. memory_write: 将信息存储到内存中
3. memory_read: 从内存中读取信息
4. get_current_time: 获取当前时间
5. calculator: 执行简单的数学计算

请根据用户的需求选择合适的工具来帮助他们。如果不需要使用工具，可以直接回答用户的问题。
请用中文回复。"""
    
    # 使用LangChain 1.0的新API创建智能体
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
    
    return agent

def interactive_agent():
    """交互式智能体示例"""
    print("=== 交互式智能体示例 ===")
    print("输入 'quit' 或 'exit' 退出")
    print("可用工具: 生成随机数, 内存读写, 获取时间, 计算器")
    print("-" * 50)
    
    agent = create_agent_with_tools()
    
    while True:
        try:
            user_input = input("\n用户: ")
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见!")
                break
            
            # 使用新的API调用智能体
            inputs = {"messages": [HumanMessage(content=user_input)]}
            result = agent.invoke(inputs)
            
            # 提取AI回复
            if "messages" in result and result["messages"]:
                ai_message = result["messages"][-1]
                if isinstance(ai_message, AIMessage):
                    print(f"助手: {ai_message.content}")
                else:
                    print(f"助手: {ai_message}")
            else:
                print("助手: 抱歉，我没有收到有效的回复。")
                
        except KeyboardInterrupt:
            print("\n\n程序被用户中断，再见!")
            break
        except Exception as e:
            print(f"发生错误: {str(e)}")

def structured_output_demo():
    """结构化输出演示"""
    print("\n=== 结构化输出演示 ===")
    
    # 初始化模型
    llm = ChatOpenAI(
        model="THUDM/GLM-Z1-9B-0414",
        base_url="https://api.siliconflow.cn/v1",
        api_key=SILICONFLOW_API_KEY,  # 直接使用字符串而不是环境变量
        temperature=0.3
    )
    
    # 创建解析器
    parser = JsonOutputParser()
    
    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的数据分析师。请分析用户的输入，并以JSON格式返回分析结果。{format_instructions}。请用中文回复。"),
        ("human", "{input}")
    ])
    
    # 创建链
    chain = prompt | llm | parser
    
    # 示例输入
    test_input = "今天天气很好，我想去公园散步，但是不知道穿什么衣服。"
    
    print(f"输入: {test_input}")
    print("\n分析结果:")
    
    try:
        result = chain.invoke({
            "input": test_input,
            "format_instructions": parser.get_format_instructions()
        })
        print(result)
    except Exception as e:
        print(f"解析错误: {str(e)}")
        # 尝试直接获取模型输出
        raw_output = llm.invoke(f"请分析以下内容并以JSON格式返回: {test_input}")
        print(f"原始输出: {raw_output.content}")

def middleware_demo():
    """中间件演示"""
    print("\n=== 中间件演示 ===")
    print("注意: 在LangChain 1.0中，中间件功能已集成到核心框架中")
    
    # 创建带有工具的智能体
    agent = create_agent_with_tools()
    
    # 示例输入
    test_input = "请记住我最喜欢的颜色是蓝色，然后生成一个1到10之间的随机数。"
    
    print(f"输入: {test_input}")
    print("\n处理过程:")
    
    try:
        # 使用流式输出展示处理过程
        inputs = {"messages": [HumanMessage(content=test_input)]}
        for chunk in agent.stream(inputs, stream_mode="updates"):
            print(f"更新: {chunk}")
        
        # 获取最终结果
        result = agent.invoke(inputs)
        if "messages" in result and result["messages"]:
            ai_message = result["messages"][-1]
            if isinstance(ai_message, AIMessage):
                print(f"\n最终回复: {ai_message.content}")
            else:
                print(f"\n最终回复: {ai_message}")
    except Exception as e:
        print(f"处理错误: {str(e)}")

def main():
    """主函数"""
    print("LangChain 1.0 智能体示例")
    print("=" * 50)
    print("1. 交互式智能体")
    print("2. 结构化输出演示")
    print("3. 中间件演示")
    print("=" * 50)
    
    choice = input("请选择示例 (1-3): ")
    
    if choice == "1":
        interactive_agent()
    elif choice == "2":
        structured_output_demo()
    elif choice == "3":
        middleware_demo()
    else:
        print("无效选择。请重新运行脚本。")

if __name__ == "__main__":
    main()