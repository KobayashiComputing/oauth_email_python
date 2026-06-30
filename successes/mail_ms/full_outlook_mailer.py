import json
import os
import base64
import mimetypes
import requests
import msal
from types import SimpleNamespace
from dotenv import load_dotenv

# ---------------- ENVIRONMENT ------------------
pDirName = "oauth_email_python"
eDirName = "env"
sDir = os.path.dirname(os.path.abspath(__file__))
eDirNdx = sDir.find(pDirName) + len(pDirName)
eDir = sDir[0:eDirNdx] + "/" + eDirName

# Token is cached for reuse  
token_path = os.path.join(eDir, 'outlook_token_cache.json')

# Outlook.com Azure tenant info file
tenant_info_path = os.path.join(eDir, 'ms_desktop_client_01.json')

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
SCOPES = ["https://graph.microsoft.com/Mail.Send", "https://graph.microsoft.com/User.Read"]
TOKEN_CACHE_FILE = token_path

# ---------------- TOKEN CACHE ----------------
def load_cache():
    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKEN_CACHE_FILE):
        with open(TOKEN_CACHE_FILE, "r") as f:
            cache.deserialize(f.read())
    return cache

def save_cache(cache):
    if cache.has_state_changed:
        with open(TOKEN_CACHE_FILE, "w") as f:
            f.write(cache.serialize())

# ---------------- AUTHENTICATION ----------------
def authenticate():
    cache = load_cache()
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            print("✅ Using cached token.")
            save_cache(cache)
            return result["access_token"]

    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise ValueError("Failed to create device flow. Check your app registration.")

    print(f"\n🔑 Go to {flow['verification_uri']} and enter the code: {flow['user_code']}")
    print("Waiting for you to sign in...\n")

    result = app.acquire_token_by_device_flow(flow)
    if "access_token" in result:
        print("✅ Authentication successful!\n")
        save_cache(cache)
        return result["access_token"]
    else:
        raise RuntimeError(f"❌ Authentication failed: {result.get('error_description')}")

# ---------------- EMAIL SENDER ----------------
def create_attachment(file_path):
    """Create a Microsoft Graph API attachment object from a local file."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Attachment not found: {file_path}")

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"

    with open(file_path, "rb") as f:
        content_bytes = f.read()

    return {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": os.path.basename(file_path),
        "contentType": mime_type,
        "contentBytes": base64.b64encode(content_bytes).decode("utf-8")
    }

def send_email(access_token, recipient, subject, body, is_html=False, attachments=None):
    """Send an email with optional HTML and attachments."""
    message = {
        "subject": subject,
        "body": {
            "contentType": "HTML" if is_html else "Text",
            "content": body
        },
        "toRecipients": [
            {"emailAddress": {"address": recipient}}
        ]
    }

    if attachments:
        message["attachments"] = attachments

    email_msg = {"message": message}

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

# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    try:
        token = authenticate()

        recipient = input("Enter recipient email: ").strip()
        subject = input("Enter subject: ").strip()

        mode = input("Send as HTML? (y/n): ").strip().lower()
        is_html = mode == "y"

        print("Enter email body (end with a blank line):")
        body_lines = []
        while True:
            line = input()
            if line == "":
                break
            body_lines.append(line)
        body = "\n".join(body_lines)

        attach_files = input("Add attachments? (y/n): ").strip().lower()
        attachments = []
        if attach_files == "y":
            while True:
                file_path = input("Enter file path (or leave blank to finish): ").strip()
                if not file_path:
                    break
                try:
                    attachments.append(create_attachment(file_path))
                    print(f"✅ Added attachment: {file_path}")
                except Exception as e:
                    print(f"❌ Could not add attachment: {e}")

        send_email(token, recipient, subject, body, is_html, attachments if attachments else None)

    except Exception as e:
        print(f"Error: {e}")
