import json
import requests
import msal

# ---------------- CONFIGURATION ----------------
CLIENT_ID = "YOUR_CLIENT_ID"       # From Azure App Registration
TENANT_ID = "YOUR_TENANT_ID"       # From Azure App Registration
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/Mail.Send"]

def authenticate():
    """Authenticate user via Device Code Flow and return access token."""
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise ValueError("Failed to create device flow. Check your app registration.")

    print(f"\n🔑 Go to {flow['verification_uri']} and enter the code: {flow['user_code']}")
    print("Waiting for you to sign in...\n")

    result = app.acquire_token_by_device_flow(flow)
    if "access_token" in result:
        print("✅ Authentication successful!\n")
        return result["access_token"]
    else:
        raise RuntimeError(f"Authentication failed: {result.get('error_description')}")

def send_email(access_token, recipient, subject, body):
    """Send an email using Microsoft Graph API."""
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

    response = requests.post(
        "https://graph.microsoft.com/v1.0/me/sendMail",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        data=json.dumps(email_msg)
    )

    if response.status_code == 202:
        print("📧 Email sent successfully!")
    else:
        print(f"❌ Failed to send email: {response.status_code} {response.text}")

if __name__ == "__main__":
    try:
        # Step 1: Authenticate
        token = authenticate()

        # Step 2: Get email details from user
        recipient = input("Enter recipient email: ").strip()
        subject = input("Enter subject: ").strip()
        print("Enter email body (end with an empty line):")
        body_lines = []
        while True:
            line = input()
            if line == "":
                break
            body_lines.append(line)
        body = "\n".join(body_lines)

        # Step 3: Send email
        send_email(token, recipient, subject, body)

    except Exception as e:
        print(f"⚠️ Error: {e}")
