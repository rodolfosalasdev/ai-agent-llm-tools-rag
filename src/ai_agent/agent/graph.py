from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from ai_agent.config import settings
from ai_agent.rag.vectorstore import build_vector_store, create_knowledge_search_tool
from ai_agent.tools.order_tool import get_order_status


def build_agent():
    vector_store = build_vector_store()
    knowledge_tool = create_knowledge_search_tool(vector_store)

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0.2,
    )

    return create_react_agent(
        llm,
        tools=[knowledge_tool, get_order_status],
        prompt=(
            "You are a support agent for a demo SaaS product. "
            "Use search_support_knowledge for policy/FAQ questions and get_order_status "
            "for order tracking. Answer in the same language as the user."
        ),
    )


def run_agent(question: str) -> str:
    agent = build_agent()
    result = agent.invoke({"messages": [("user", question)]})
    last_message = result["messages"][-1]
    return last_message.content
