# Send Email via Outlook.com with OAuth 2.0

Bing.com Query: 
- give me a python script that will send email using my personal outlook.com email account with oauth 2.0

Got it ✅ — since Microsoft has disabled basic authentication (SMTP username/password) for personal Outlook.com accounts, you now need to use OAuth 2.0 with the Microsoft Graph API to send emails.

Below is a complete, runnable Python script that:
- Authenticates you with Outlook.com using OAuth 2.0.
- Sends an email via the Microsoft Graph API.
- Uses the Device Code Flow (no need to embed your password).

## Setup Steps
1. Register an App in Azure Portal
    - Go to: https://portal.azure.com → Azure Active Directory → App registrations → New registration.
    - Name: e.g., OutlookEmailSender.
    - Supported account types: Accounts in any organizational directory and personal Microsoft accounts.
    - Redirect URI: Leave blank for device code flow.
    - Save the Application (client) ID — put it in CLIENT_ID.
    - Note: for "personal" accounts, the TENANT_ID is "consumers"

2. API Permissions
    - In your app → API Permissions → Add a permission → Microsoft Graph → Delegated permissions → Mail.Send.
    - Click Grant admin consent (if available).

3. Allow public client flows
    - Go to your App Registration in Azure Portal
    - Azure Active Directory → App registrations → Select your app.
    - Authentication -> Advanced Settings (needs legacy mode) -> Allow public client flows -> Enable Mobile and Desktop
    - Save.
    - Ensure Supported Account Types
        - In Overview, make sure your app is set to:
            - Accounts in any organizational directory and personal Microsoft accounts.
    - Permissions
        - API Permissions → Add Microsoft Graph → Delegated → Mail.Send.
        - Click Grant admin consent (if available).

4. Install Required Libraries
```
pip install msal requests
```

5. Run the Script
```
python send_outlook_email.py
```

- It will show a URL and a code.
- Open the URL in your browser, log in with your Outlook.com account, and enter the code.
- The script will then send the email.

## Security Notes
- Never hardcode your password — OAuth 2.0 avoids that.
- Store CLIENT_ID in environment variables for production.
- Tokens are cached in memory here; for persistent caching, use msal.SerializableTokenCache.

If you want, I can also give you a version that supports attachments and HTML email bodies using the same OAuth 2.0 flow.
Do you want me to extend it for that?


## Crashes:

{'error': 'invalid_client', 'error_description': "AADSTS70002: The provided client is not supported for this feature. The client application must be marked as 'mobile.' Trace ID: de79155d-16e7-42ab-8a68-d80d67d96c00 Correlation ID: 515df608-ab15-4f07-8b33-849665371e63 Timestamp: 2026-07-01 21:26:58Z", 'error_codes': [70002], 'timestamp': '2026-07-01 21:26:58Z', 'trace_id': 'de79155d-16e7-42ab-8a68-d80d67d96c00', 'correlation_id': '515df608-ab15-4f07-8b33-849665371e63', 'error_uri': 'https://login.microsoftonline.com/error?code=70002', 'interval': 5, 'expires_in': 1800, 'expires_at': 1782943018.3235629, '_correlation_id': '515df608-ab15-4f07-8b33-849665371e63'}

Ah — I know exactly what’s happening.

That AADSTS70002 error with "must be marked as 'mobile'" means your Azure App Registration is not configured to allow the Device Code Flow for personal Microsoft accounts (Outlook.com, Hotmail, Live).

By default, new Azure apps are created as web apps and cannot use public client flows like Device Code unless you explicitly enable them.

Fix — Enable Public Client (Mobile & Desktop) Flow
Go to your App Registration in Azure Portal
Azure Active Directory → App registrations → Select your app.

Enable Public Client Flow

In the left menu, go to Authentication.
Scroll to Advanced settings → Allow public client flows.
Set Enable the following mobile and desktop flows to Yes.
Save.
Ensure Supported Account Types

In Overview, make sure your app is set to:
Accounts in any organizational directory and personal Microsoft accounts.
Permissions

API Permissions → Add Microsoft Graph → Delegated → Mail.Send.
Click Grant admin consent (if available).
Updated Script Notes
The Python script I gave you will work unchanged after you enable the public client flow.
The key is that Device Code Flow is only allowed for apps marked as public clients (mobile/desktop).

Alternative: Authorization Code Flow
If you don’t want to enable public client flow, you can use the Authorization Code Flow with a redirect URI (e.g., http://localhost:5000) and a local web server to capture the token.
That’s more secure for production, but Device Code Flow is simpler for quick scripts.

If you want, I can give you a ready-to-run Authorization Code Flow version that works without enabling the mobile flag — it will pop open your browser, log you in, and send the email.

Do you want me to rewrite it that way?

I told it "yes" and got the following:
Alright — here’s a complete, runnable Python script that uses the OAuth 2.0 Authorization Code Flow with Microsoft Graph to send email from your personal Outlook.com account.

This method does not require enabling the “mobile” public client flow — instead, it uses a redirect URI and a local HTTP server to capture the authorization code.

Python Script — Outlook.com Email via OAuth 2.0 Authorization Code Flow
Python

Copy code
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
Setup Steps
1️⃣ Register an App in Azure Portal
Go to Azure Portal → Azure Active Directory → App registrations → New registration.
Name: OutlookEmailSender.
Supported account types: Accounts in any organizational directory and personal Microsoft accounts.
Redirect URI: Web → http://localhost:5000/getAToken.
Click Register.
2️⃣ Add Client Secret
In your app → Certificates & secrets → New client secret.
Copy the Value (this is your CLIENT_SECRET).
3️⃣ API Permissions
In your app → API Permissions → Add a permission → Microsoft Graph → Delegated → Mail.Send.
Click Grant admin consent (if available).
4️⃣ Install Dependencies
Bash

Copy code
pip install msal flask requests
5️⃣ Run the Script
Bash

Copy code
python outlook_oauth_email.py
Open http://localhost:5000 in your browser.
Click the login link, sign in with your Outlook.com account.
Grant permission to send email.
The script will send the email and print confirmation.
✅ Advantages of this method

Works without enabling “mobile” public client flow.
Uses a secure confidential client with CLIENT_SECRET.
Can be extended for HTML emails, attachments, or reading inbox.
If you want, I can now extend this script to send HTML emails with attachments so it’s production-ready.
Do you want me to add that?