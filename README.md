# 🤖 AI-Powered Customer Support Automation System

> Built with LangGraph | Groq LLM | RAG Pipeline | SQLite Memory | Human-in-the-Loop

---

## 📌 Project Overview

ABC Technologies receives thousands of daily support requests covering product information, technical issues, billing queries, account management, and refund requests.

This project implements an **AI-Powered Customer Support Automation System** that automatically classifies, routes, and resolves customer queries using state-of-the-art AI agents built with **LangGraph**.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 Intent Classification | Automatically categorizes queries into Sales, Technical, Billing, or Account |
| 🔀 Smart Routing | Routes each query to the appropriate specialized support agent |
| 📚 RAG Pipeline | Retrieves relevant information from company documents using FAISS |
| 💾 Memory System | Stores and recalls conversation history using SQLite |
| 👤 Human-in-the-Loop | Escalates high-risk requests to human supervisor for approval |
| 🔍 Supervisor Agent | Validates and improves responses before sending to customers |

---

## 🏗️ System Architecture
Customer Query

↓

Intent Classification (LLM)

↓

Sales | Technical | Billing | Account | Memory

↓

Human Approval (High-Risk Only)

↓

Supervisor Agent

↓

Final Response → SQLite Memory Storage

---

## 🗂️ Project Structure
customer_support_ai/

├── main.py                 # Main LangGraph workflow and agents

├── knowledge_base.py       # Company documents for RAG pipeline

├── diagram.py              # Workflow diagram generator

├── memory.db               # SQLite conversation memory database

├── workflow_diagram.png    # LangGraph architecture diagram

├── screenshots.zip         # Project execution screenshots

└── README.md               # Project documentation

---

## 🏢 Support Departments

| Department | Handles |
|------------|---------|
| 💼 Sales | Product information, subscription plans, pricing details |
| 🔧 Technical Support | Application errors, installation issues, login problems |
| 💳 Billing | Invoice requests, payment issues, refund requests |
| 👤 Account | Password reset, profile updates, account activation |

---

## 📚 Knowledge Base Documents

The RAG pipeline retrieves information from:
- 📄 Company Policy Document
- 💰 Pricing Guide
- 🔧 Technical Manual
- ❓ FAQ Document

---

## ⚠️ Human-in-the-Loop Approval

The following requests require **human supervisor approval** before response:
- 💸 Refund requests
- ❌ Subscription cancellation
- 🔒 Account closure requests
- 🎁 Compensation requests
- 📢 Escalation to management

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Groq API Key (free at https://console.groq.com)

### Step 1 — Clone the repository
```bash
git clone https://github.com/Raja-Lineysha/ai-customer-support-automation.git
cd ai-customer-support-automation
```

### Step 2 — Install dependencies
```bash
pip install langgraph langchain langchain-community langchain-groq faiss-cpu tiktoken sentence-transformers huggingface-hub langchain-text-splitters langchain-core
```

### Step 3 — Add your Groq API key
Open `main.py` and replace:
```python
GROQ_API_KEY = "your_groq_api_key_here"
```

### Step 4 — Run the system
```bash
python main.py
```

---

## 🧪 Sample Queries Demonstrated

| # | Customer Query | Expected Route |
|---|---------------|----------------|
| 1 | What are the pricing plans available? | 💼 Sales |
| 2 | I forgot my account password | 👤 Account |
| 3 | My application crashes when I upload a file | 🔧 Technical Support |
| 4 | I need a refund for my annual subscription | 💳 Billing + 👤 Human Approval |
| 5 | What was my previous support issue? | 💾 Memory Recall |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| 🔗 LangGraph | Workflow orchestration and agent management |
| 🤖 Groq LLM (llama-3.3-70b-versatile) | AI response generation |
| 🔍 FAISS | Vector store for RAG retrieval |
| 🤗 HuggingFace Embeddings | Text embedding generation |
| 🗄️ SQLite | Conversation memory storage |
| 📊 Matplotlib | Workflow diagram generation |

---

## 📋 Assignment Tasks Completed

- [x] Task 1 — LangGraph workflow design
- [x] Task 2 — State structure implementation
- [x] Task 3 — Intent Classification node
- [x] Task 4 — Conditional routing
- [x] Task 5 — Specialized support agents
- [x] Task 6 — RAG pipeline integration
- [x] Task 7 — SQLite memory implementation
- [x] Task 8 — Human-in-the-Loop approval
- [x] Task 9 — Supervisor agent
- [x] Task 10 — System demonstration

---

## 👩‍💻 Author

**Raja Lineysha**
IBM Agentic AI Course — Assignment 2
