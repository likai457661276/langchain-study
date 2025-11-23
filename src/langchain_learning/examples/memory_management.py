"""
Memory Management Example - LangChain 1.0 Memory Features

This example demonstrates how to use memory features in LangChain 1.0.
It shows how to store, retrieve, and search memories using LangGraph's memory store.
"""

import os
from typing import List, Dict, Any
import json
from datetime import datetime

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.embeddings import init_embeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.store.memory import InMemoryStore
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

# Load environment variables
load_dotenv()

# Initialize rich console for pretty output
console = Console()


def setup_memory_store():
    """
    Set up an in-memory store for demonstration.
    In a production environment, you would use a persistent store.
    """
    # Initialize embeddings
    embeddings = init_embeddings("openai")
    
    # Create in-memory store with embeddings
    # Note: In a real application, you would use a proper embedding function
    # For this demo, we'll use a simple mock embedding function
    def embed(texts: List[str]) -> List[List[float]]:
        # Mock embedding function - in production, use real embeddings
        return [[hash(text) % 1000 / 1000.0 for _ in range(10)] for text in texts]
    
    store = InMemoryStore(index={"embed": embed, "dims": 10})
    return store


def basic_memory_operations():
    """
    Demonstrate basic memory operations: put, get, search.
    """
    console.print(Panel.fit("💾 Basic Memory Operations", style="bold blue"))
    
    # Set up memory store
    store = setup_memory_store()
    console.print("[green]✓ Memory store initialized[/green]")
    
    # Define namespace for user memories
    user_id = "demo_user"
    namespace = (user_id, "memories")
    
    # Store some memories
    memories = [
        {
            "key": "preference",
            "value": {"preference": "User prefers concise answers and technical details."}
        },
        {
            "key": "project",
            "value": {"project": "User is working on a LangChain learning project."}
        },
        {
            "key": "expertise",
            "value": {"expertise": "User has intermediate Python knowledge and is new to LangChain."}
        }
    ]
    
    console.print("\n[bold]Storing memories:[/bold]")
    for memory in memories:
        store.put(namespace, memory["key"], memory["value"])
        console.print(f"  ✓ Stored {memory['key']}: {memory['value']}")
    
    # Retrieve a specific memory
    console.print("\n[bold]Retrieving specific memory:[/bold]")
    retrieved = store.get(namespace, "preference")
    if retrieved:
        console.print(f"  Retrieved preference: {retrieved.value}")
    
    # Search memories
    console.print("\n[bold]Searching memories:[/bold]")
    search_results = store.search(namespace, query="user knowledge")
    console.print(f"  Found {len(search_results)} memories matching 'user knowledge':")
    for result in search_results:
        console.print(f"    - {result.key}: {result.value}")
    
    # List all memories in namespace
    console.print("\n[bold]All memories in namespace:[/bold]")
    all_items = store.search(namespace)
    for item in all_items:
        console.print(f"    - {item.key}: {item.value}")


