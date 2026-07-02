import os
import json
import msal
import requests

# ----------------------------
# CONFIGURATION - EDIT THESE
# ----------------------------
CLIENT_ID = "YOUR_APP_CLIENT_ID"  # From Azure App Registration
TENANT_ID = "consumers"  # For personal Microsoft accounts
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/Mail.Send"]
TOKEN_FILE = "msal_token.json"

# ----------------------------
# Load token from file if exists
# ----------------------------
def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None

# ----------------------------
# Save token to file
# ----------------------------
def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        json.dump(token, f)

# ----------------------------
# Get an access token (interactive if needed)
# ----------------------------
def get_access_token():
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

    # Try to load existing token
    token_data = load_token()
    if token_data:
        result = app.acquire_token_silent(SCOPES, account=None)
        if result:
            return result["access_token"]

    # Interactive login if no valid token
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise ValueError("Failed to create device flow. Check your CLIENT_ID and internet connection.")

    print(f"Please go to {flow['verification_uri']} and enter the code: {flow['user_code']}")
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        save_token(result)
        return result["access_token"]
    else:
        raise ValueError(f"Failed to obtain token: {result.get('error_description')}")

# ----------------------------
# Send email using Microsoft Graph API
# ----------------------------
def send_email(access_token, recipient, subject, body):
    endpoint = "https://graph.microsoft.com/v1.0/me/sendMail"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    email_msg = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {"emailAddress": {"address": recipient}}
            ]
        }
    }
    response = requests.post(endpoint, headers=headers, json=email_msg)
    if response.status_code == 202:
        print("✅ Email sent successfully!")
    else:
        print(f"❌ Failed to send email: {response.status_code} {response.text}")

# ----------------------------
# MAIN EXECUTION
# ----------------------------
if __name__ == "__main__":
    try:
        token = get_access_token()
        send_email(
            token,
            recipient="recipient@example.com",
            subject="Test Email from Python",
            body="Hello! This is a test email sent via Outlook.com and OAuth 2.0."
        )
    except Exception as e:
        print(f"Error: {e}")
