"""
=========================================================
ENTERPRISE CUSTOMER SUPPORT TOOL AGENT
=========================================================

Objective:
------------
Enhance the customer support agent with:
1. Tool usage
2. Tool selection logic
3. Safeguards
4. Failure handling
5. Misuse prevention

---------------------------------------------------------
FEATURES
---------------------------------------------------------

TOOLS:
1. Knowledge Base Search Tool
2. Ticket Escalation Tool
3. Order Status Tool

SAFETY:
- Prevent unsafe actions
- Prevent infinite loops
- Handle invalid tool selection
- Restrict sensitive operations

---------------------------------------------------------
INSTALLATION
---------------------------------------------------------

pip install langchain
pip install langchain-openai
pip install langchain-community
pip install faiss-cpu
pip install tiktoken
pip install langchain-text-splitters

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
Fraud cases must be escalated.

---------------------------------------------------------
RUN
---------------------------------------------------------

python tool_enabled_support_agent.py
"""

import os
import datetime
from dotenv import load_dotenv

# =========================================================
# LANGCHAIN IMPORTS
# =========================================================

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS

from langchain_text_splitters import RecursiveCharacterTextSplitter

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

# Load environment variables from .env file
load_dotenv()

# Verify API key is loaded
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please create a .env file with your API key.")

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
# VECTOR STORE
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
# TOOL 1 - KNOWLEDGE SEARCH
# =========================================================

def knowledge_search_tool(query):

    docs = retriever.invoke(query)

    if not docs:
        return "No relevant knowledge found."

    context = "\n".join([
        doc.page_content for doc in docs
    ])

    return context

# =========================================================
# TOOL 2 - ESCALATION TOOL
# =========================================================

def escalation_tool(issue):

    return (
        f"ESCALATION CREATED:\n"
        f"Issue '{issue}' has been escalated "
        f"to the human support team."
    )

# =========================================================
# TOOL 3 - ORDER STATUS TOOL
# =========================================================

def order_status_tool(order_id):

    fake_orders = {

        "1001": "Shipped",
        "1002": "Processing",
        "1003": "Delivered"
    }

    return fake_orders.get(
        order_id,
        "Order ID not found."
    )

# =========================================================
# TOOL REGISTRY
# =========================================================

TOOLS = {

    "knowledge_search": knowledge_search_tool,
    "escalation": escalation_tool,
    "order_status": order_status_tool
}

# =========================================================
# SAFETY RULES
# =========================================================

UNSAFE_KEYWORDS = [
    "hack",
    "bypass security",
    "disable mfa permanently",
    "steal"
]

MAX_TOOL_CALLS = 3

# =========================================================
# LOGGING
# =========================================================

LOG_FILE = "tool_agent_logs.txt"

def log_interaction(user_input, tool_used, response):

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        timestamp = datetime.datetime.now()

        file.write("\n" + "=" * 70)

        file.write(f"\n[{timestamp}]")

        file.write(f"\nUSER:\n{user_input}")

        file.write(f"\nTOOL USED:\n{tool_used}")

        file.write(f"\nRESPONSE:\n{response}\n")

# =========================================================
# TOOL SELECTION LOGIC
# =========================================================

def choose_tool(user_input):

    text = user_input.lower()

    # -----------------------------------------------------
    # CORRECT TOOL SELECTION
    # -----------------------------------------------------

    if "refund" in text:
        return "knowledge_search"

    elif "password" in text:
        return "knowledge_search"

    elif "fraud" in text:
        return "escalation"

    elif "hacked" in text:
        return "escalation"

    elif "order" in text:
        return "order_status"

    # -----------------------------------------------------
    # INCORRECT TOOL SELECTION DEMO
    # -----------------------------------------------------

    elif "weather" in text:

        # Wrong tool intentionally
        return "order_status"

    return "knowledge_search"

# =========================================================
# SAFETY CHECK
# =========================================================

def safety_check(user_input):

    text = user_input.lower()

    for word in UNSAFE_KEYWORDS:

        if word in text:

            return False

    return True

# =========================================================
# MAIN AGENT
# =========================================================

def run_agent():

    print("=" * 70)
    print(" ENTERPRISE CUSTOMER SUPPORT TOOL AGENT ")
    print("=" * 70)

    print("\nType 'exit' to stop.\n")

    tool_call_count = 0

    while True:

        user_input = input("Customer: ")

        if user_input.lower() == "exit":

            print("\nAgent stopped.")
            break

        # -------------------------------------------------
        # SAFETY CHECK
        # -------------------------------------------------

        if not safety_check(user_input):

            response = (
                "Unsafe or policy-violating request detected."
            )

            print("\nAgent:")
            print(response)

            log_interaction(
                user_input,
                "BLOCKED",
                response
            )

            continue

        # -------------------------------------------------
        # LOOP SAFEGUARD
        # -------------------------------------------------

        tool_call_count += 1

        if tool_call_count > MAX_TOOL_CALLS:

            response = (
                "Too many tool calls detected. "
                "Escalating to human support."
            )

            print("\nAgent:")
            print(response)

            log_interaction(
                user_input,
                "LOOP_PROTECTION",
                response
            )

            break

        # -------------------------------------------------
        # SELECT TOOL
        # -------------------------------------------------

        tool_name = choose_tool(user_input)

        print(f"\n[Tool Selected: {tool_name}]")

        # -------------------------------------------------
        # EXECUTE TOOL
        # -------------------------------------------------

        try:

            if tool_name == "order_status":

                # Extract order ID
                words = user_input.split()

                order_id = None

                for word in words:

                    if word.isdigit():

                        order_id = word
                        break

                if order_id:

                    result = TOOLS[tool_name](order_id)

                else:

                    result = (
                        "Please provide a valid order ID."
                    )

            else:

                result = TOOLS[tool_name](user_input)

            # -------------------------------------------------
            # LLM RESPONSE GENERATION
            # -------------------------------------------------

            final_prompt = f"""
            You are an enterprise customer support AI.

            User Query:
            {user_input}

            Tool Result:
            {result}

            Generate a professional customer response.
            """

            response = llm.invoke(final_prompt)

            print("\nAgent Response:\n")
            print(response.content)

            print("\n" + "-" * 70)

            log_interaction(
                user_input,
                tool_name,
                response.content
            )

        except Exception as error:

            error_response = (
                f"Tool execution failed: {error}"
            )

            print("\nError:")
            print(error_response)

            log_interaction(
                user_input,
                "FAILED_TOOL_CALL",
                error_response
            )

# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    run_agent()
