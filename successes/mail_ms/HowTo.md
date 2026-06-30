# Perfect ✅ — here’s a terminal-only Python example to send an email from an Outlook.com account using OAuth 2.0 and the Device Code Flow (no Flask, no redirect).

This is great for quick testing or scripts running locally.

## Steps Before Running
1. Register an app in Azure App Registrations
    - Supported account types: Accounts in any organizational directory and personal Microsoft accounts
    - Redirect URI: None needed for device code flow
    - API Permissions: Add Mail.Send (Delegated) and grant admin consent if needed.
        - API Permissions -> Microsoft Graph -> Delegated -> search for "Mail.send"
    - Copy Client ID and Tenant ID.

2. Install dependencies:
```
pip install msal requests
```

3. See code in 'send_md_oauth2.py'

## How It Works
1. Device Code Flow:
    - Script prints a URL and code.
    - You open the URL in a browser, enter the code, and log in with your Outlook.com account.

2. Access Token:
    - Script waits until you finish logging in.
    - Microsoft returns an access token.

3. Send Email:
    - Script sends the email via Microsoft Graph API.

## Notes
- No CLIENT_SECRET is needed for device code flow.
- Works with personal Outlook.com and Microsoft 365 accounts.
- Make sure Mail.Send permission is granted in Azure.

If you want, I can also give you a version that reads the recipient, subject, and body from the terminal so you can send custom emails interactively.
That would make it more like a mini command-line Outlook mailer.

Do you want me to make that interactive version?