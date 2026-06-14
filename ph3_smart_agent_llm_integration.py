import os
import datetime
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# ---------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------

# Load environment variables from .env file
load_dotenv()

# Verify API key is loaded
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please create a .env file with your API key.")

# ---------------------------------------------------
# LLM CONFIGURATION
# ---------------------------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# ---------------------------------------------------
# PROMPT STRATEGIES
# ---------------------------------------------------

basic_prompt = PromptTemplate.from_template("""
Answer the customer support question.

Customer Query:
{query}
""")

structured_prompt = PromptTemplate.from_template("""
You are a customer support assistant.

Rules:
- Be professional
- Escalate sensitive issues
- Never ask for passwords

Customer Query:
{query}

Provide:
1. Issue Category
2. Resolution
3. Escalation Needed
""")

enterprise_prompt = PromptTemplate.from_template("""
You are an enterprise AI Support Resolution Agent.

Safety Rules:
- Refuse unsafe requests
- Do not fabricate policies
- Escalate sensitive issues
- Protect customer privacy
- Admit uncertainty if unsure

Response Format:
- Issue Summary
- Safe Resolution Steps
- Escalation Needed
- Confidence Level

Customer Query:
{query}
""")

# ---------------------------------------------------
# CHAIN CREATION (Modern LangChain)
# ---------------------------------------------------

basic_chain = basic_prompt | llm
structured_chain = structured_prompt | llm
enterprise_chain = enterprise_prompt | llm

# ---------------------------------------------------
# LOGGING
# ---------------------------------------------------

LOG_FILE = "smart_agent_logs.txt"

def log_interaction(strategy, user_input, response):

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        timestamp = datetime.datetime.now()

        file.write("\n" + "=" * 60)
        file.write(f"\n[{timestamp}]")
        file.write(f"\nPROMPT STRATEGY: {strategy}")
        file.write(f"\nUSER: {user_input}")
        file.write(f"\nAGENT RESPONSE:\n{response}\n")

# ---------------------------------------------------
# STRATEGY SELECTOR
# ---------------------------------------------------

def get_chain(strategy):

    if strategy == "1":
        return basic_chain, "Basic Prompt"

    elif strategy == "2":
        return structured_chain, "Structured Prompt"

    else:
        return enterprise_chain, "Enterprise Safety Prompt"

# ---------------------------------------------------
# MAIN APPLICATION
# ---------------------------------------------------

def run_agent():

    print("=" * 60)
    print(" SMART CUSTOMER CARE AI AGENT ")
    print("=" * 60)

    print("\nSelect Prompt Strategy:\n")

    print("1 -> Basic Prompt")
    print("2 -> Structured Prompt")
    print("3 -> Enterprise Safety Prompt\n")

    strategy = input("Choose strategy (1/2/3): ")

    chain, strategy_name = get_chain(strategy)

    print(f"\nUsing: {strategy_name}")
    print("\nType 'exit' to stop.\n")

    while True:

        user_input = input("Customer: ")

        if user_input.lower() == "exit":

            print("\nAgent stopped.")
            break

        try:

            response = chain.invoke({
                "query": user_input
            })

            print("\nAgent Response:\n")
            print(response.content)

            log_interaction(
                strategy_name,
                user_input,
                response.content
            )

            print("\n" + "-" * 60)

        except Exception as error:

            print("\nError:")
            print(error)

# ---------------------------------------------------
# START APPLICATION
# ---------------------------------------------------

if __name__ == "__main__":

    run_agent()
