"""
内存管理示例 - LangChain 1.0 内存功能

本示例演示如何在LangChain 1.0中使用内存功能。
它展示了如何使用LangGraph的内存存储来存储、检索和搜索内存。
"""

import os
from typing import List, Dict, Any
import json
from datetime import datetime

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.embeddings import init_embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.store.memory import InMemoryStore
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

# 加载环境变量
load_dotenv()

# 初始化rich控制台用于美化输出
console = Console()


def setup_memory_store():
    """
    设置一个内存存储用于演示。
    在生产环境中，您将使用持久化存储。
    """
    # 初始化嵌入
    embeddings = OpenAIEmbeddings(
        model="BAAI/bge-large-zh-v1.5",
        base_url="https://api.siliconflow.cn/v1",
        api_key=os.getenv("SILICONFLOW_API_KEY")
    )
    
    # 创建带有嵌入的内存存储
    # 注意：在实际应用中，您将使用适当的嵌入函数
    # 对于此演示，我们将使用简单的模拟嵌入函数
    def embed(texts: List[str]) -> List[List[float]]:
        # 模拟嵌入函数 - 在生产环境中使用真实嵌入
        return [[hash(text) % 1000 / 1000.0 for _ in range(10)] for text in texts]
    
    store = InMemoryStore(index={"embed": embed, "dims": 10})
    return store


def basic_memory_operations():
    """
    演示基本内存操作：put、get、search。
    """
    console.print(Panel.fit("💾 基本内存操作", style="bold blue"))
    
    # 设置内存存储
    store = setup_memory_store()
    console.print("[green]✓ 内存存储已初始化[/green]")
    
    # 定义用户内存的命名空间
    user_id = "demo_user"
    namespace = (user_id, "memories")
    
    # 存储一些内存
    memories = [
        {
            "key": "preference",
            "value": {"preference": "用户更喜欢简洁的答案和技术细节。"}
        },
        {
            "key": "project",
            "value": {"project": "用户正在做一个LangChain学习项目。"}
        },
        {
            "key": "expertise",
            "value": {"expertise": "用户具有中级Python知识，对LangChain还不熟悉。"}
        }
    ]
    
    console.print("\n[bold]存储内存:[/bold]")
    for memory in memories:
        store.put(namespace, memory["key"], memory["value"])
        console.print(f"  ✓ 已存储 {memory['key']}: {memory['value']}")
    
    # 检索特定内存
    console.print("\n[bold]检索特定内存:[/bold]")
    retrieved = store.get(namespace, "preference")
    if retrieved:
        console.print(f"  检索到的偏好: {retrieved.value}")
    
    # 搜索内存
    console.print("\n[bold]搜索内存:[/bold]")
    search_results = store.search(namespace, query="用户知识")
    console.print(f"  找到 {len(search_results)} 个匹配'用户知识'的内存:")
    for result in search_results:
        console.print(f"    - {result.key}: {result.value}")
    
    # 列出命名空间中的所有内存
    console.print("\n[bold]命名空间中的所有内存:[/bold]")
    all_items = store.search(namespace)
    for item in all_items:
        console.print(f"    - {item.key}: {item.value}")


