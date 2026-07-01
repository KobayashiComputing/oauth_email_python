import os
import json
import requests
from msal import PublicClientApplication
from types import SimpleNamespace
from dotenv import load_dotenv

# ---------------- ENVIRONMENT ------------------
pDirName = "oauth_email_python"
eDirName = "env"
sDir = os.path.dirname(os.path.abspath(__file__))
eDirNdx = sDir.find(pDirName) + len(pDirName)
eDir = sDir[0:eDirNdx] + "/" + eDirName

# Token is cached for reuse  
token_path = os.path.join(eDir, 'outlook_token_cache_02.json')

# Outlook.com Azure tenant info file
tenant_info_path = os.path.join(eDir, 'ms_desktop_client_02.json')

load_dotenv()

obj = SimpleNamespace()

try:
    # Read and parse JSON from file
    with open(tenant_info_path, "r") as f:
        obj = json.load(f, object_hook=SimpleNamespace)
except FileNotFoundError:
    print("File not found.")
    exit(1)
except json.JSONDecodeError as e:
    print("Error parsing JSON file:", e)
    exit(1)
except Exception as e:
    print("Unexpected error:", e)
    exit(1)

print("\nParsed from file as well:")
print("     Tenant ID: ", obj.installed.tenant_id)
print("     Client ID: ", obj.installed.client_id)


# ---------------- CONFIGURATION ----------------
CLIENT_ID = obj.installed.client_id     # From Azure App Registration
TENANT_ID = obj.installed.tenant_id     # From Azure App Registration
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/Mail.Send"]

# Create a public client application (no secret needed for device code flow)
app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

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
