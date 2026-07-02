import msal
import requests
import json
import sys
import os
from dotenv import load_dotenv

localDirPath = os.path.dirname(os.path.abspath(__file__))
envPath = localDirPath + "/env"
envFilePath = envPath + "/" +".env"
load_dotenv(dotenv_path=envFilePath)

# -------------------------------
# CONFIGURATION - EDIT THESE
# -------------------------------
CLIENT_ID = os.getenv('CLIENT_ID')  # From Azure App Registration
TENANT_ID = "consumers"  # 'consumers' for personal Outlook.com accounts
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/Mail.Send"]

# Email details
SENDER = "kobayashicomputing@outlook.com"
RECIPIENT = "andy@slowlanecafe.com"
SUBJECT = "Test Email from Python via Outlook OAuth 2.0"
BODY_TEXT = "Hello! This is a test email sent using Microsoft Graph API and OAuth 2.0."

# -------------------------------
# AUTHENTICATION
# -------------------------------
def get_access_token():
    """Authenticate using Device Code Flow and return an access token."""
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

    # Try to get token from cache first
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result:
            return result["access_token"]

    # If no cached token, start device code flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        print("Failed to create device flow. Check your CLIENT_ID.")
        sys.exit(1)

    print(f"Go to {flow['verification_uri']} and enter the code: {flow['user_code']}")
    sys.stdout.flush()

    result = app.acquire_token_by_device_flow(flow)     # this blocks until a return is received
    if "access_token" in result:
        return result["access_token"]
    else:
        print("Authentication failed:", result.get("error_description"))
        sys.exit(1)

# -------------------------------
# SEND EMAIL
# -------------------------------
def send_email(access_token):
    """Send an email using Microsoft Graph API."""
    endpoint = "https://graph.microsoft.com/v1.0/me/sendMail"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    email_msg = {
        "message": {
            "subject": SUBJECT,
            "body": {
                "contentType": "Text",
                "content": BODY_TEXT
            },
            "toRecipients": [
                {"emailAddress": {"address": RECIPIENT}}
            ]
        }
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(email_msg))
    if response.status_code == 202:
        print("✅ Email sent successfully!")
    else:
        print(f"❌ Failed to send email: {response.status_code} - {response.text}")

# -------------------------------
# MAIN EXECUTION
# -------------------------------
if __name__ == "__main__":
    token = get_access_token()
    send_email(token)
