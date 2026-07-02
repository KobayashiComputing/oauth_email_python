# Send Outlook.com Email with Token Cache and Silent Refresh

> Source File: send_outlook_email_with_token_cache_and_refresh.py

Got it ✅ — since Microsoft has disabled basic authentication (SMTP with username/password) for personal Outlook.com accounts, you now need to use OAuth 2.0 with the Microsoft Graph API to send emails.

Below is a complete, runnable Python script that:
- Authenticates with OAuth 2.0 using MSAL (Microsoft Authentication Library)
- Saves the token to a local file for reuse
- Sends an email via your Outlook.com account using the Microsoft Graph API

Alright — I’ll extend the script so that it automatically refreshes the token silently whenever possible, without prompting you again until the refresh token expires.

The key changes are:
- Store the full MSAL token cache (not just the access token) in a file.
- Use acquire_token_silent() with the stored account to refresh automatically.
- Only fall back to device code flow if the refresh token is expired or missing.


Updated Python Script — Outlook.com Email with Auto Token Refresh

## What’s New in This Version
1. Persistent Token Cache
- Uses msal.SerializableTokenCache() to store access + refresh tokens in msal_cache.json.
- This allows silent refresh without re-login until the refresh token expires (usually 90 days for personal accounts).

2. Silent Refresh First
- Checks for existing accounts in the cache.
- Calls acquire_token_silent() to refresh automatically.
- Falls back to device code flow only if needed.

3. No Manual Token Management
- You don’t need to manually save/load tokens — MSAL handles it.

## Setup Steps
1. Register an App in Azure Portal
    - Go to: https://portal.azure.com → Azure Active Directory → App registrations → New registration.
    - Name: e.g., OutlookEmailSender.
    - Supported account types: Accounts in any organizational directory and personal Microsoft accounts.
    - Redirect URI: Leave blank for device code flow.
    - Save the Application (client) ID — put it in CLIENT_ID.

2. API Permissions
    - In your app → API Permissions → Add a permission → Microsoft Graph → Delegated permissions → Mail.Send.
    - Click Grant admin consent (if available).

3. Allow public client flows
    - Go to your App Registration in Azure Portal
    - Azure Active Directory → App registrations → Select your app.

    - Enable Public Client Flow

    - In the left menu, go to Authentication.
    - Scroll to Advanced settings → Allow public client flows.
    - Set Enable the following mobile and desktop flows to Yes.
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

- First run: prompts for device code login.
    - It will show a URL and a code.
    - Open the URL in your browser, log in with your Outlook.com account, and enter the code.
- Later runs: refreshes silently.
- The script will then send the email.

## Security Notes
- Never hardcode your password — OAuth 2.0 avoids that.
- Store CLIENT_ID in environment variables for production.
- Tokens are cached in memory here; for persistent caching, use msal.SerializableTokenCache.
