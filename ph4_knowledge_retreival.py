"""
=========================================================
ENTERPRISE CUSTOMER SUPPORT RAG AGENT
=========================================================

Objective:
------------
Enhance the baseline customer support agent using:
1. Embeddings
2. Semantic Search
3. Retrieval-Augmented Generation (RAG)
4. Knowledge Base Grounding

This version:
- Retrieves relevant information from documents
- Uses embeddings for semantic search
- Improves response accuracy
- Reduces hallucinations

---------------------------------------------------------
INSTALLATION
---------------------------------------------------------

pip install langchain
pip install langchain-openai
pip install langchain-community
pip install faiss-cpu
pip install tiktoken

---------------------------------------------------------
CREATE KNOWLEDGE BASE FILE
---------------------------------------------------------

Create:
knowledge_base.txt

Add sample content:

---------------------------------------------------------

Password Reset Policy:
Users can reset passwords using the Forgot Password option.

Refund Policy:
Refunds are processed within 5-7 business days.

Delivery Policy:
Orders are shipped within 2 business days.

MFA Security Policy:
MFA cannot be permanently disabled without admin approval.

Error 503:
Error 503 indicates temporary server unavailability.

Fraud Handling:
Fraud-related incidents must be escalated immediately.

Account Security:
Compromised accounts should be escalated to
the security team.

---------------------------------------------------------
RUN
---------------------------------------------------------

python rag_customer_support_agent.py
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
# LOAD KNOWLEDGE BASE DOCUMENT
# =========================================================

loader = TextLoader("knowledge_base.txt")

documents = loader.load()

# =========================================================
# SPLIT DOCUMENTS INTO CHUNKS
# =========================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

docs = text_splitter.split_documents(documents)

# =========================================================
# CREATE EMBEDDINGS
# =========================================================

embeddings = OpenAIEmbeddings()

# =========================================================
# CREATE VECTOR DATABASE
# =========================================================

vectorstore = FAISS.from_documents(
    docs,
    embeddings
)

# =========================================================
# CREATE RETRIEVER
# =========================================================

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

# =========================================================
# LLM CONFIGURATION
# =========================================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# =========================================================
# ENTERPRISE RAG PROMPT
# =========================================================

prompt = PromptTemplate.from_template("""
You are an enterprise AI Customer Support Agent.

IMPORTANT RULES:
- Use ONLY the provided knowledge base context.
- Do NOT fabricate policies.
- Refuse unsafe requests.
- Escalate sensitive issues.
- If information is missing, clearly say so.

--------------------------------------------------

Knowledge Base Context:
{context}

--------------------------------------------------

Customer Query:
{query}

--------------------------------------------------

Provide:
1. Issue Summary
2. Resolution Steps
3. Escalation Needed
4. Confidence Level
""")

# =========================================================
# LOGGING
# =========================================================

LOG_FILE = "rag_agent_logs.txt"

def log_interaction(user_input, context, response):

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        timestamp = datetime.datetime.now()

        file.write("\n" + "=" * 70)

        file.write(f"\n[{timestamp}]")

        file.write(f"\nUSER QUERY:\n{user_input}\n")

        file.write(f"\nRETRIEVED CONTEXT:\n{context}\n")

        file.write(f"\nAGENT RESPONSE:\n{response}\n")

# =========================================================
# RETRIEVE RELEVANT DOCUMENTS
# =========================================================

def retrieve_context(query):

    retrieved_docs = retriever.invoke(query)

    if not retrieved_docs:

        return None, []

    context = "\n".join([
        doc.page_content for doc in retrieved_docs
    ])

    return context, retrieved_docs

# =========================================================
# GENERATE RESPONSE
# =========================================================

def generate_response(query):

    context, retrieved_docs = retrieve_context(query)

    # -----------------------------------------------------
    # HANDLE MISSING INFORMATION
    # -----------------------------------------------------

    if not context:

        return (
            "I could not find relevant information "
            "in the knowledge base.",
            []
        )

    # -----------------------------------------------------
    # CREATE FINAL PROMPT
    # -----------------------------------------------------

    final_prompt = prompt.invoke({

        "context": context,
        "query": query
    })

    # -----------------------------------------------------
    # CALL LLM
    # -----------------------------------------------------

    response = llm.invoke(final_prompt)

    return response.content, retrieved_docs

# =========================================================
# MAIN APPLICATION
# =========================================================

def run_agent():

    print("=" * 70)
    print(" ENTERPRISE CUSTOMER SUPPORT RAG AGENT ")
    print("=" * 70)

    print("\nType 'exit' to stop.\n")

    while True:

        user_input = input("Customer: ")

        # Exit condition
        if user_input.lower() == "exit":

            print("\nAgent stopped.")
            break

        try:

            # Generate response
            response, retrieved_docs = generate_response(
                user_input
            )

            # Display response
            print("\nAgent Response:\n")
            print(response)

            # Show retrieved knowledge
            print("\nRetrieved Knowledge:\n")

            if retrieved_docs:

                for doc in retrieved_docs:

                    print("- " + doc.page_content)

            else:

                print("No relevant documents found.")

            print("\n" + "-" * 70)

            # Log interaction
            retrieved_text = "\n".join([
                doc.page_content for doc in retrieved_docs
            ])

            log_interaction(
                user_input,
                retrieved_text,
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
