# LangChain 1.0 学习项目

这是一个基于 LangChain 1.0 的学习项目，旨在帮助您快速掌握 LangChain 的核心概念和功能。

## 项目结构

```
langchain-learning/
├── src/
│   └── langchain_learning/
│       ├── __init__.py
│       ├── examples/
│       │   ├── __init__.py
│       │   ├── simple_chatbot.py         # 基础聊天机器人示例 (已修改为中文聊天助手)
│       │   ├── agent_with_tools.py       # 使用工具的智能代理示例
│       │   ├── memory_management.py      # 记忆管理示例
│       │   ├── siliconflow_qwen.py       # 硅基流动 Qwen 模型集成示例
│       │   ├── test_chinese_chat.py      # 中文聊天助手测试脚本
│       │   ├── demo_chinese_chat.py      # 中文聊天助手演示脚本
│       │   ├── test_model_selection.py   # 模型选择测试脚本
│       │   └── model_selection_demo.py   # 模型比较演示脚本
│       ├── models/
│       │   └── __init__.py
│       └── utils/
│           └── __init__.py
├── tests/
├── docs/
│   ├── chinese_chatbot_guide.md    # 中文聊天助手使用指南
│   └── development_summary.md       # 开发总结文档
├── pyproject.toml
├── .env.example
└── README.md
```

## 安装与设置

### 环境要求

- Python 3.9 或更高版本
- UV (推荐的 Python 包管理工具)

### 安装步骤

1. 克隆项目到本地:
```bash
git clone <repository-url>
cd langchain-learning
```

2. 使用 UV 安装依赖:
```bash
uv sync
```

或者使用 pip:
```bash
pip install -e .
```

3. 配置环境变量:
```bash
cp .env.example .env
```

编辑 `.env` 文件，添加您的 API 密钥:
```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key
```

## 示例说明

### 1. 简单聊天机器人 (simple_chatbot.py)

这个示例已修改为使用硅基流动的 Qwen3-8B 模型，提供中文对话功能:

- 使用硅基流动 API (Qwen/Qwen3-8B)
- 中文对话界面
- 中文提示和响应
- 适合中文用户交互
- 支持多模型选择功能

运行示例:
```bash
uv run python src/langchain_learning/examples/simple_chatbot.py
```

快速演示:
```bash
uv run python src/langchain_learning/examples/demo_chinese_chat.py
```

模型选择测试:
```bash
uv run python src/langchain_learning/examples/test_model_selection.py
```

模型比较演示:
```bash
uv run python src/langchain_learning/examples/model_selection_demo.py
```

支持的模型:
- 通义千问 Qwen3-8B (默认)
- DeepSeek-R1-0528-Qwen3-8B
- 清华 GLM-Z1-9B-0414
- 清华 GLM-4-9B-Chat

详细使用指南请参考: [中文聊天助手使用指南](docs/chinese_chatbot_guide.md)

### 2. 使用工具的智能代理 (agent_with_tools.py)

这个示例展示了如何创建一个能够使用各种工具的智能代理，包括:

- 自定义工具创建 (时间获取、计算、随机数生成、内存操作、网络搜索)
- 代理创建与配置
- 交互式会话
- 结构化输出
- 中间件实现 (PII 处理、摘要、人工审核)

运行示例:
```bash
uv run python src/langchain_learning/examples/agent_with_tools.py
```

### 3. 记忆管理 (memory_management.py)

这个示例展示了 LangChain 1.0 中的记忆管理功能，包括:

- 短期记忆 (对话历史)
- 长期记忆 (向量存储)
- 嵌入缓存
- 语义搜索
- 记忆检索与更新

运行示例:
```bash
uv run python src/langchain_learning/examples/memory_management.py
```

## LangChain 1.0 核心概念

### 组件架构

LangChain 1.0 采用了组件化的架构设计，主要包括:

- **模型**: 支持多种 LLM 提供商 (OpenAI, Anthropic, Google 等)
- **工具**: 可扩展的工具系统，允许代理执行各种操作
- **记忆**: 多层次的记忆系统，支持短期和长期记忆
- **中间件**: 可插拔的处理组件，如 PII 处理、摘要等

### LangGraph 集成

LangChain 1.0 深度集成了 LangGraph，提供了:

- 状态图定义
- 条件路由
- 并行执行
- 人机交互循环

### 记忆系统

LangChain 1.0 的记忆系统支持:

- 对话历史管理
- 向量存储集成
- 语义搜索
- 嵌入缓存

## 开发指南

### 添加新示例

1. 在 `src/langchain_learning/examples/` 目录下创建新的 Python 文件
2. 实现您的示例代码
3. 在 README.md 中添加说明

### 运行测试

```bash
uv run pytest
```

### 代码格式化

项目使用 Ruff 进行代码格式化和检查:

```bash
uv run ruff format .
uv run ruff check .
```

## 学习资源

- [LangChain 1.0 官方文档](https://python.langchain.com/v0.2/)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [LangChain 社区](https://discord.gg/langchain)

## 常见问题

### Q: 如何切换不同的模型提供商?

A: 在示例代码中，您可以修改 `model_provider` 变量为 `"openai"`、`"anthropic"` 或 `"google"`，并确保在 `.env` 文件中设置了相应的 API 密钥。

### Q: 如何添加自定义工具?

A: 参考 `agent_with_tools.py` 中的工具定义方式，使用 `@tool` 装饰器创建自定义工具函数。

### Q: 如何使用自定义记忆系统?

A: 查看 `memory_management.py` 中的示例，了解如何实现短期记忆、长期记忆和嵌入缓存。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request!