"""
高级智能体示例 - LangChain 1.0高级功能

此示例演示了LangChain 1.0的更多高级功能，包括：
1. 记忆管理
2. 工具链组合
3. 条件路由
4. 错误处理
5. 流式处理
"""

import os
import random
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# LangChain 核心组件
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableBranch
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory

# LangChain OpenAI 集成
from langchain_openai import ChatOpenAI

# 获取API密钥
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "")
if not SILICONFLOW_API_KEY:
    raise ValueError("未找到 SILICONFLOW_API_KEY 环境变量，请检查 .env 文件")

# 高级工具定义
@tool
def weather_search(location: str) -> str:
    """模拟天气搜索工具"""
    # 模拟不同城市的天气数据
    weather_data = {
        "北京": {"温度": "15°C", "天气": "晴朗", "湿度": "45%", "风速": "5km/h"},
        "上海": {"温度": "18°C", "天气": "多云", "湿度": "60%", "风速": "8km/h"},
        "广州": {"温度": "25°C", "天气": "小雨", "湿度": "80%", "风速": "3km/h"},
        "深圳": {"温度": "24°C", "天气": "阴天", "湿度": "75%", "风速": "6km/h"},
        "成都": {"温度": "20°C", "天气": "雾霾", "湿度": "70%", "风速": "2km/h"},
    }
    
    if location in weather_data:
        data = weather_data[location]
        return f"{location}当前天气: 温度{data['温度']}, {data['天气']}, 湿度{data['湿度']}, 风速{data['风速']}"
    else:
        # 为未知城市生成随机天气数据
        temp = random.randint(10, 30)
        conditions = ["晴朗", "多云", "阴天", "小雨", "大雨", "雪"]
        condition = random.choice(conditions)
        humidity = random.randint(30, 90)
        wind = random.randint(1, 15)
        return f"{location}当前天气: 温度{temp}°C, {condition}, 湿度{humidity}%, 风速{wind}km/h"

@tool
def news_search(topic: str) -> str:
    """模拟新闻搜索工具"""
    news_templates = [
        f"最新报道: 关于{topic}的研究取得重大突破",
        f"今日头条: {topic}相关产业迎来新发展机遇",
        f"专家观点: {topic}的未来发展趋势分析",
        f"市场动态: {topic}领域投资价值评估",
        f"国际视野: 全球{topic}发展现状对比"
    ]
    return random.choice(news_templates)

@tool
def data_analysis(data: str) -> str:
    """数据分析工具"""
    try:
        # 尝试解析JSON数据
        if data.startswith('{') or data.startswith('['):
            parsed_data = json.loads(data)
            return f"数据分析结果: 已解析JSON数据，包含{len(parsed_data)}个元素"
        else:
            # 简单文本分析
            char_count = len(data)
            word_count = len(data.split())
            return f"文本分析结果: 字符数{char_count}, 单词数{word_count}"
    except json.JSONDecodeError:
        return f"数据分析结果: 无法解析为JSON，但包含{len(data)}个字符"

@tool
def task_scheduler(task: str, priority: str = "medium") -> str:
    """任务调度工具"""
    priorities = ["high", "medium", "low"]
    if priority not in priorities:
        priority = "medium"
    
    # 模拟任务ID生成
    task_id = f"TASK-{random.randint(1000, 9999)}"
    
    # 模拟任务调度
    scheduled_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"任务已调度: ID={task_id}, 任务={task}, 优先级={priority}, 调度时间={scheduled_time}"

# 自定义记忆类
class SimpleMemory:
    """简单的记忆实现"""
    
    def __init__(self):
        self.chat_history = InMemoryChatMessageHistory()
    
    def get_history(self):
        """获取聊天历史"""
        return self.chat_history.messages
    
    def add_user_message(self, message: str):
        """添加用户消息"""
        self.chat_history.add_user_message(message)
    
    def add_ai_message(self, message: str):
        """添加AI消息"""
        self.chat_history.add_ai_message(message)
    
    def clear(self):
        """清空记忆"""
        self.chat_history.clear()

