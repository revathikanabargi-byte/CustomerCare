"""
=========================================================
ENTERPRISE ADAPTIVE CUSTOMER SUPPORT AGENT
=========================================================

Objective:
------------
Enhance the AI support agent with:
1. Feedback learning
2. Adaptive behavior
3. Response improvement
4. Memory-based personalization
5. Behavioral evolution

---------------------------------------------------------
FEATURES
---------------------------------------------------------

1. Feedback collection
2. Adaptive response behavior
3. Conversation memory
4. Retrieval-Augmented Generation (RAG)
5. Multi-step reasoning
6. Safety controls
7. Behavior evolution tracking

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

python adaptive_support_agent.py
"""

import os
import json
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
# MEMORY
# =========================================================

conversation_memory = []

MAX_MEMORY = 6

# =========================================================
# FEEDBACK STORAGE
# =========================================================

FEEDBACK_FILE = "feedback_memory.json"

# =========================================================
# DEFAULT ADAPTIVE SETTINGS
# =========================================================

adaptive_settings = {

    "response_style": "standard",

    "detail_level": "medium",

    "escalation_sensitivity": "normal",

    "positive_feedback_count": 0,

    "negative_feedback_count": 0
}

# =========================================================
# LOAD FEEDBACK MEMORY
# =========================================================

def load_feedback_memory():

    global adaptive_settings

    try:

        with open(FEEDBACK_FILE, "r") as file:

            adaptive_settings = json.load(file)

    except:

        save_feedback_memory()

# =========================================================
# SAVE FEEDBACK MEMORY
# =========================================================

def save_feedback_memory():

    with open(FEEDBACK_FILE, "w") as file:

        json.dump(
            adaptive_settings,
            file,
            indent=4
        )

# =========================================================
# LOGGING
# =========================================================

LOG_FILE = "adaptive_agent_logs.txt"

def log_interaction(user_input, response, feedback=None):

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        timestamp = datetime.datetime.now()

        file.write("\n" + "=" * 70)

        file.write(f"\n[{timestamp}]")

        file.write(f"\nUSER:\n{user_input}")

        file.write(f"\nAGENT:\n{response}")

        if feedback:

            file.write(f"\nFEEDBACK:\n{feedback}")

        file.write("\n")

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
# ADAPTIVE PROMPT BUILDER
# =========================================================

def build_adaptive_prompt():

    response_style = adaptive_settings[
        "response_style"
    ]

    detail_level = adaptive_settings[
        "detail_level"
    ]

    escalation_sensitivity = adaptive_settings[
        "escalation_sensitivity"
    ]

    return PromptTemplate.from_template(f"""
    You are an adaptive enterprise AI
    customer support agent.

    CURRENT BEHAVIOR SETTINGS:

    Response Style:
    {response_style}

    Detail Level:
    {detail_level}

    Escalation Sensitivity:
    {escalation_sensitivity}

    --------------------------------------------------

    Instructions:
    - Use retrieved knowledge
    - Be professional
    - Avoid hallucinations
    - Escalate sensitive issues
    - Learn from feedback trends

    --------------------------------------------------

    Previous Conversation:
    {{memory}}

    --------------------------------------------------

    Retrieved Knowledge:
    {{context}}

    --------------------------------------------------

    Customer Query:
    {{query}}

    --------------------------------------------------

    Generate:
    - Issue Understanding
    - Resolution Steps
    - Escalation Needed
    - Confidence Level
    """)

# =========================================================
# FEEDBACK ADAPTATION LOGIC
# =========================================================

def update_behavior(feedback):

    # -----------------------------------------------------
    # POSITIVE FEEDBACK
    # -----------------------------------------------------

    if feedback.lower() == "good":

        adaptive_settings[
            "positive_feedback_count"
        ] += 1

    # -----------------------------------------------------
    # NEGATIVE FEEDBACK
    # -----------------------------------------------------

    elif feedback.lower() == "bad":

        adaptive_settings[
            "negative_feedback_count"
        ] += 1

    # -----------------------------------------------------
    # ADAPTIVE BEHAVIOR CHANGES
    # -----------------------------------------------------

    negative_count = adaptive_settings[
        "negative_feedback_count"
    ]

    positive_count = adaptive_settings[
        "positive_feedback_count"
    ]

    # More detailed responses after bad feedback
    if negative_count >= 2:

        adaptive_settings[
            "detail_level"
        ] = "high"

    # More cautious escalation after repeated bad feedback
    if negative_count >= 3:

        adaptive_settings[
            "escalation_sensitivity"
        ] = "high"

    # Friendlier style after positive feedback
    if positive_count >= 3:

        adaptive_settings[
            "response_style"
        ] = "friendly"

    save_feedback_memory()

# =========================================================
# RESPONSE GENERATION
# =========================================================

def generate_response(user_input):

    # -----------------------------------------------------
    # RETRIEVE CONTEXT
    # -----------------------------------------------------

    retrieved_context = retrieve_context(
        user_input
    )

    # -----------------------------------------------------
    # MEMORY CONTEXT
    # -----------------------------------------------------

    memory_context = get_memory_context()

    # -----------------------------------------------------
    # BUILD ADAPTIVE PROMPT
    # -----------------------------------------------------

    adaptive_prompt = build_adaptive_prompt()

    final_prompt = adaptive_prompt.invoke({

        "memory": memory_context,

        "context": retrieved_context,

        "query": user_input
    })

    # -----------------------------------------------------
    # GENERATE RESPONSE
    # -----------------------------------------------------

    response = llm.invoke(final_prompt)

    return response.content

# =========================================================
# MAIN APPLICATION
# =========================================================

def run_agent():

    load_feedback_memory()

    print("=" * 70)
    print(" ENTERPRISE ADAPTIVE SUPPORT AGENT ")
    print("=" * 70)

    print("\nFeedback Commands:")
    print("- Type 'good' for positive feedback")
    print("- Type 'bad' for negative feedback")
    print("- Type 'exit' to stop\n")

    last_response = None

    while True:

        user_input = input("Customer: ")

        # -------------------------------------------------
        # EXIT
        # -------------------------------------------------

        if user_input.lower() == "exit":

            print("\nAgent stopped.")
            break

        # -------------------------------------------------
        # FEEDBACK HANDLING
        # -------------------------------------------------

        if user_input.lower() in ["good", "bad"]:

            update_behavior(user_input)

            print("\nFeedback stored.")

            print("\nUPDATED BEHAVIOR SETTINGS:\n")

            for key, value in adaptive_settings.items():

                print(f"{key}: {value}")

            continue

        try:

            # -------------------------------------------------
            # MEMORY STORAGE
            # -------------------------------------------------

            add_to_memory(
                "Customer",
                user_input
            )

            # -------------------------------------------------
            # GENERATE RESPONSE
            # -------------------------------------------------

            response = generate_response(
                user_input
            )

            last_response = response

            # -------------------------------------------------
            # STORE RESPONSE
            # -------------------------------------------------

            add_to_memory(
                "Agent",
                response
            )

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
