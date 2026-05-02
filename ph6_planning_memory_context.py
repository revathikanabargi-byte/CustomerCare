"""
=========================================================
ENTERPRISE MULTI-STEP REASONING SUPPORT AGENT
=========================================================

Objective:
------------
Enhance the AI support agent with:
1. Multi-step reasoning
2. Conversation memory
3. Multi-turn conversations
4. Planning logic
5. Memory retention and reset behavior

---------------------------------------------------------
FEATURES
---------------------------------------------------------

1. Multi-step reasoning
2. Conversation memory
3. Context-aware conversations
4. Memory reset
5. Escalation handling
6. Safety controls
7. Retrieval-Augmented Generation (RAG)

---------------------------------------------------------
INSTALLATION
---------------------------------------------------------

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

Account Security:
Compromised accounts should be escalated to security.

---------------------------------------------------------
RUN
---------------------------------------------------------

python multi_step_reasoning_agent.py
"""

import os
import datetime

# =========================================================
# LANGCHAIN IMPORTS
# =========================================================

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_core.prompts import PromptTemplate

# =========================================================
# OPENAI API KEY
# =========================================================

os.environ["OPENAI_API_KEY"] = "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"

# =========================================================
# LOAD KNOWLEDGE BASE
# =========================================================

loader = TextLoader("knowledge_base.txt")

documents = loader.load()

# =========================================================
# SPLIT DOCUMENTS
# =========================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)

# =========================================================
# CREATE EMBEDDINGS
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
# SHORT-TERM MEMORY
# =========================================================

conversation_memory = []

MAX_MEMORY = 5

# =========================================================
# MEMORY RESET KEYWORDS
# =========================================================

RESET_COMMANDS = [
    "reset",
    "clear memory",
    "forget conversation"
]

# =========================================================
# SAFETY KEYWORDS
# =========================================================

UNSAFE_KEYWORDS = [
    "hack",
    "bypass security",
    "disable mfa permanently",
    "steal"
]

# =========================================================
# LOGGING
# =========================================================

LOG_FILE = "multi_step_agent_logs.txt"

def log_interaction(user_input, response):

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        timestamp = datetime.datetime.now()

        file.write("\n" + "=" * 70)

        file.write(f"\n[{timestamp}]")

        file.write(f"\nUSER:\n{user_input}")

        file.write(f"\nAGENT:\n{response}\n")

# =========================================================
# MEMORY FUNCTIONS
# =========================================================

def add_to_memory(role, message):

    conversation_memory.append({
        "role": role,
        "message": message
    })

    # -----------------------------------------------------
    # MEMORY RETENTION POLICY
    # Keep only latest conversations
    # -----------------------------------------------------

    if len(conversation_memory) > MAX_MEMORY:

        conversation_memory.pop(0)

# =========================================================
# GET MEMORY CONTEXT
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
# RESET MEMORY
# =========================================================

def reset_memory():

    conversation_memory.clear()

# =========================================================
# SAFETY CHECK
# =========================================================

def is_safe(query):

    query = query.lower()

    for word in UNSAFE_KEYWORDS:

        if word in query:

            return False

    return True

# =========================================================
# RETRIEVE KNOWLEDGE
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
# MULTI-STEP REASONING
# =========================================================

def reason_and_respond(user_input):

    # -----------------------------------------------------
    # STEP 1 - SAFETY CHECK
    # -----------------------------------------------------

    if not is_safe(user_input):

        return (
            "Unsafe or policy-violating request detected."
        )

    # -----------------------------------------------------
    # STEP 2 - RETRIEVE KNOWLEDGE
    # -----------------------------------------------------

    retrieved_context = retrieve_context(user_input)

    # -----------------------------------------------------
    # STEP 3 - FETCH MEMORY
    # -----------------------------------------------------

    memory_context = get_memory_context()

    # -----------------------------------------------------
    # STEP 4 - MULTI-STEP PLANNING PROMPT
    # -----------------------------------------------------

    prompt = PromptTemplate.from_template("""
    You are an enterprise AI Customer Support Agent.

    --------------------------------------------------

    STEP-BY-STEP INSTRUCTIONS:

    1. Understand the user's issue
    2. Review previous conversation context
    3. Use the retrieved knowledge base
    4. Decide whether escalation is needed
    5. Generate a safe and professional response

    --------------------------------------------------

    Previous Conversation:
    {memory}

    --------------------------------------------------

    Retrieved Knowledge:
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

    final_prompt = prompt.invoke({

        "memory": memory_context,
        "context": retrieved_context,
        "query": user_input
    })

    # -----------------------------------------------------
    # STEP 5 - GENERATE RESPONSE
    # -----------------------------------------------------

    response = llm.invoke(final_prompt)

    return response.content

# =========================================================
# MAIN APPLICATION
# =========================================================

def run_agent():

    print("=" * 70)
    print(" ENTERPRISE MULTI-STEP REASONING AGENT ")
    print("=" * 70)

    print("\nCommands:")
    print("- Type 'reset' to clear memory")
    print("- Type 'exit' to stop\n")

    while True:

        user_input = input("Customer: ")

        # -------------------------------------------------
        # EXIT
        # -------------------------------------------------

        if user_input.lower() == "exit":

            print("\nAgent stopped.")
            break

        # -------------------------------------------------
        # MEMORY RESET
        # -------------------------------------------------

        if user_input.lower() in RESET_COMMANDS:

            reset_memory()

            print("\nMemory cleared.")

            continue

        try:

            # -------------------------------------------------
            # ADD USER INPUT TO MEMORY
            # -------------------------------------------------

            add_to_memory("Customer", user_input)

            # -------------------------------------------------
            # MULTI-STEP REASONING
            # -------------------------------------------------

            response = reason_and_respond(user_input)

            # -------------------------------------------------
            # STORE RESPONSE IN MEMORY
            # -------------------------------------------------

            add_to_memory("Agent", response)

            # -------------------------------------------------
            # DISPLAY RESPONSE
            # -------------------------------------------------

            print("\nAgent Response:\n")
            print(response)

            print("\n" + "-" * 70)

            # -------------------------------------------------
            # LOGGING
            # -------------------------------------------------

            log_interaction(
                user_input,
                response
            )

        except Exception as error:

            print("\nError:")
            print(error)

# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    run_agent()
