import os
import json
import msal
import requests
import os
from dotenv import load_dotenv

localDirPath = os.path.dirname(os.path.abspath(__file__))
envFilePath = localDirPath + "/" +".env"
load_dotenv(dotenv_path=envFilePath)

# ----------------------------
# CONFIGURATION - EDIT THESE
# ----------------------------
CLIENT_ID = os.getenv('CLIENT_ID')  # From Azure App Registration
TENANT_ID = "consumers"  # For personal Microsoft accounts
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/Mail.Send"]
TOKEN_CACHE_FILE = localDirPath + "/" + "msal_cache.json"

# ----------------------------
# Load MSAL token cache from file
# ----------------------------
def load_cache():
    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKEN_CACHE_FILE):
        with open(TOKEN_CACHE_FILE, "r") as f:
            cache.deserialize(f.read())
    return cache

# ----------------------------
# Save MSAL token cache to file
# ----------------------------
def save_cache(cache):
    if cache.has_state_changed:
        with open(TOKEN_CACHE_FILE, "w") as f:
            f.write(cache.serialize())

# ----------------------------
# Get an access token (silent refresh if possible)
# ----------------------------
def get_access_token():
    cache = load_cache()
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

    accounts = app.get_accounts()
    if accounts:
        # Try silent refresh
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            save_cache(cache)
            return result["access_token"]

    # If silent refresh fails, use device code flow
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise ValueError("Failed to create device flow. Check CLIENT_ID and internet connection.")

    print(f"Please go to {flow['verification_uri']} and enter the code: {flow['user_code']}")
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        save_cache(cache)
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
            recipient="andy@slowlanecafe.com",
            subject="Test Email with Auto Token Refresh",
            body="Hello! This email was sent via Outlook.com with OAuth 2.0 and automatic token refresh."
        )
    except Exception as e:
        print(f"Error: {e}")
