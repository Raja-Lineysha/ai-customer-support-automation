# AI-Powered Customer Support Automation System

## Project Overview
This project implements an AI-Powered Customer Support Automation System for ABC Technologies using LangGraph, Groq LLM, RAG pipeline, and SQLite memory.

## Features
- Intent Classification (Sales, Technical, Billing, Account)
- Conditional Routing to specialized agents
- RAG pipeline using company documents
- SQLite-based conversation memory
- Human-in-the-Loop approval for high-risk requests
- Supervisor agent for response validation

## Project Structure
- main.py - Main application code
- knowledge_base.py - Company documents for RAG
- memory.db - SQLite memory database
- README.md - Project documentation

## Setup Instructions

### Step 1 - Install dependencies
pip install langgraph langchain langchain-community langchain-groq faiss-cpu tiktoken sentence-transformers huggingface-hub langchain-text-splitters langchain-core

### Step 2 - Add your Groq API key
Open main.py and replace your_groq_api_key_here with your actual Groq API key.

### Step 3 - Run the system
python main.py

## Sample Queries Demonstrated
- Query 1: What are the pricing plans? → Sales
- Query 2: I forgot my password → Account
- Query 3: My app crashes on file upload → Technical Support
- Query 4: I need a refund → Billing with Human Approval
- Query 5: What was my previous issue? → Memory Recall

## Technologies Used
- LangGraph - Workflow orchestration
- Groq LLM llama-3.3-70b-versatile - AI responses
- FAISS - Vector store for RAG
- HuggingFace Embeddings - Text embeddings
- SQLite - Conversation memory