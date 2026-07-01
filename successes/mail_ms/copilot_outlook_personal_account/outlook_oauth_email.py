import json
import requests
import msal
from flask import Flask, request

# -------------------------------
# CONFIGURATION - EDIT THESE
# -------------------------------
CLIENT_ID = "YOUR_APP_CLIENT_ID"  # From Azure App Registration
CLIENT_SECRET = "YOUR_APP_CLIENT_SECRET"  # From Azure App Registration
TENANT_ID = "consumers"  # 'consumers' for personal Microsoft accounts
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/Mail.Send"]
REDIRECT_URI = "http://localhost:5000/getAToken"

# Email details
RECIPIENT = "recipient@example.com"
SUBJECT = "Test Email from Python via Outlook OAuth 2.0"
BODY_TEXT = "Hello! This is a test email sent using Microsoft Graph API and OAuth 2.0 Authorization Code Flow."

# -------------------------------
# FLASK APP TO HANDLE REDIRECT
# -------------------------------
app = Flask(__name__)
token_cache = None  # Will store token after login


@app.route("/")
def homepage():
    """Step 1: Redirect user to Microsoft login page."""
    auth_app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    auth_url = auth_app.get_authorization_request_url(
        SCOPES, redirect_uri=REDIRECT_URI
    )
    return f'<a href="{auth_url}">Click here to log in with Outlook.com</a>'


@app.route("/getAToken")
def authorized():
    """Step 2: Microsoft redirects here with ?code=..."""
    global token_cache
    code = request.args.get("code")
    if not code:
        return "No authorization code returned."

    auth_app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )
    result = auth_app.acquire_token_by_authorization_code(
        code, scopes=SCOPES, redirect_uri=REDIRECT_URI
    )

    if "access_token" in result:
        token_cache = result
        send_email(result["access_token"])
        return "✅ Email sent successfully! You can close this window."
    else:
        return f"❌ Authentication failed: {result.get('error_description')}"


# -------------------------------
# SEND EMAIL FUNCTION
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
    print("Starting local server at http://localhost:5000 ...")
    print("Open this URL in your browser to log in and send the email.")
    app.run(port=5000)
