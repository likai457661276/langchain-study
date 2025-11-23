# 硅基流动中文聊天助手使用指南

本指南介绍如何使用硅基流动中文聊天助手及其多模型选择功能。

## 快速开始

### 1. 环境配置

确保您已设置 `SILICONFLOW_API_KEY` 环境变量：

```bash
# 在 .env 文件中添加
SILICONFLOW_API_KEY=your_siliconflow_api_key_here
```

### 2. 运行中文聊天助手

```bash
uv run python src/langchain_learning/examples/simple_chatbot.py
```

## 功能特性

### 1. 交互式中文聊天

- 支持自然中文对话
- 提供流畅的聊天体验
- 可随时退出对话

### 2. 多模型选择

支持以下模型：

1. **通义千问 Qwen3-8B** (默认)
   - 阿里巴巴开发的大型语言模型
   - 擅长中文理解和生成

2. **DeepSeek-R1-0528-Qwen3-8B**
   - DeepSeek AI 开发的推理模型
   - 适合复杂推理任务

3. **清华 GLM-Z1-9B-0414**
   - 清华大学开发的通用语言模型
   - 平衡性能与效率

4. **清华 GLM-4-9B-Chat**
   - 清华大学开发的对话优化模型
   - 专为对话场景优化

### 3. 演示功能

- **消息类型演示**: 展示不同消息类型的处理
- **流式响应演示**: 展示实时流式输出效果
- **模型列表查看**: 查看所有可用模型

## 使用示例

### 基本对话

```bash
# 启动聊天助手
uv run python src/langchain_learning/examples/simple_chatbot.py

# 选择 "1. 中文聊天"
# 选择模型 (或使用默认)
# 开始对话
```

### 模型比较

```bash
# 运行模型比较演示
uv run python src/langchain_learning/examples/model_selection_demo.py

# 选择 "1. 模型响应比较"
# 查看不同模型对同一问题的回答
```

### 交互式模型选择

```bash
# 运行模型比较演示
uv run python src/langchain_learning/examples/model_selection_demo.py

# 选择 "2. 交互式模型选择"
# 选择特定模型进行对话
```

## 高级用法

### 自定义系统提示

您可以在代码中修改系统提示，定制模型的行为：

```python
# 在 simple_chatbot.py 中修改
system_prompt = "你是一个专业的Python编程助手..."
```

### 调整模型参数

可以根据需要调整模型参数：

```python
# 在 initialize_siliconflow_model 函数中
llm = ChatOpenAI(
    model=model_id,
    temperature=0.7,    # 控制创造性，0-1之间
    max_tokens=1024,    # 最大响应长度
    streaming=True      # 启用流式响应
)
```

## 故障排除

### 常见问题

1. **API密钥错误**
   - 确保 `SILICONFLOW_API_KEY` 正确设置
   - 检查密钥是否有效

2. **模型响应慢**
   - 尝试减少 `max_tokens` 值
   - 检查网络连接

3. **模型选择无效**
   - 确保输入有效的数字选项
   - 检查模型ID是否正确

### 调试技巧

1. 使用测试脚本验证模型连接：
   ```bash
   uv run python src/langchain_learning/examples/test_model_selection.py
   ```

2. 检查API响应：
   ```python
   # 在代码中添加调试输出
   print(f"模型ID: {model_id}")
   print(f"API响应: {response}")
   ```

## 扩展开发

### 添加新模型

1. 在 `list_available_models` 函数中添加新模型：
   ```python
   {
       "id": "new/model-id",
       "name": "新模型名称"
   }
   ```

2. 确保新模型在硅基流动平台上可用

### 自定义工具

您可以扩展聊天助手，添加自定义工具：

```python
from langchain.tools import tool

@tool
def custom_tool(input_text: str) -> str:
    """自定义工具描述"""
    # 工具实现
    return "工具结果"
```

## 资源链接

- [硅基流动官方文档](https://siliconflow.cn/)
- [LangChain 1.0 文档](https://python.langchain.com/v0.2/)
- [通义千问模型介绍](https://qwen.aliyun.com/)
- [DeepSeek AI](https://www.deepseek.ai/)
- [清华GLM模型](https://github.com/THUDM/GLM)