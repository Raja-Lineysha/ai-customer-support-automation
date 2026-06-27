# ============================================================
# AI-Powered Customer Support Automation System
# Built with LangGraph + Groq + RAG + SQLite Memory
# ============================================================

import os
import sqlite3
from typing import TypedDict, List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langgraph.graph import StateGraph, END
from knowledge_base import COMPANY_POLICY, PRICING_GUIDE, TECHNICAL_MANUAL, FAQ_DOCUMENT

# ============================================================
# CONFIGURATION
# ============================================================
GROQ_API_KEY = "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"  # 👈 PASTE YOUR GROQ KEY HERE
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize Groq LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

# ============================================================
# TASK 2 — STATE STRUCTURE
# ============================================================
class CustomerSupportState(TypedDict):
    customer_name: str
    customer_query: str
    intent: str
    department: str
    retrieved_context: str
    agent_response: str
    needs_approval: bool
    approved: bool
    supervisor_response: str
    final_response: str
    conversation_history: List[dict]
    session_id: str

# ============================================================
# TASK 6 — RAG PIPELINE SETUP
# ============================================================
def setup_rag():
    print("Setting up RAG pipeline...")
    documents = [COMPANY_POLICY, PRICING_GUIDE, TECHNICAL_MANUAL, FAQ_DOCUMENT]
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = []
    for doc in documents:
        chunks.extend(splitter.split_text(doc))
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(chunks, embeddings)
    print("RAG pipeline ready!")
    return vectorstore

vectorstore = setup_rag()

def retrieve_context(query: str) -> str:
    docs = vectorstore.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in docs])

