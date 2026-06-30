import json
import requests
import msal

# ---------------- CONFIGURATION ----------------
CLIENT_ID = "YOUR_CLIENT_ID"       # From Azure App Registration
TENANT_ID = "YOUR_TENANT_ID"       # From Azure App Registration
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/Mail.Send"]

# Create a public client application (no secret needed for device code flow)
app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

# Step 1: Get device code
flow = app.initiate_device_flow(scopes=SCOPES)
if "user_code" not in flow:
    raise ValueError("Failed to create device flow. Check your app registration.")

print(f"🔑 Go to {flow['verification_uri']} and enter the code: {flow['user_code']}")

# Step 2: Wait for user to authenticate
result = app.acquire_token_by_device_flow(flow)  # This will block until login is complete

if "access_token" in result:
    print("✅ Authentication successful!")

    # Step 3: Prepare email payload
    email_msg = {
        "message": {
            "subject": "Hello from Python via Outlook OAuth 2.0 (Device Code Flow)",
            "body": {
                "contentType": "Text",
                "content": "This is a test email sent using Microsoft Graph API and OAuth 2.0 device code flow!"
            },
            "toRecipients": [
                {"emailAddress": {"address": "recipient@example.com"}}
            ]
        }
    }

    # Step 4: Send email
    response = requests.post(
        "https://graph.microsoft.com/v1.0/me/sendMail",
        headers={
            "Authorization": f"Bearer {result['access_token']}",
            "Content-Type": "application/json"
        },
        data=json.dumps(email_msg)
    )

    if response.status_code == 202:
        print("📧 Email sent successfully!")
    else:
        print(f"❌ Failed to send email: {response.status_code} {response.text}")

else:
    print(f"❌ Authentication failed: {result.get('error_description')}")
