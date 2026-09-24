from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from datetime import datetime

# 工具1：计算器
@tool
def calculator(a: float, b: float, op: str) -> str:
    """
    简单计算器工具
    Args:
        a: 第一个数字
        b: 第二个数字
        op: 运算符号，支持 + - * /
    """
    if op == "+":
        res = a + b
    elif op == "-":
        res = a - b
    elif op == "*":
        res = a * b
    elif op == "/":
        if b == 0:
            return "除数不能为0"
        res = a / b
    else:
        return "不支持的运算符"
    return f"计算结果 = {res}"

# 工具2：获取当前时间（新增，写在tools数组前面！）
@tool
def get_current_time() -> str:
    """
    获取当前系统时间，当用户询问现在几点、当前日期、时间时调用
    """
    now = datetime.now()
    return f"当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}"


# 注册两个工具
tools = [calculator, get_current_time]
tool_node = ToolNode(tools)

# 模型
model = ChatOllama(
    model="qwen2.5:7b",
    temperature=0,
    base_url="http://127.0.0.1:11434"
).bind_tools(tools)


def should_continue(state: MessagesState):
    messages = state["messages"]
    last_msg = messages[-1]
    # 如果存在工具调用，则去执行工具；否则直接结束
    if last_msg.tool_calls:
        return "tools"
    return "__end__"


def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    # 调试打印：查看模型生成的工具调用
    print("\n====模型tool_calls信息====", response.tool_calls)
    return {"messages": [response]}


# 构建图
workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
# 删掉start_key/end_key，标准写法！
workflow.add_edge("tools", "agent")

app = workflow.compile()

# 导出流程图（需要先安装依赖 pip install pygraphviz）
try:
    with open("agent_graph.png", "wb") as f:
        f.write(app.get_graph().draw_mermaid_png())
    print("流程图已保存为 agent_graph.png")
except Exception as e:
    print("导出流程图失败，如需要该功能请执行 pip install pygraphviz，不影响Agent主体运行", e)


# 对话入口
if __name__ == "__main__":
    print("Agent已启动，输入问题，可调用计算器/时间工具。输入exit退出")
    while True:
        user_input = input("\n你：")
        if user_input == "exit":
            break
        sys_prompt = "你必须使用对应工具完成任务，数学计算调用calculator，查询时间调用get_current_time，不要自己口算或编造时间。"
        res = app.invoke({
            "messages": [
                ("system", sys_prompt),
                ("human", user_input)
            ]
        })
        print(f"AI: {res['messages'][-1].content}")
