# Customer Support AI Agent

This project implements a **Customer Support AI Agent** using Python and LangChain.  
The agent interacts safely with users, answers service-related questions, handles complaints, and logs them in a Google Sheet.  

- **View logged complaints:** [Google Sheet Link](https://docs.google.com/spreadsheets/d/1qm7H3mHC97-N1ghFUb9cw3wDBnQgJxrfB44vFZXVGQY/edit?usp=sharing)

---

## 1. Guardrail Design

### Input Guardrails
- Filters incoming queries to ensure they are within the scope of **customer support**.
- Blocks or rejects queries containing keywords related to:  
  `politics, medical, health, disease, harm, violence, illegal, hack, offensive, adult, religion`.
- Out-of-scope queries are politely rejected:  
  > "I'm sorry, but I can only assist with customer support-related queries. Please ask about our services or submit a complaint."

### Output Guardrails
- Ensures all responses are **safe, professional, and free from bias**.
- Removes inappropriate words (like “hate”, “offensive”, “inappropriate”).
- Ensures responses end with proper punctuation and are clear.

---

## 2. Tools

### 1. Knowledge Base Tool
- Handles frequently asked questions about company services.
- Example data:
  - Internet speeds: 10 Mbps, 50 Mbps, 100 Mbps.
  - Working hours: 9 AM – 6 PM (Mon–Fri).
  - Refund policy: 7 days for service downtime.
  - Billing info and contact info.
- Fetches answers for service-related questions.

### 2. Complain Ticket Tool
- Handles complaints from users.
- Classifies complaint severity:
  - **High:** urgent issues, outages.
  - **Medium:** issues affecting service but not critical.
  - **Low:** minor issues.
- Generates a unique **ticket ID**.
- Assigns complaints to predefined human agents: **Rahim, Sara, John**.
- Returns complaint details including complaint text, severity, assigned agent, date/time, user name.

### 3. Google Sheet Tool
- Logs complaint data into a Google Sheet with columns:
  - Complaint ID  
  - User Name  
  - Complaint Description  
  - Category (Low/Medium/High)  
  - Assigned Agent  
  - Date/Time  


---

## 3. Example User-Agent Conversations

### Service Questions
**User:** "What internet speeds do you provide?"  
**Agent:** "Available internet speed packages: 10 Mbps ($20/month), 50 Mbps ($40/month), 100 Mbps ($60/month)."

**User:** "What are your working hours?"  
**Agent:** "Our working hours are 9 AM to 6 PM, Monday through Friday."

### Complaints
**User:** "I want to complain about slow internet."  
**Agent:** "Your complaint has been logged as Medium priority. Agent Rahim will follow up shortly. Ticket ID: TICKET-4821."

**User:** "My internet is down since yesterday."  
**Agent:** "Your complaint has been logged as High priority. Agent Sara will follow up shortly. Ticket ID: TICKET-7392."

### Out-of-Scope Queries
**User:** "Tell me about politics."  
**Agent:** "I'm sorry, but I can only assist with customer support-related queries. Please ask about our services or submit a complaint."

---

## 4. Setup Instructions

1. Clone the repository.  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Set environment variables in .env:
    ```bash
    GOOGLE_SERVICE_ACCOUNT_JSON=path/to/service_account.json
    GOOGLE_SHEET_ID=your_google_sheet_id
    GEMINI_API_KEY=your_google_api_key
4. Run the agent interactively:
   ```bash
     python app.py
5. Enter queries in the terminal. The agent responds according to guardrails and tools.

## 5. Notes

-Ensure your Google Sheet is shared with the service account email.
-The agent assigns complaints randomly to one of the three predefined agents.
-All outputs are filtered for safe and professional communication.
