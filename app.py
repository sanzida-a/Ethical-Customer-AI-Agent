import os
import re
import json
import random
import datetime
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# --- Input Guardrails ---
def input_guardrail(query: str) -> bool:
    """Check if the query is within scope (customer support related)."""
    blocked_keywords = [
        "politics", "medical", "health", "disease", "harm", "violence",
        "illegal", "hack", "offensive", "adult", "religion"
    ]
    query_lower = query.lower()
    return not any(keyword in query_lower for keyword in blocked_keywords)

# --- Output Guardrails ---
def output_guardrail(response: str) -> str:
    """Ensure response is safe, professional, and clear."""
    response = re.sub(r'\b(hate|offensive|inappropriate)\b', '', response, flags=re.IGNORECASE)
    if not response.endswith('.'):
        response += '.'
    return response

# --- Knowledge Base Tool ---
knowledge_base = {
    "internet speeds": "Available internet speed packages: 10 Mbps ($20/month), 50 Mbps ($40/month), 100 Mbps ($60/month).",
    "working hours": "Our working hours are 9 AM to 6 PM, Monday through Friday.",
    "refund policy": "We offer a full refund for service downtime exceeding 7 days.",
    "billing": "Billing is monthly; payments are due on the 1st of each month.",
    "contact support": "Contact us via email at support@company.com or call 1-800-123-4567."
}

def knowledge_base_tool(query: str) -> str:
    """Fetch answer from the knowledge base."""
    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value
    return "Sorry, I couldn't find information on that topic. Please ask about our services."

# --- Complaint Ticket Tool ---
human_agents = ["Rahim", "Sara", "John"]

def categorize_complaint(complaint: str) -> str:
    complaint_lower = complaint.lower()
    if any(word in complaint_lower for word in ["urgent", "emergency", "down", "outage"]):
        return "High"
    elif any(word in complaint_lower for word in ["slow", "issue", "problem"]):
        return "Medium"
    else:
        return "Low"

def generate_ticket_id() -> str:
    return f"TICKET-{random.randint(1000, 9999)}"

def complain_ticket_tool(complaint: str, user_name: str) -> dict:
    severity = categorize_complaint(complaint)
    ticket_id = generate_ticket_id()
    assigned_agent = random.choice(human_agents)
    return {
        "ticket_id": ticket_id,
        "user_name": user_name,
        "complaint": complaint,
        "severity": severity,
        "assigned_agent": assigned_agent,
        "date_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# --- Google Sheet Tool ---
def google_sheet_tool(ticket_data: dict) -> str:
    """Log complaint details to Google Sheet."""
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"), scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(os.getenv("GOOGLE_SHEET_ID")).sheet1
        row = [
            ticket_data["ticket_id"],
            ticket_data["user_name"],
            ticket_data["complaint"],
            ticket_data["severity"],
            ticket_data["assigned_agent"],
            ticket_data["date_time"]
        ]
        sheet.append_row(row)
        return f"Complaint logged successfully with Ticket ID: {ticket_data['ticket_id']}."
    except Exception as e:
        return f"Failed to log complaint to Google Sheet: {str(e)}"

# --- Main Processing Function ---
def process_query(query: str, user_name: str = "Anonymous") -> str:
    if not input_guardrail(query):
        return output_guardrail(
            "I'm sorry, but I can only assist with customer support-related queries. "
            "Please ask about our services or submit a complaint."
        )

    if "complain" in query.lower() or any(word in query.lower() for word in ["issue", "problem", "down", "slow"]):
        ticket_data = complain_ticket_tool(query, user_name)
        google_sheet_tool(ticket_data)
        response = (f"Your complaint has been logged as {ticket_data['severity']} priority. "
                    f"Agent {ticket_data['assigned_agent']} will follow up shortly. "
                    f"Ticket ID: {ticket_data['ticket_id']}.")
    else:
        response = knowledge_base_tool(query)

    return output_guardrail(response)

# --- Interactive Terminal Input ---
if __name__ == "__main__":
    print("Welcome to the Customer Support AI Agent!")
    print("Type 'exit' to quit.\n")

    user_name = input("Enter your name: ") or "Anonymous"

    while True:
        query = input("\nEnter your query: ")
        if query.lower() == "exit":
            print("Goodbye!")
            break
        response = process_query(query, user_name)
        print(f"Response: {response}")
