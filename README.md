# LLM-Agent 简易原型（ReAct + LangGraph + Ollama）
> 个人开源项目，实现具备工具调用能力的LLM Agent，基于本地Ollama大模型运行，无外部API依赖。

## ✨ 项目功能
1. ReAct 智能Agent循环：思考 → 调用工具 → 获取结果 → 再思考输出答案
2. 内置工具
   - calculator：数学加减乘除计算器
   - get_current_time：获取系统当前时间
3. 本地私有化大模型推理，不依赖外部API
4. LangGraph状态图管理对话，模块化设计，方便新增自定义工具

## 🛠️ 技术栈
- Python 3.11.9
- LangGraph：构建Agent状态流转图
- langchain-ollama：对接本地Ollama大模型
- Ollama + Qwen2.5:7b：本地大模型推理
- datetime：时间工具

## 📦 环境部署
### 前置条件
1. 安装 Ollama，本地拉取模型
```bash
ollama pull qwen2.5:7b
```
2. 安装项目依赖
```bash
pip install -r requirements.txt
```
## ▶️ 运行项目
```bash
python main.py
```
启动后即可和 Agent 对话，它会自动判断什么时候调用计算器、时间工具。
