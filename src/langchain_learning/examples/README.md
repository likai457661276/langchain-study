# LangChain 1.0 智能体示例

本项目展示了如何使用LangChain 1.0构建智能体系统，包括基础工具调用和高级功能实现。

## 功能特点

### 基础智能体功能
- **工具调用**: 集成多种工具，包括天气查询、计算器、时间获取等
- **结构化输出**: 使用Pydantic定义输出结构，确保数据格式一致性
- **中间件支持**: 实现请求预处理和响应后处理
- **交互式对话**: 支持多轮对话和上下文管理

### 高级智能体功能
- **记忆管理**: 实现对话历史的存储和检索
- **条件路由**: 根据用户意图智能选择处理流程
- **工具链组合**: 将多个工具串联使用，实现复杂功能
- **流式处理**: 支持实时流式输出，提升用户体验
- **错误处理**: 完善的错误处理机制，确保系统稳定性

## 安装依赖

```bash
pip install langchain langchain-openai python-dotenv pydantic
```

## 环境配置

在项目根目录创建`.env`文件，添加以下内容：

```
OPENAI_API_KEY=your_openai_api_key_here
```

## 运行示例

### 交互式运行

1. **基础智能体示例**:
   ```bash
   python src/langchain_learning/examples/agent_with_tools.py
   ```

2. **高级智能体示例**:
   ```bash
   python src/langchain_learning/examples/advanced_agent.py
   ```

### 自动演示

运行自动演示脚本，查看所有功能的演示：

```bash
python src/langchain_learning/examples/auto_demo.py
```

该脚本将自动演示：
- 基础智能体的结构化输出和中间件功能
- 高级智能体的记忆管理、工具链组合和错误处理
- 所有测试用例的执行

### 交互式演示

运行交互式演示脚本，手动选择要演示的功能：

```bash
python src/langchain_learning/examples/demo.py
```

## 代码结构

```
src/langchain_learning/examples/
├── agent_with_tools.py      # 基础智能体实现
├── advanced_agent.py         # 高级智能体实现
├── test_agent.py             # 基础智能体测试
├── test_advanced_agent.py    # 高级智能体测试
├── demo.py                   # 交互式演示脚本
├── auto_demo.py              # 自动演示脚本
└── README.md                 # 本文档
```

## 主要组件

### 基础智能体组件

- **CustomTool**: 自定义工具基类
- **WeatherSearchTool**: 天气查询工具
- **CalculatorTool**: 计算器工具
- **TimeTool**: 时间获取工具
- **MemoryReadTool**: 内存读取工具
- **MemoryWriteTool**: 内存写入工具
- **GenerateRandomNumberTool**: 随机数生成工具
- **StructuredOutputParser**: 结构化输出解析器
- **LoggingMiddleware**: 日志中间件
- **AgentWithTools**: 基础智能体类

### 高级智能体组件

- **SimpleMemory**: 简单记忆管理类
- **ConditionalRoutingAgent**: 条件路由智能体
- **ToolChain**: 工具链组合类
- **StreamingAgent**: 流式处理智能体
- **ErrorHandlingAgent**: 错误处理智能体
- **AdvancedAgent**: 高级智能体类

### 工具集

- **weather_search**: 天气查询
- **calculator**: 计算器
- **get_current_time**: 获取当前时间
- **memory_read**: 读取内存
- **memory_write**: 写入内存
- **generate_random_number**: 生成随机数
- **data_analysis**: 数据分析
- **text_sorting**: 文本排序
- **text_generation**: 文本生成
- **task_scheduler**: 任务调度

## 注意事项

1. 确保已正确设置OpenAI API密钥
2. 网络连接正常，以便访问OpenAI API
3. 某些工具（如天气查询）可能需要额外的API配置

## 故障排除

### 常见问题

1. **导入错误**: 确保所有依赖已正确安装
2. **API密钥错误**: 检查`.env`文件中的API密钥是否正确
3. **网络连接问题**: 确保网络连接正常，可以访问OpenAI API

### 调试技巧

1. 查看日志输出，了解智能体的决策过程
2. 使用测试脚本验证各个组件的功能
3. 检查工具的输入和输出，确保数据格式正确

## 扩展

### 添加新工具

1. 继承`BaseTool`类
2. 实现`_run`方法
3. 在智能体中注册新工具

### 添加新的输出格式

1. 定义新的Pydantic模型
2. 创建相应的输出解析器
3. 在智能体中使用新的输出格式

### 添加新的中间件

1. 继承`BaseMiddleware`类
2. 实现`before`和`after`方法
3. 在智能体中注册新的中间件

## 参考资料

- [LangChain 1.0 官方文档](https://python.langchain.com/docs/get_started/introduction)
- [LangChain 智能体指南](https://python.langchain.com/docs/modules/agents)
- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)