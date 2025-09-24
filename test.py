import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Test Google Sheets connection
try:
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"), scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(os.getenv("GOOGLE_SHEET_ID")).sheet1
    sheet.append_row(["TEST", "Test User", "Test complaint", "Low", "Test Agent", "2025-09-24 23:00:00"])
    logging.info("Test row appended successfully.")
    print("Test row appended successfully.")
except Exception as e:
    logging.error(f"Failed to append to Google Sheet: {str(e)}")
    print(f"Error: {str(e)}")