def conversation_memory_demo():
    """
    Demonstrate how to use memory in a conversation context.
    """
    console.print(Panel.fit("💬 Conversation Memory Demo", style="bold blue"))
    
    # Initialize model and memory store
    model = init_chat_model("gpt-4o-mini", model_provider="openai")
    store = setup_memory_store()
    
    # Define namespace for conversation memories
    user_id = "demo_user"
    namespace = (user_id, "conversation")
    
    # Store conversation context
    conversation_context = {
        "topic": "LangChain learning",
        "user_goals": "Understand how to use LangChain 1.0 for building AI applications",
        "previous_discussions": [
            "User asked about basic chat setup",
            "User inquired about agents and tools",
            "User wanted to know about memory management"
        ]
    }
    
    store.put(namespace, "context", conversation_context)
    
    console.print("[green]✓ Conversation context stored[/green]")
    
    # Simulate a conversation with memory
    console.print("\n[bold]Simulating conversation with memory:[/bold]\n")
    
    # First message
    user_message = "Can you help me understand LangChain's memory features?"
    
    # Retrieve relevant memories before responding
    memories = store.search(namespace, query="memory features")
    
    # Format memories for context
    memory_context = "\n".join([f"- {item.key}: {item.value}" for item in memories])
    
    # Create a prompt with memory context
    system_prompt = f"""You are a helpful assistant for learning LangChain.
    
    Previous conversation context:
    {memory_context}
    
    Use this context to provide a personalized response.
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    
    # Get model response
    response = model.invoke(messages)
    
    console.print(f"[bold blue]User:[/bold blue] {user_message}")
    console.print(f"[bold green]Assistant:[/bold green] {response.content}")
    
    # Store this interaction in memory
    interaction = {
        "timestamp": datetime.now().isoformat(),
        "user_message": user_message,
        "assistant_response": response.content
    }
    
    store.put(namespace, f"interaction_{datetime.now().strftime('%Y%m%d_%H%M%S')}", interaction)
    console.print("[green]✓ Interaction stored in memory[/green]")


def vector_memory_demo():
    """
    Demonstrate vector-based memory storage and retrieval.
    """
    console.print(Panel.fit("🔍 Vector Memory Demo", style="bold blue"))
    
    # Initialize embeddings
    embeddings = init_embeddings("openai")
    
    # Create a simple vector store using Chroma
    vector_store = Chroma(
        collection_name="langchain_memories",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db"
    )
    
    console.print("[green]✓ Vector store initialized[/green]")
    
    # Add some documents to the vector store
    documents = [
        "LangChain is a framework for building applications powered by large language models.",
        "Agents in LangChain can use tools to perform actions and gather information.",
        "Memory in LangChain allows applications to remember previous interactions.",
        "LangChain 1.0 introduced the create_agent function for easier agent creation.",
        "LangGraph provides a low-level orchestration framework for building agents."
    ]
    
    # Add documents with IDs
    ids = [f"doc_{i}" for i in range(len(documents))]
    vector_store.add_texts(texts=documents, ids=ids)
    
    console.print(f"[green]✓ Added {len(documents)} documents to vector store[/green]")
    
    # Search for similar documents
    query = "How to create agents in LangChain?"
    console.print(f"\n[bold]Searching for documents similar to:[/bold] {query}")
    
    results = vector_store.similarity_search_with_score(query, k=3)
    
    console.print(f"\n[bold]Found {len(results)} similar documents:[/bold]\n")
    for i, (doc, score) in enumerate(results):
        console.print(f"[bold]Result {i+1}[/bold] (Score: {score:.4f}):")
        console.print(f"  {doc.page_content}\n")


def long_term_memory_demo():
    """
    Demonstrate long-term memory management with user profiles.
    """
    console.print(Panel.fit("🧠 Long-term Memory Demo", style="bold blue"))
    
    # Initialize model and memory store
    model = init_chat_model("gpt-4o-mini", model_provider="openai")
    store = setup_memory_store()
    
    # Create a user profile
    user_id = "demo_user"
    profile_namespace = (user_id, "profile")
    memories_namespace = (user_id, "memories")
    
    # Store user profile
    profile = {
        "name": "Demo User",
        "preferences": {
            "response_style": "concise",
            "technical_level": "intermediate",
            "interests": ["AI", "Python", "LangChain"]
        },
        "learning_goals": [
            "Understand LangChain basics",
            "Build an AI application",
            "Learn about agents and tools"
        ],
        "last_interaction": datetime.now().isoformat()
    }
    
    store.put(profile_namespace, "user_profile", profile)
    console.print("[green]✓ User profile stored[/green]")
    
    # Store some specific memories
    memories = [
        {"key": "question_1", "value": {"question": "What is LangChain?", "answer": "A framework for LLM applications"}},
        {"key": "question_2", "value": {"question": "How do I create an agent?", "answer": "Use the create_agent function"}},
        {"key": "question_3", "value": {"question": "What tools are available?", "answer": "Various tools for web search, calculations, etc."}}
    ]
    
    for memory in memories:
        store.put(memories_namespace, memory["key"], memory["value"])
    
    console.print(f"[green]✓ Stored {len(memories)} Q&A memories[/green]")
    
    # Retrieve user profile
    user_profile = store.get(profile_namespace, "user_profile")
    console.print("\n[bold]User Profile:[/bold]")
    console.print(f"  Name: {user_profile.value['name']}")
    console.print(f"  Response Style: {user_profile.value['preferences']['response_style']}")
    console.print(f"  Technical Level: {user_profile.value['preferences']['technical_level']}")
    console.print(f"  Interests: {', '.join(user_profile.value['preferences']['interests'])}")
    
    # Search for relevant memories based on a query
    query = "agent creation"
    console.print(f"\n[bold]Searching memories for:[/bold] {query}")
    
    relevant_memories = store.search(memories_namespace, query=query)
    console.print(f"[bold]Found {len(relevant_memories)} relevant memories:[/bold]")
    
    for memory in relevant_memories:
        console.print(f"  - {memory.value['question']}: {memory.value['answer']}")
    
    # Simulate a personalized response based on profile and memories
    console.print("\n[bold]Simulating personalized response:[/bold]\n")
    
    # Get relevant memories
    memories_context = "\n".join([
        f"- {mem.value['question']}: {mem.value['answer']}" 
        for mem in relevant_memories
    ])
    
    # Create personalized prompt
    system_prompt = f"""You are a helpful assistant for {user_profile.value['name']}.
    
    User Profile:
    - Response Style: {user_profile.value['preferences']['response_style']}
    - Technical Level: {user_profile.value['preferences']['technical_level']}
    - Interests: {', '.join(user_profile.value['preferences']['interests'])}
    
    Previous Q&A:
    {memories_context}
    
    Provide a response that matches the user's preferences and builds on their previous knowledge.
    """
    
    user_question = "Can you explain more about agent creation in LangChain?"
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_question)
    ]
    
    response = model.invoke(messages)
    
    console.print(f"[bold blue]User:[/bold blue] {user_question}")
    console.print(f"[bold green]Assistant:[/bold green] {response.content}")
    
    # Update last interaction
    profile["last_interaction"] = datetime.now().isoformat()
    store.put(profile_namespace, "user_profile", profile)
    console.print("[green]✓ Updated last interaction time[/green]")


if __name__ == "__main__":
    console.print(Panel.fit("LangChain 1.0 Memory Management Examples", style="bold blue"))
    
    choice = console.input(
        "\n[bold]Select an example to run:[/bold]\n"
        "1. Basic Memory Operations\n"
        "2. Conversation Memory Demo\n"
        "3. Vector Memory Demo\n"
        "4. Long-term Memory Demo\n"
        "[bold]Enter your choice (1-4):[/bold] "
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
        console.print("[red]Invalid choice. Please run the script again.[/red]")