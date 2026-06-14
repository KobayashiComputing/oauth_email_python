# ====================================================================
# Created by Microsoft's CoPilot AI via Bing.com using Edge
# using search "python oauth2 mail relay using outlook.com"
# ====================================================================

import asyncio
import base64
import os
import smtplib
from email.message import EmailMessage
from aiosmtpd.controller import Controller
from msal import PublicClientApplication, SerializableTokenCache

# -----------------------------
# CONFIGURATION
# -----------------------------
CLIENT_ID = "YOUR_APP_CLIENT_ID"       # Azure App Registration
TENANT_ID = "YOUR_TENANT_ID"           # 'common' or 'consumers' for personal
USERNAME = "your_outlook_email@example.com"
PASSWORD = "legacy_password_for_local_auth"  # For devices to connect to relay
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://outlook.office365.com/.default"]

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

TOKEN_CACHE_FILE = "msal_token_cache.bin"

# -----------------------------
# OAUTH2 TOKEN HANDLING
# -----------------------------
class OAuth2TokenManager:
    def __init__(self):
        self.cache = SerializableTokenCache()
        if os.path.exists(TOKEN_CACHE_FILE):
            try:
                self.cache.deserialize(open(TOKEN_CACHE_FILE, "r").read())
            except Exception:
                print("Warning: Could not read token cache, starting fresh.")

        self.app = PublicClientApplication(
            CLIENT_ID,
            authority=AUTHORITY,
            token_cache=self.cache
        )

    def save_cache(self):
        if self.cache.has_state_changed:
            with open(TOKEN_CACHE_FILE, "w") as f:
                f.write(self.cache.serialize())

    def get_access_token(self):
        # Try silent refresh
        accounts = self.app.get_accounts(username=USERNAME)
        if accounts:
            result = self.app.acquire_token_silent(SCOPES, account=accounts[0])
            if result and "access_token" in result:
                self.save_cache()
                return result["access_token"]

        # Interactive login (first time only)
        print("Opening browser for Microsoft login...")
        result = self.app.acquire_token_interactive(scopes=SCOPES, login_hint=USERNAME)
        if "access_token" in result:
            self.save_cache()
            return result["access_token"]
        else:
            raise Exception(f"Token error: {result.get('error_description')}")

    @staticmethod
    def generate_oauth2_string(username, access_token):
        auth_string = f"user={username}\x01auth=Bearer {access_token}\x01\x01"
        return base64.b64encode(auth_string.encode()).decode()

# -----------------------------
# SMTP RELAY HANDLER
# -----------------------------
class RelayHandler:
    def __init__(self, token_manager):
        self.token_manager = token_manager

    async def handle_DATA(self, server, session, envelope):
        print(f"Received message from {session.peer}")
        print(f"Message for: {envelope.rcpt_tos}")
        print(f"Message length: {len(envelope.content)} bytes")

        if not getattr(session, "authenticated", False):
            return "530 Authentication required"

        try:
            access_token = self.token_manager.get_access_token()
            auth_string = self.token_manager.generate_oauth2_string(USERNAME, access_token)

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.docmd("AUTH", "XOAUTH2 " + auth_string)
                smtp.sendmail(envelope.mail_from, envelope.rcpt_tos, envelope.content)

            print("Email relayed successfully.")
            return "250 Message accepted for delivery"
        except smtplib.SMTPAuthenticationError as e:
            print("SMTP Auth failed:", e.smtp_error.decode())
            return "535 Authentication failed"
        except Exception as e:
            print("Relay error:", str(e))
            return "451 Temporary local problem"

    async def handle_AUTH(self, server, session, envelope, mechanism, auth_data):
        if mechanism == "PLAIN":
            try:
                auth_decoded = base64.b64decode(auth_data).decode()
                _, username, password = auth_decoded.split("\x00")
                if username == USERNAME and password == PASSWORD:
                    session.authenticated = True
                    return "235 Authentication successful"
            except Exception:
                pass
        return "535 Authentication failed"

# -----------------------------
# MAIN ENTRY
# -----------------------------
if __name__ == "__main__":
    token_manager = OAuth2TokenManager()
    handler = RelayHandler(token_manager)
    controller = Controller(handler, hostname="0.0.0.0", port=2525)  # Local SMTP relay port
    print("Starting SMTP relay on port 2525...")
    controller.start()

    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("Stopping relay...")
        controller.stop()
        token_manager.save_cache()