# ============================================================
# TASK 7 — SQLITE MEMORY
# ============================================================
def init_memory():
    conn = sqlite3.connect("memory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            customer_name TEXT,
            query TEXT,
            intent TEXT,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_to_memory(session_id, customer_name, query, intent, response):
    conn = sqlite3.connect("memory.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversations (session_id, customer_name, query, intent, response)
        VALUES (?, ?, ?, ?, ?)
    """, (session_id, customer_name, query, intent, response))
    conn.commit()
    conn.close()

def get_memory(session_id):
    conn = sqlite3.connect("memory.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT customer_name, query, intent, response, timestamp
        FROM conversations WHERE session_id = ?
        ORDER BY timestamp DESC LIMIT 5
    """, (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

init_memory()

# ============================================================
# TASK 3 — INTENT CLASSIFICATION NODE
# ============================================================
def classify_intent(state: CustomerSupportState) -> CustomerSupportState:
    print(f"\n[Intent Classification] Query: {state['customer_query']}")

    memory_keywords = ["previous", "last time", "before", "earlier", "history", "what did i ask"]
    if any(word in state["customer_query"].lower() for word in memory_keywords):
        state["intent"] = "Memory"
        state["department"] = "Memory"
        return state

    messages = [
        SystemMessage(content="""You are an intent classifier for a customer support system.
Classify the customer query into exactly one of these categories:
- Sales (pricing, plans, product info)
- Technical (errors, crashes, login, installation)
- Billing (invoices, payments, refunds)
- Account (password reset, profile, activation)

Reply with ONLY the category name. Nothing else."""),
        HumanMessage(content=state["customer_query"])
    ]
    response = llm.invoke(messages)
    intent = response.content.strip()
    state["intent"] = intent
    state["department"] = intent
    print(f"[Intent Classification] Result: {intent}")
    return state

# ============================================================
# TASK 4 — CONDITIONAL ROUTING
# ============================================================
def route_query(state: CustomerSupportState) -> str:
    intent = state["intent"]
    print(f"[Router] Routing to: {intent}")
    if intent == "Sales":
        return "sales_agent"
    elif intent == "Technical":
        return "technical_agent"
    elif intent == "Billing":
        return "billing_agent"
    elif intent == "Account":
        return "account_agent"
    elif intent == "Memory":
        return "memory_agent"
    else:
        return "sales_agent"

# ============================================================
# TASK 5 — SPECIALIZED AGENTS
# ============================================================
def sales_agent(state: CustomerSupportState) -> CustomerSupportState:
    print("[Sales Agent] Handling query...")
    context = retrieve_context(state["customer_query"])
    state["retrieved_context"] = context
    messages = [
        SystemMessage(content=f"""You are a Sales Support Agent for ABC Technologies.
Use the following company information to answer the customer query.

Company Information:
{context}

Be helpful, professional, and concise."""),
        HumanMessage(content=state["customer_query"])
    ]
    response = llm.invoke(messages)
    state["agent_response"] = response.content
    state["needs_approval"] = False
    return state

def technical_agent(state: CustomerSupportState) -> CustomerSupportState:
    print("[Technical Agent] Handling query...")
    context = retrieve_context(state["customer_query"])
    state["retrieved_context"] = context
    messages = [
        SystemMessage(content=f"""You are a Technical Support Agent for ABC Technologies.
Use the following technical documentation to help the customer.

Technical Documentation:
{context}

Provide clear step-by-step solutions."""),
        HumanMessage(content=state["customer_query"])
    ]
    response = llm.invoke(messages)
    state["agent_response"] = response.content
    state["needs_approval"] = False
    return state

def billing_agent(state: CustomerSupportState) -> CustomerSupportState:
    print("[Billing Agent] Handling query...")
    context = retrieve_context(state["customer_query"])
    state["retrieved_context"] = context

    high_risk_keywords = ["refund", "cancel", "closure", "compensation", "escalat"]
    needs_approval = any(word in state["customer_query"].lower() for word in high_risk_keywords)

    messages = [
        SystemMessage(content=f"""You are a Billing Support Agent for ABC Technologies.
Use the following billing information to help the customer.

Billing Information:
{context}

Be clear about billing processes and policies."""),
        HumanMessage(content=state["customer_query"])
    ]
    response = llm.invoke(messages)
    state["agent_response"] = response.content
    state["needs_approval"] = needs_approval
    return state

def account_agent(state: CustomerSupportState) -> CustomerSupportState:
    print("[Account Agent] Handling query...")
    context = retrieve_context(state["customer_query"])
    state["retrieved_context"] = context
    messages = [
        SystemMessage(content=f"""You are an Account Support Agent for ABC Technologies.
Use the following account management information to help the customer.

Account Information:
{context}

Guide the customer clearly through account-related processes."""),
        HumanMessage(content=state["customer_query"])
    ]
    response = llm.invoke(messages)
    state["agent_response"] = response.content
    state["needs_approval"] = False
    return state

def memory_agent(state: CustomerSupportState) -> CustomerSupportState:
    print("[Memory Agent] Retrieving conversation history...")
    history = get_memory(state["session_id"])
    if history:
        history_text = "\n".join([
            f"- Query: {row[1]} | Department: {row[2]} | Time: {row[4]}"
            for row in history
        ])
        state["agent_response"] = f"Here is your previous support history:\n\n{history_text}"
    else:
        state["agent_response"] = "I don't have any previous conversation history for you."
    state["needs_approval"] = False
    return state

# ============================================================
# TASK 8 — HUMAN-IN-THE-LOOP
# ============================================================
def check_approval_needed(state: CustomerSupportState) -> str:
    if state.get("needs_approval", False):
        return "human_approval"
    return "supervisor_agent"

def human_approval(state: CustomerSupportState) -> CustomerSupportState:
    print("\n" + "="*50)
    print("HUMAN APPROVAL REQUIRED")
    print("="*50)
    print(f"Customer Query: {state['customer_query']}")
    print(f"Agent Response: {state['agent_response']}")
    print("="*50)
    decision = input("Supervisor, do you approve this response? (yes/no): ").strip().lower()
    if decision == "yes":
        state["approved"] = True
        state["supervisor_response"] = "Approved by supervisor."
        print("Approved!")
    else:
        state["approved"] = False
        state["supervisor_response"] = "Rejected by supervisor."
        print("Rejected!")
    return state

# ============================================================
# TASK 9 — SUPERVISOR AGENT
# ============================================================
def supervisor_agent(state: CustomerSupportState) -> CustomerSupportState:
    print("[Supervisor Agent] Validating response...")

    if state.get("needs_approval") and not state.get("approved", False):
        state["final_response"] = "Your request has been received and is under review. A supervisor will contact you within 24 hours."
        return state

    messages = [
        SystemMessage(content="""You are a Customer Support Supervisor for ABC Technologies.
Review the agent response and improve it if needed.
Make sure it is professional, polite, clear and complete.
Return only the final improved response."""),
        HumanMessage(content=f"Customer Query: {state['customer_query']}\nAgent Response: {state['agent_response']}")
    ]
    response = llm.invoke(messages)
    state["final_response"] = response.content
    return state

# ============================================================
# FINAL RESPONSE NODE
# ============================================================
def generate_final_response(state: CustomerSupportState) -> CustomerSupportState:
    print("\n" + "="*60)
    print("FINAL RESPONSE TO CUSTOMER:")
    print("="*60)
    print(state["final_response"])
    print("="*60)

    save_to_memory(
        state["session_id"],
        state["customer_name"],
        state["customer_query"],
        state["intent"],
        state["final_response"]
    )
    return state

# ============================================================
# TASK 1 — BUILD LANGGRAPH WORKFLOW
# ============================================================
def build_graph():
    graph = StateGraph(CustomerSupportState)

    graph.add_node("classify_intent", classify_intent)
    graph.add_node("sales_agent", sales_agent)
    graph.add_node("technical_agent", technical_agent)
    graph.add_node("billing_agent", billing_agent)
    graph.add_node("account_agent", account_agent)
    graph.add_node("memory_agent", memory_agent)
    graph.add_node("human_approval", human_approval)
    graph.add_node("supervisor_agent", supervisor_agent)
    graph.add_node("generate_final_response", generate_final_response)

    graph.set_entry_point("classify_intent")

    graph.add_conditional_edges("classify_intent", route_query, {
        "sales_agent": "sales_agent",
        "technical_agent": "technical_agent",
        "billing_agent": "billing_agent",
        "account_agent": "account_agent",
        "memory_agent": "memory_agent"
    })

    for agent in ["sales_agent", "technical_agent", "billing_agent", "account_agent"]:
        graph.add_conditional_edges(agent, check_approval_needed, {
            "human_approval": "human_approval",
            "supervisor_agent": "supervisor_agent"
        })

    graph.add_edge("memory_agent", "supervisor_agent")
    graph.add_edge("human_approval", "supervisor_agent")
    graph.add_edge("supervisor_agent", "generate_final_response")
    graph.add_edge("generate_final_response", END)

    return graph.compile()

# ============================================================
# TASK 10 — DEMO WITH SAMPLE QUERIES
# ============================================================
def run_query(app, session_id, customer_name, query):
    print(f"\n{'='*60}")
    print(f"Customer: {customer_name}")
    print(f"Query: {query}")
    print(f"{'='*60}")

    initial_state = CustomerSupportState(
        customer_name=customer_name,
        customer_query=query,
        intent="",
        department="",
        retrieved_context="",
        agent_response="",
        needs_approval=False,
        approved=False,
        supervisor_response="",
        final_response="",
        conversation_history=[],
        session_id=session_id
    )
    result = app.invoke(initial_state)
    return result

if __name__ == "__main__":
    print("Starting AI-Powered Customer Support System...")
    app = build_graph()

    SESSION_ID = "customer_david_001"
    CUSTOMER_NAME = "David"

    # Query 1 - Sales
    run_query(app, SESSION_ID, CUSTOMER_NAME, "What are the pricing plans available for your software?")

    # Query 2 - Account
    run_query(app, SESSION_ID, CUSTOMER_NAME, "I forgot my account password.")

    # Query 3 - Technical
    run_query(app, SESSION_ID, CUSTOMER_NAME, "My application crashes whenever I upload a file.")

    # Query 4 - Billing (needs human approval)
    run_query(app, SESSION_ID, CUSTOMER_NAME, "I need a refund for my annual subscription.")

    # Query 5 - Memory Recall
    run_query(app, SESSION_ID, CUSTOMER_NAME, "What was my previous support issue?")