# 创建带有记忆的智能体
def create_memory_agent():
    """创建带有记忆功能的智能体"""
    # 初始化模型
    llm = ChatOpenAI(
        model="THUDM/GLM-Z1-9B-0414",
        base_url="https://api.siliconflow.cn/v1",
        api_key=SILICONFLOW_API_KEY,
        temperature=0.7
    )
    
    # 定义工具列表
    tools = [weather_search, news_search, data_analysis, task_scheduler]
    
    # 创建系统提示
    system_prompt = """你是一个高级AI助手，具有记忆能力和多种工具。你可以:

1. 使用weather_search查询天气信息
2. 使用news_search搜索新闻
3. 使用data_analysis分析数据
4. 使用task_scheduler调度任务

你具有记忆功能，可以记住之前的对话内容。请根据用户的需求选择合适的工具来帮助他们。
请用中文回复。"""
    
    # 使用LangChain 1.0的新API创建智能体
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )
    
    # 创建记忆实例
    memory = SimpleMemory()
    
    return agent, memory

# 创建条件路由智能体
def create_conditional_agent():
    """创建带有条件路由的智能体"""
    # 初始化模型
    llm = ChatOpenAI(
        model="THUDM/GLM-Z1-9B-0414",
        base_url="https://api.siliconflow.cn/v1",
        api_key=SILICONFLOW_API_KEY,
        temperature=0.3
    )
    
    # 创建意图分类提示
    intent_prompt = ChatPromptTemplate.from_template("""
    分析用户输入的意图，并分类为以下之一:
    - "weather": 天气查询
    - "news": 新闻搜索
    - "data": 数据分析
    - "task": 任务调度
    - "general": 一般对话
    
    用户输入: {input}
    
    只返回分类结果，不要添加其他内容:
    """)
    
    # 创建意图分类链
    intent_chain = intent_prompt | llm | StrOutputParser()
    
    # 创建不同意图的处理链
    weather_chain = ChatPromptTemplate.from_template("你是一个天气助手，请回答关于天气的问题: {input}") | llm | StrOutputParser()
    news_chain = ChatPromptTemplate.from_template("你是一个新闻助手，请回答关于新闻的问题: {input}") | llm | StrOutputParser()
    data_chain = ChatPromptTemplate.from_template("你是一个数据分析助手，请回答关于数据分析的问题: {input}") | llm | StrOutputParser()
    task_chain = ChatPromptTemplate.from_template("你是一个任务管理助手，请回答关于任务调度的问题: {input}") | llm | StrOutputParser()
    general_chain = ChatPromptTemplate.from_template("你是一个通用助手，请回答用户的问题: {input}") | llm | StrOutputParser()
    
    # 创建条件路由
    chain = RunnableBranch(
        (lambda x: "weather" in x["intent"], weather_chain),
        (lambda x: "news" in x["intent"], news_chain),
        (lambda x: "data" in x["intent"], data_chain),
        (lambda x: "task" in x["intent"], task_chain),
        general_chain,
    )
    
    # 组合链
    full_chain = {
        "intent": intent_chain,
        "input": lambda x: x["input"]
    } | chain
    
    return full_chain

# 创建工具链组合示例
def create_tool_chain():
    """创建工具链组合示例"""
    # 初始化模型
    llm = ChatOpenAI(
        model="THUDM/GLM-Z1-9B-0414",
        base_url="https://api.siliconflow.cn/v1",
        api_key=SILICONFLOW_API_KEY,
        temperature=0.5
    )
    
    # 创建数据处理链
    process_chain = (
        RunnableLambda(lambda x: {"input": x})
        | RunnablePassthrough.assign(
            processed=RunnableLambda(lambda x: data_analysis.invoke({"data": x["input"]}))
        )
    )
    
    # 创建总结链
    summary_prompt = ChatPromptTemplate.from_template("""
    基于以下信息和数据处理结果，请提供一个简洁的总结:
    
    原始输入: {input}
    数据处理结果: {processed}
    
    总结:
    """)
    
    summary_chain = summary_prompt | llm | StrOutputParser()
    
    # 组合链
    full_chain = process_chain | summary_chain
    
    return full_chain

# 记忆智能体演示
def memory_agent_demo():
    """记忆智能体演示"""
    print("\n=== 记忆智能体演示 ===")
    print("这个演示展示了带有记忆功能的智能体")
    print("输入 'quit' 或 'exit' 退出")
    print("-" * 50)
    
    agent, memory = create_memory_agent()
    
    while True:
        try:
            user_input = input("\n用户: ")
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("再见!")
                break
            
            # 使用智能体处理输入
            inputs = {"messages": [HumanMessage(content=user_input)]}
            result = agent.invoke(inputs)
            
            # 提取AI回复
            if "messages" in result and result["messages"]:
                ai_message = result["messages"][-1]
                if isinstance(ai_message, AIMessage):
                    print(f"助手: {ai_message.content}")
                    # 保存到记忆中
                    memory.add_user_message(user_input)
                    memory.add_ai_message(ai_message.content)
                else:
                    print(f"助手: {ai_message}")
            else:
                print("助手: 抱歉，我没有收到有效的回复。")
                
        except KeyboardInterrupt:
            print("\n\n程序被用户中断，再见!")
            break
        except Exception as e:
            print(f"发生错误: {str(e)}")