def conversation_memory_demo():
    """
    演示如何在对话上下文中使用内存。
    """
    console.print(Panel.fit("💬 对话内存演示", style="bold blue"))
    
    # 初始化模型和内存存储
    model = init_chat_model("gpt-4o-mini", model_provider="openai")
    store = setup_memory_store()
    
    # 定义对话内存的命名空间
    user_id = "demo_user"
    namespace = (user_id, "conversation")
    
    # 存储对话上下文
    conversation_context = {
        "topic": "LangChain学习",
        "user_goals": "了解如何使用LangChain 1.0构建AI应用程序",
        "previous_discussions": [
            "用户询问了基本聊天设置",
            "用户询问了代理和工具",
            "用户想了解内存管理"
        ]
    }
    
    store.put(namespace, "context", conversation_context)
    
    console.print("[green]✓ 对话上下文已存储[/green]")
    
    # 模拟带有内存的对话
    console.print("\n[bold]模拟带有内存的对话:[/bold]\n")
    
    # 第一条消息
    user_message = "你能帮我理解LangChain的内存功能吗？"
    
    # 在响应前检索相关内存
    memories = store.search(namespace, query="内存功能")
    
    # 格式化内存用于上下文
    memory_context = "\n".join([f"- {item.key}: {item.value}" for item in memories])
    
    # 创建带有内存上下文的提示
    system_prompt = f"""你是一个学习LangChain的得力助手。
    
    之前的对话上下文:
    {memory_context}
    
    使用此上下文提供个性化响应。
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    
    # 获取模型响应
    response = model.invoke(messages)
    
    console.print(f"[bold blue]用户:[/bold blue] {user_message}")
    console.print(f"[bold green]助手:[/bold green] {response.content}")
    
    # 将此交互存储在内存中
    interaction = {
        "timestamp": datetime.now().isoformat(),
        "user_message": user_message,
        "assistant_response": response.content
    }
    
    store.put(namespace, f"interaction_{datetime.now().strftime('%Y%m%d_%H%M%S')}", interaction)
    console.print("[green]✓ 交互已存储在内存中[/green]")


def vector_memory_demo():
    """
    演示基于向量的内存存储和检索。
    """
    console.print(Panel.fit("🔍 向量内存演示", style="bold blue"))
    
    # 初始化嵌入
    embeddings = OpenAIEmbeddings(
        model="BAAI/bge-large-zh-v1.5",
        base_url="https://api.siliconflow.cn/v1",
        api_key=os.getenv("SILICONFLOW_API_KEY")
    )
    
    # 使用Chroma创建简单的向量存储
    vector_store = Chroma(
        collection_name="langchain_memories",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db"
    )
    
    console.print("[green]✓ 向量存储已初始化[/green]")
    
    # 向向量存储添加一些文档
    documents = [
        "LangChain是一个用于构建由大型语言模型驱动的应用程序的框架。",
        "LangChain中的代理可以使用工具执行操作和收集信息。",
        "LangChain中的内存允许应用程序记住之前的交互。",
        "LangChain 1.0引入了create_agent函数，使代理创建更容易。",
        "LangGraph提供了一个用于构建代理的低级编排框架。"
    ]
    
    # 添加带有ID的文档
    ids = [f"doc_{i}" for i in range(len(documents))]
    vector_store.add_texts(texts=documents, ids=ids)
    
    console.print(f"[green]✓ 已向向量存储添加 {len(documents)} 个文档[/green]")
    
    # 搜索相似文档
    query = "如何在LangChain中创建代理？"
    console.print(f"\n[bold]搜索与以下内容相似的文档:[/bold] {query}")
    
    results = vector_store.similarity_search_with_score(query, k=3)
    
    console.print(f"\n[bold]找到 {len(results)} 个相似文档:[/bold]\n")
    for i, (doc, score) in enumerate(results):
        console.print(f"[bold]结果 {i+1}[/bold] (得分: {score:.4f}):")
        console.print(f"  {doc.page_content}\n")


def long_term_memory_demo():
    """
    演示使用用户档案的长期内存管理。
    """
    console.print(Panel.fit("🧠 长期内存演示", style="bold blue"))
    
    # 初始化模型和内存存储
    model = init_chat_model("gpt-4o-mini", model_provider="openai")
    store = setup_memory_store()
    
    # 创建用户档案
    user_id = "demo_user"
    profile_namespace = (user_id, "profile")
    memories_namespace = (user_id, "memories")
    
    # 存储用户档案
    profile = {
        "name": "演示用户",
        "preferences": {
            "response_style": "简洁",
            "technical_level": "中级",
            "interests": ["AI", "Python", "LangChain"]
        },
        "learning_goals": [
            "理解LangChain基础知识",
            "构建AI应用程序",
            "了解代理和工具"
        ],
        "last_interaction": datetime.now().isoformat()
    }
    
    store.put(profile_namespace, "user_profile", profile)
    console.print("[green]✓ 用户档案已存储[/green]")
    
    # 存储一些特定的内存
    memories = [
        {"key": "question_1", "value": {"question": "什么是LangChain？", "answer": "一个用于LLM应用程序的框架"}},
        {"key": "question_2", "value": {"question": "如何创建代理？", "answer": "使用create_agent函数"}},
        {"key": "question_3", "value": {"question": "有哪些工具可用？", "answer": "各种用于网络搜索、计算等的工具"}}
    ]
    
    for memory in memories:
        store.put(memories_namespace, memory["key"], memory["value"])
    
    console.print(f"[green]✓ 已存储 {len(memories)} 个问答内存[/green]")
    
    # 检索用户档案
    user_profile = store.get(profile_namespace, "user_profile")
    console.print("\n[bold]用户档案:[/bold]")
    console.print(f"  姓名: {user_profile.value['name']}")
    console.print(f"  响应风格: {user_profile.value['preferences']['response_style']}")
    console.print(f"  技术水平: {user_profile.value['preferences']['technical_level']}")
    console.print(f"  兴趣: {', '.join(user_profile.value['preferences']['interests'])}")
    
    # 根据查询搜索相关内存
    query = "代理创建"
    console.print(f"\n[bold]搜索内存:[/bold] {query}")
    
    relevant_memories = store.search(memories_namespace, query=query)
    console.print(f"[bold]找到 {len(relevant_memories)} 个相关内存:[/bold]")
    
    for memory in relevant_memories:
        console.print(f"  - {memory.value['question']}: {memory.value['answer']}")
    
    # 模拟基于档案和内存的个性化响应
    console.print("\n[bold]模拟个性化响应:[/bold]\n")
    
    # 获取相关内存
    memories_context = "\n".join([
        f"- {mem.value['question']}: {mem.value['answer']}" 
        for mem in relevant_memories
    ])
    
    # 创建个性化提示
    system_prompt = f"""你是 {user_profile.value['name']} 的得力助手。
    
    用户档案:
    - 响应风格: {user_profile.value['preferences']['response_style']}
    - 技术水平: {user_profile.value['preferences']['technical_level']}
    - 兴趣: {', '.join(user_profile.value['preferences']['interests'])}
    
    之前的问答:
    {memories_context}
    
    提供符合用户偏好并基于其之前知识的响应。
    """
    
    user_question = "你能详细解释一下LangChain中的代理创建吗？"
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_question)
    ]
    
    response = model.invoke(messages)
    
    console.print(f"[bold blue]用户:[/bold blue] {user_question}")
    console.print(f"[bold green]助手:[/bold green] {response.content}")
    
    # 更新最后交互时间
    profile["last_interaction"] = datetime.now().isoformat()
    store.put(profile_namespace, "user_profile", profile)
    console.print("[green]✓ 已更新最后交互时间[/green]")


if __name__ == "__main__":
    console.print(Panel.fit("LangChain 1.0 内存管理示例", style="bold blue"))
    
    choice = console.input(
        "\n[bold]选择要运行的示例:[/bold]\n"
        "1. 基本内存操作\n"
        "2. 对话内存演示\n"
        "3. 向量内存演示\n"
        "4. 长期内存演示\n"
        "[bold]输入您的选择 (1-4):[/bold] "
    )
    
    if choice == "1":
        basic_memory_operations()
    elif choice == "2":
        conversation_memory_demo()
    elif choice == "3":
        vector_memory_demo()
    elif choice == "4":
        long_term_memory_demo()
    else:
        console.print("[red]无效选择。请再次运行脚本。[/red]")