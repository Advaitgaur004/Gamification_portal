import os
import gspread
from typing import List

def initialize_gspread() -> gspread.client.Client:
    """
    Initialize a gspread client with the given credentials.
    """
    credentials = get_credentials()
    return gspread.service_account_from_dict(credentials)

def get_credentials() -> dict:
    """
    Return gspread credentials.
    """
    return {
        "type": os.getenv("TYPE"),
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        "private_key": os.getenv("PRIVATE_KEY"),
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
        "universe_domain": os.getenv("UNIVERSE_DOMAIN")
    }

def get_enrolled_students(sheet_name: str, worksheet_name: str) -> List[str]:
    """
    Fetches enrolled students from a given Google Sheet worksheet and returns them as a list.
    """
    credentials = get_credentials()
    client = gspread.service_account_from_dict(credentials)
    sh = client.open(sheet_name)
    worksheet = sh.worksheet(worksheet_name) if worksheet_name else sh.get_worksheet(0)
    
    # Get all rows from the worksheet
    rows = worksheet.get_all_records()
    
    # Extract student IDs from the rows
    student_ids = [row['Enrolled Students'] for row in rows if 'Enrolled Students' in row]
    
    return student_ids
