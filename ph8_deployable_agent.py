"""
=========================================================
ENTERPRISE DEPLOYMENT-READY SUPPORT AGENT
=========================================================

Objective:
------------
Production-style AI Customer Support Agent with:
1. Deployment readiness
2. Logging and tracing
3. Runtime failure handling
4. Health monitoring
5. REST API support
6. Graceful degradation

---------------------------------------------------------
FEATURES
---------------------------------------------------------

1. FastAPI deployment
2. Structured logging
3. Latency tracking
4. Error handling
5. Graceful failure responses
6. Health check endpoint
7. Retrieval-Augmented Generation (RAG)
8. Conversation memory
9. Request tracing
10. Enterprise-safe responses

---------------------------------------------------------
INSTALLATION
---------------------------------------------------------

pip install fastapi
pip install uvicorn
pip install langchain
pip install langchain-openai
pip install langchain-community
pip install langchain-text-splitters
pip install faiss-cpu
pip install tiktoken

---------------------------------------------------------
CREATE KNOWLEDGE BASE FILE
---------------------------------------------------------

knowledge_base.txt

Sample Content:

Password Reset Policy:
Users can reset passwords using Forgot Password.

Refund Policy:
Refunds take 5-7 business days.

MFA Policy:
MFA cannot be disabled permanently.

Fraud Handling:
Fraud incidents must be escalated immediately.

Error 503:
Error 503 indicates temporary server unavailability.

---------------------------------------------------------
RUN LOCAL SERVER
---------------------------------------------------------

uvicorn deployment_ready_agent:app --reload

---------------------------------------------------------
TEST API
---------------------------------------------------------

Open Browser:

http://127.0.0.1:8000/docs

---------------------------------------------------------
SAMPLE API REQUEST
---------------------------------------------------------

POST /chat

{
    "query": "How long does a refund take?"
}

=========================================================
"""

import os
import time
import uuid
import logging
import traceback
from dotenv import load_dotenv

from typing import Dict

# =========================================================
# FASTAPI
# =========================================================

from fastapi import FastAPI
from pydantic import BaseModel

# =========================================================
# LANGCHAIN IMPORTS
# =========================================================

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from langchain_community.document_loaders import (
    TextLoader
)

from langchain_community.vectorstores import FAISS

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_core.prompts import PromptTemplate

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

# Load environment variables from .env file
load_dotenv()

# Verify API key is loaded
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please create a .env file with your API key.")

# =========================================================
# LOGGING CONFIGURATION
# =========================================================

logging.basicConfig(

    filename="deployment_agent.log",

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)

# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Enterprise Support Agent",
    version="1.0"
)

# =========================================================
# REQUEST MODEL
# =========================================================

class ChatRequest(BaseModel):

    query: str

# =========================================================
# LOAD KNOWLEDGE BASE
# =========================================================

loader = TextLoader("knowledge_base.txt")

documents = loader.load()

# =========================================================
# TEXT SPLITTING
# =========================================================

splitter = RecursiveCharacterTextSplitter(

    chunk_size=300,

    chunk_overlap=50
)

docs = splitter.split_documents(documents)

# =========================================================
# EMBEDDINGS
# =========================================================

embeddings = OpenAIEmbeddings()

# =========================================================
# VECTOR DATABASE
# =========================================================

