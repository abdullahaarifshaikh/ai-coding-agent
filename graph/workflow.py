from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage
from core.state import AgentState
from core.model import get_model
from tools import tools
from core.prompt import SYSTEM_PROMPT

def build_workflow():
    model_with_tools = get_model()

    def call_model(state: AgentState):
        sys_msg = SystemMessage(content=SYSTEM_PROMPT)
        messages = [sys_msg] + state["messages"]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}

    wf = StateGraph(AgentState)

    wf.add_node("agent", call_model)
    wf.add_node("tools", ToolNode(tools))

    wf.add_edge(START, "agent")
    wf.add_conditional_edges("agent", tools_condition)
    wf.add_edge("tools", "agent")

    wf.set_finish_point("agent")

    return wf.compile()
