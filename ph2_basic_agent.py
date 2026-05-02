"""
Basic Customer Care AI Agent
--------------------------------
Features:
1. Accepts user input
2. Generates simple rule-based responses
3. Demonstrates baseline limitations
4. Logs conversations

Run:
python customer_support_agent.py
"""

import datetime

# ----------------------------------------
# Simple Rule-Based Knowledge Base
# ----------------------------------------

RESPONSES = {
    "password": "You can reset your password using the 'Forgot Password' option.",
    "refund": "Refund requests are usually processed within 5-7 business days.",
    "payment": "Please verify whether the payment was deducted from your account.",
    "error 503": "Error 503 means the service is temporarily unavailable.",
    "delivery": "Please check your order tracking status in the Orders section.",
    "cancel order": "Your order can be cancelled before shipment."
}

# ----------------------------------------
# Unsafe Keywords
# ----------------------------------------

UNSAFE_REQUESTS = [
    "hack",
    "steal",
    "disable security",
    "bypass",
    "fake payment"
]

# ----------------------------------------
# Sensitive Keywords for Escalation
# ----------------------------------------

ESCALATE_REQUESTS = [
    "fraud",
    "legal",
    "complaint",
    "lawsuit",
    "account hacked"
]

# ----------------------------------------
# Log File
# ----------------------------------------

LOG_FILE = "customer_support_logs.txt"

# ----------------------------------------
# Logging Function
# NOTE:
# This baseline version stores raw user data.
# This is intentionally shown as a limitation.
# ----------------------------------------

def log_interaction(user_input, response):

    with open(LOG_FILE, "a") as file:

        timestamp = datetime.datetime.now()

        file.write(f"\n[{timestamp}]")
        file.write(f"\nUser: {user_input}")
        file.write(f"\nAgent: {response}\n")

# ----------------------------------------
# Response Generator
# ----------------------------------------

def generate_response(user_input):

    user_input_lower = user_input.lower()

    # ------------------------------------
    # Safety Check
    # ------------------------------------

    for unsafe_word in UNSAFE_REQUESTS:

        if unsafe_word in user_input_lower:

            return (
                "I cannot assist with unsafe or policy-violating requests."
            )

    # ------------------------------------
    # Escalation Check
    # ------------------------------------

    for escalate_word in ESCALATE_REQUESTS:

        if escalate_word in user_input_lower:

            return (
                "This issue is sensitive and will be escalated "
                "to a human support specialist."
            )

    # ------------------------------------
    # Rule-Based Matching
    # ------------------------------------

    for keyword, response in RESPONSES.items():

        if keyword in user_input_lower:

            return response

    # ------------------------------------
    # Default Response
    # ------------------------------------

    return (
        "Sorry, I could not understand your request. "
        "Please contact customer support."
    )

# ----------------------------------------
# Main Agent Loop
# ----------------------------------------

def run_agent():

    print("=" * 50)
    print(" Customer Care AI Support Agent ")
    print("=" * 50)

    print("\nType 'exit' to stop the agent.\n")

    while True:

        user_input = input("Customer: ")

        if user_input.lower() == "exit":

            print("\nAgent stopped.")
            break

        response = generate_response(user_input)

        print(f"\nAgent: {response}\n")

        log_interaction(user_input, response)

# ----------------------------------------
# Run Application
# ----------------------------------------

if __name__ == "__main__":

    run_agent()