# 条件路由智能体演示
def conditional_agent_demo():
    """条件路由智能体演示"""
    print("\n=== 条件路由智能体演示 ===")
    print("这个演示展示了基于意图的条件路由功能")
    print("-" * 50)
    
    chain = create_conditional_agent()
    
    # 示例输入
    test_inputs = [
        "北京今天天气怎么样?",
        "最近有什么科技新闻?",
        "请分析这段数据: {'sales': [100, 200, 150], 'profit': [10, 20, 15]}",
        "帮我安排一个明天上午的会议",
        "你好，请介绍一下你自己"
    ]
    
    for test_input in test_inputs:
        print(f"\n用户: {test_input}")
        try:
            result = chain.invoke({"input": test_input})
            print(f"助手: {result}")
        except Exception as e:
            print(f"错误: {str(e)}")
        print("-" * 30)

# 工具链组合演示
def tool_chain_demo():
    """工具链组合演示"""
    print("\n=== 工具链组合演示 ===")
    print("这个演示展示了如何组合多个工具形成处理链")
    print("-" * 50)
    
    chain = create_tool_chain()
    
    # 示例输入
    test_input = "请分析这组销售数据: 产品A:100件, 产品B:200件, 产品C:150件"
    
    print(f"输入: {test_input}")
    print("\n处理结果:")
    
    try:
        result = chain.invoke(test_input)
        print(result)
    except Exception as e:
        print(f"错误: {str(e)}")

# 流式处理演示
def streaming_demo():
    """流式处理演示"""
    print("\n=== 流式处理演示 ===")
    print("这个演示展示了流式处理功能")
    print("-" * 50)
    
    # 创建智能体
    agent, _ = create_memory_agent()
    
    # 示例输入
    test_input = "请帮我查询北京的天气，然后安排一个明天下午的任务"
    
    print(f"输入: {test_input}")
    print("\n流式输出:")
    
    try:
        inputs = {"messages": [HumanMessage(content=test_input)]}
        # 使用流式输出
        for chunk in agent.stream(inputs):
            if "messages" in chunk and chunk["messages"]:
                latest_message = chunk["messages"][-1]
                if hasattr(latest_message, "content") and latest_message.content:
                    print(latest_message.content, end="", flush=True)
        print()  # 换行
    except Exception as e:
        print(f"错误: {str(e)}")

# 错误处理演示
def error_handling_demo():
    """错误处理演示"""
    print("\n=== 错误处理演示 ===")
    print("这个演示展示了如何处理智能体运行中的错误")
    print("-" * 50)
    
    # 创建智能体
    agent, _ = create_memory_agent()
    
    # 示例输入（包含可能导致错误的内容）
    test_inputs = [
        "请分析这段无效的JSON数据: {invalid json}",
        "请查询一个不存在的城市的天气: 不存在的城市",
        "正常查询: 北京的天气怎么样?"
    ]
    
    for test_input in test_inputs:
        print(f"\n输入: {test_input}")
        try:
            inputs = {"messages": [HumanMessage(content=test_input)]}
            result = agent.invoke(inputs)
            
            if "messages" in result and result["messages"]:
                ai_message = result["messages"][-1]
                if isinstance(ai_message, AIMessage):
                    print(f"助手: {ai_message.content}")
                else:
                    print(f"助手: {ai_message}")
            else:
                print("助手: 抱歉，我没有收到有效的回复。")
        except Exception as e:
            print(f"错误处理: {str(e)}")
        print("-" * 30)

def main():
    """主函数"""
    print("LangChain 1.0 高级智能体示例")
    print("=" * 50)
    print("1. 记忆智能体演示")
    print("2. 条件路由智能体演示")
    print("3. 工具链组合演示")
    print("4. 流式处理演示")
    print("5. 错误处理演示")
    print("=" * 50)
    
    choice = input("请选择演示 (1-5): ")
    
    if choice == "1":
        memory_agent_demo()
    elif choice == "2":
        conditional_agent_demo()
    elif choice == "3":
        tool_chain_demo()
    elif choice == "4":
        streaming_demo()
    elif choice == "5":
        error_handling_demo()
    else:
        print("无效选择。请重新运行脚本。")

if __name__ == "__main__":
    main()