vectorstore = FAISS.from_documents(
    docs,
    embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

# =========================================================
# LLM
# =========================================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# =========================================================
# MEMORY
# =========================================================

conversation_memory = []

MAX_MEMORY = 5

# =========================================================
# SAFETY RULES
# =========================================================

UNSAFE_KEYWORDS = [
    "hack",
    "bypass security",
    "steal",
    "disable mfa permanently"
]

# =========================================================
# MEMORY FUNCTIONS
# =========================================================

def add_to_memory(role, message):

    conversation_memory.append({

        "role": role,

        "message": message
    })

    if len(conversation_memory) > MAX_MEMORY:

        conversation_memory.pop(0)

# =========================================================
# MEMORY CONTEXT
# =========================================================

def get_memory_context():

    memory_text = ""

    for item in conversation_memory:

        memory_text += (
            f"{item['role']}: "
            f"{item['message']}\n"
        )

    return memory_text

# =========================================================
# SAFETY CHECK
# =========================================================

def is_safe(query):

    text = query.lower()

    for word in UNSAFE_KEYWORDS:

        if word in text:

            return False

    return True

# =========================================================
# RETRIEVAL
# =========================================================

def retrieve_context(query):

    docs = retriever.invoke(query)

    if not docs:

        return "No relevant knowledge found."

    context = "\n".join([
        doc.page_content for doc in docs
    ])

    return context

# =========================================================
# PROMPT
# =========================================================

prompt = PromptTemplate.from_template("""
You are an enterprise AI customer support agent.

Rules:
- Use only retrieved knowledge
- Avoid hallucinations
- Escalate sensitive issues
- Be professional
- Protect customer privacy

--------------------------------------------------

Conversation Memory:
{memory}

--------------------------------------------------

Retrieved Context:
{context}

--------------------------------------------------

Customer Query:
{query}

--------------------------------------------------

Provide:
- Issue Understanding
- Resolution Steps
- Escalation Needed
- Confidence Level
""")

# =========================================================
# RESPONSE GENERATION
# =========================================================

def generate_response(user_query):

    # -----------------------------------------------------
    # SAFETY CHECK
    # -----------------------------------------------------

    if not is_safe(user_query):

        return {
            "response":
                "Unsafe request detected.",
            "status":
                "blocked"
        }

    # -----------------------------------------------------
    # RETRIEVE CONTEXT
    # -----------------------------------------------------

    context = retrieve_context(user_query)

    # -----------------------------------------------------
    # MEMORY
    # -----------------------------------------------------

    memory = get_memory_context()

    # -----------------------------------------------------
    # FINAL PROMPT
    # -----------------------------------------------------

    final_prompt = prompt.invoke({

        "memory": memory,

        "context": context,

        "query": user_query
    })

    # -----------------------------------------------------
    # GENERATE RESPONSE
    # -----------------------------------------------------

    result = llm.invoke(final_prompt)

    return {
        "response": result.content,
        "status": "success"
    }

# =========================================================
# HEALTH CHECK ENDPOINT
# =========================================================

@app.get("/health")

def health_check():

    return {
        "status": "healthy"
    }

# =========================================================
# MAIN CHAT ENDPOINT
# =========================================================

@app.post("/chat")

def chat(request: ChatRequest):

    # -----------------------------------------------------
    # TRACE ID
    # -----------------------------------------------------

    trace_id = str(uuid.uuid4())

    # -----------------------------------------------------
    # LATENCY START
    # -----------------------------------------------------

    start_time = time.time()

    try:

        query = request.query

        # -------------------------------------------------
        # STORE MEMORY
        # -------------------------------------------------

        add_to_memory(
            "Customer",
            query
        )

        # -------------------------------------------------
        # GENERATE RESPONSE
        # -------------------------------------------------

        result = generate_response(query)

        # -------------------------------------------------
        # STORE RESPONSE MEMORY
        # -------------------------------------------------

        add_to_memory(
            "Agent",
            result["response"]
        )

        # -------------------------------------------------
        # LATENCY
        # -------------------------------------------------

        latency = round(
            time.time() - start_time,
            2
        )

        # -------------------------------------------------
        # LOGGING
        # -------------------------------------------------

        logging.info(

            f"TRACE_ID={trace_id} | "
            f"QUERY={query} | "
            f"STATUS=SUCCESS | "
            f"LATENCY={latency}s"
        )

        # -------------------------------------------------
        # API RESPONSE
        # -------------------------------------------------

        return {

            "trace_id": trace_id,

            "latency_seconds": latency,

            "status": result["status"],

            "response": result["response"]
        }

    # =====================================================
    # GRACEFUL FAILURE HANDLING
    # =====================================================

    except Exception as error:

        latency = round(
            time.time() - start_time,
            2
        )

        # -------------------------------------------------
        # ERROR LOGGING
        # -------------------------------------------------

        logging.error(

            f"TRACE_ID={trace_id} | "
            f"STATUS=FAILED | "
            f"LATENCY={latency}s | "
            f"ERROR={str(error)}"
        )

        logging.error(traceback.format_exc())

        # -------------------------------------------------
        # SAFE FAILURE RESPONSE
        # -------------------------------------------------

        return {

            "trace_id": trace_id,

            "status": "failed",

            "latency_seconds": latency,

            "response": (
                "The support agent encountered "
                "a temporary issue. "
                "Please try again later or "
                "contact human support."
            )
        }

"""
=========================================================
DEPLOYMENT ASSUMPTIONS
=========================================================

1. Python 3.10+
2. OpenAI API key available
3. Internet access enabled
4. knowledge_base.txt exists
5. Required pip packages installed

=========================================================
DEPLOYMENT OPTIONS
=========================================================

LOCAL:
uvicorn deployment_ready_agent:app --reload

PRODUCTION:
uvicorn deployment_ready_agent:app --host 0.0.0.0 --port 8000

DOCKER:
Can be containerized easily

CLOUD:
Deployable on:
- AWS
- Azure
- GCP
- Kubernetes
- OpenShift

=========================================================
LATENCY & ERROR LOGGING
=========================================================

Example Logs:

2026-05-01 12:10:11 |
INFO |
TRACE_ID=123 |
QUERY=Refund status |
STATUS=SUCCESS |
LATENCY=2.4s

=========================================================
GRACEFUL FAILURE HANDLING
=========================================================

Example Failure:
- OpenAI timeout
- Invalid API key
- Missing KB file

Safe User Response:
"The support agent encountered a temporary issue."

=========================================================
LIMITATIONS
=========================================================

1. In-memory conversation storage
2. No authentication
3. No rate limiting
4. No persistent database
5. No distributed tracing
6. Single-agent architecture
7. Retrieval quality depends on KB quality

=========================================================
FUTURE ENTERPRISE ENHANCEMENTS
=========================================================

- Redis memory
- PostgreSQL logging
- LangSmith tracing
- OAuth authentication
- API gateway
- Kubernetes autoscaling
- Observability dashboards
- Human approval workflows
- Multi-agent orchestration
- Guardrails & moderation APIs
=========================================================
"""
