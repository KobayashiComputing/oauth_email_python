[W3Tutorials.net](https://www.w3tutorials.net/)

- [Home](https://www.w3tutorials.net/)
- [Online Go Compiler](https://www.w3tutorials.net/online-go-compiler/)

Last Updated: Mar 21, 2026

# Python smtplib: Is Sending Gmail via OAuth2 Possible? \[Explained\]

Sending emails programmatically is a common task in Python, whether for automating notifications, transactional emails, or batch communications. For years, developers relied on `smtplib`—Python’s built-in library for Simple Mail Transfer Protocol (SMTP)—to send emails via Gmail using username-password authentication. However, Google has increasingly tightened security measures, phasing out "Less Secure Apps" access and requiring stronger authentication methods.

One of the most secure and recommended alternatives is **OAuth2**, an open authorization framework that allows apps to access user data without exposing passwords. But can you use `smtplib` with OAuth2 to send Gmail?

**Short answer: Yes!** This blog will guide you through the entire process, from understanding OAuth2 to implementing it with `smtplib` for secure Gmail delivery. We’ll cover setup, code examples, troubleshooting, and alternatives to ensure you can send emails safely and reliably.

## Table of Contents[#](#table-of-contents)

1.  [What is OAuth2 and Why It Matters for Gmail?](#what-is-oauth2-and-why-it-matters-for-gmail)
2.  [Prerequisites](#prerequisites)
3.  [Step-by-Step Guide: Sending Gmail with OAuth2 and smtplib](#step-by-step-guide-sending-gmail-with-oauth2-and-smtplib)
    - 3.1 [Set Up a Google Cloud Project](#31-set-up-a-google-cloud-project)
    - 3.2 [Enable the Gmail API](#32-enable-the-gmail-api)
    - 3.3 [Configure the OAuth Consent Screen](#33-configure-the-oauth-consent-screen)
    - 3.4 [Create OAuth2 Client ID Credentials](#34-create-oauth2-client-id-credentials)
    - 3.5 [Install Required Libraries](#35-install-required-libraries)
    - 3.6 [Obtain and Store OAuth2 Tokens](#36-obtain-and-store-oauth2-tokens)
    - 3.7 [Send Email with smtplib and OAuth2](#37-send-email-with-smtplib-and-oauth2)
4.  [Common Issues and Troubleshooting](#common-issues-and-troubleshooting)
5.  [Alternatives to smtplib for OAuth2](#alternatives-to-smtplib-for-oauth2)
6.  [Conclusion](#conclusion)
7.  [References](#references)

## What is OAuth2 and Why It Matters for Gmail?[#](#what-is-oauth2-and-why-it-matters-for-gmail)

### What is OAuth2?[#](#what-is-oauth2)

OAuth2 (Open Authorization 2.0) is an industry-standard protocol for **secure authorization**. Unlike traditional password-based authentication—where you share your Gmail password with an app—OAuth2 uses **access tokens** to grant limited access to your account. Tokens are short-lived, revocable, and specific to the app and permissions (e.g., "only send emails"), making them far more secure.

### Why Gmail Requires OAuth2[#](#why-gmail-requires-oauth2)

In 2019, Google deprecated "Less Secure Apps" (LSA) access, which allowed apps to use your Gmail password directly. Since May 2022, LSA is fully disabled for all Google accounts. Today, to send emails via Gmail programmatically, you must use:

- **OAuth2** (recommended for most apps), or
- **App Passwords** (only for accounts with 2-Step Verification enabled, but this is being phased out).

OAuth2 is the future-proof, secure choice. It ensures your password is never exposed, and you retain granular control over app permissions.

## Prerequisites[#](#prerequisites)

Before diving in, ensure you have:

- A **Google account** (personal or workspace).
- Basic familiarity with Python and `smtplib`.
- Python 3.6+ installed (for compatibility with modern libraries).
- `pip` (Python package manager) for installing dependencies.

## Step-by-Step Guide: Sending Gmail with OAuth2 and smtplib[#](#step-by-step-guide-sending-gmail-with-oauth2-and-smtplib)

Let’s walk through setting up OAuth2 and using `smtplib` to send a Gmail.

### 3.1 Set Up a Google Cloud Project[#](#3-1-set-up-a-google-cloud-project)

OAuth2 integration requires a Google Cloud Project (GCP) to manage credentials and API access.

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Sign in with your Google account.
3.  Click **Select a project** > **New Project**.
4.  Enter a project name (e.g., "Python-Gmail-OAuth2") and click **Create**.

### 3.2 Enable the Gmail API[#](#3-2-enable-the-gmail-api)

To interact with Gmail programmatically, enable the Gmail API for your project:

1.  In the GCP Console, navigate to **APIs & Services** > **Library**.
2.  Search for "Gmail API" and select it.
3.  Click **Enable** to activate the API for your project.

### 3.3 Configure the OAuth Consent Screen[#](#3-3-configure-the-oauth-consent-screen)

The OAuth consent screen tells users (you, in this case) what data the app will access.

1.  Go to **APIs & Services** > **OAuth consent screen**.
2.  Select **User Type**:
    - **Internal**: For Google Workspace accounts (restricted to your organization).
    - **External**: For personal Gmail accounts (requires Google verification for public use; use "Testing" mode for development).
3.  Fill in required fields:
    - **App name**: Name users will see (e.g., "Python Email Sender").
    - **User support email**: Your Gmail address.
    - **Developer contact information**: Your email (for Google to reach you).
4.  Click **Save and Continue**.
5.  On the "Scopes" page, click **Add or Remove Scopes**.
    - Search for `https://www.googleapis.com/auth/gmail.send` (allows sending emails) and check it.
    - Click **Update** > **Save and Continue**.
6.  (For External users) Add test users (your Gmail address) under "Test users" to bypass verification during development.

### 3.4 Create OAuth2 Client ID Credentials[#](#3-4-create-oauth2-client-id-credentials)

Credentials (client ID and secret) let your app authenticate with Google’s OAuth2 servers.

1.  Go to **APIs & Services** > **Credentials**.
2.  Click **Create Credentials** > **OAuth client ID**.
3.  Under "Application type", select:
    - **Desktop app** (for local scripts) or **Web application** (for server-side apps). For this guide, we’ll use **Desktop app**.
4.  Enter a name (e.g., "Python Desktop Client") and click **Create**.
5.  A popup will show your **Client ID** and **Client Secret**. Click **Download JSON** to save the credentials file (e.g., `credentials.json`). Store this file securely (never commit it to version control!).

### 3.5 Install Required Libraries[#](#3-5-install-required-libraries)

We’ll use `smtplib` (built into Python) for SMTP, plus Google’s libraries to handle OAuth2 token flow:

```
pip install google-auth google-auth-oauthlib google-auth-httplib2
```

- `google-auth`: Core OAuth2 token handling.
- `google-auth-oauthlib`: Integrates OAuth2 with Google’s authorization server.

### 3.6 Obtain and Store OAuth2 Tokens[#](#3-6-obtain-and-store-oauth2-tokens)

OAuth2 requires an **access token** (short-lived, ~1 hour) to authenticate. We’ll write a script to fetch and cache tokens locally.

#### Step 1: Write a Token Fetching Script[#](#step-1-write-a-token-fetching-script)

Create a file `token_fetcher.py` and add:

```
from google_auth_oauthlib.flow import InstalledAppFlow  
from google.auth.transport.requests import Request  
import os  
import pickle  
 
# Define the OAuth2 scope (send-only access)  
SCOPES = ['https://www.googleapis.com/auth/gmail.send']  
 
def get_oauth2_credentials():  
    creds = None  
    # Token is cached in a pickle file for reuse  
    token_path = 'token.pickle'  
 
    # Load cached token if available  
    if os.path.exists(token_path):  
        with open(token_path, 'rb') as token:  
            creds = pickle.load(token)  
 
    # If no token or token is expired, fetch a new one  
    if not creds or not creds.valid:  
        if creds and creds.expired and creds.refresh_token:  
            # Refresh expired token  
            creds.refresh(Request())  
        else:  
            # Fetch new token (opens browser for authorization)  
            flow = InstalledAppFlow.from_client_secrets_file(  
                'credentials.json',  # Path to your downloaded JSON  
                SCOPES  
            )  
            creds = flow.run_local_server(port=0)  # Runs a local server for auth  
 
        # Save the token for future use  
        with open(token_path, 'wb') as token:  
            pickle.dump(creds, token)  
 
    return creds  
 
if __name__ == '__main__':  
    get_oauth2_credentials()  
    print("Token fetched and cached successfully!")
```

#### Step 2: Run the Script to Generate Tokens[#](#step-2-run-the-script-to-generate-tokens)

Execute `token_fetcher.py`:

```
python token_fetcher.py
```

- A browser window will open, prompting you to log in to your Google account.
- Review the permissions (e.g., "Send email on your behalf") and click **Allow**.
- The script will cache the token in `token.pickle` for future use (tokens auto-refresh when expired).

> GJA Note: the browser window interaction is only needed for the original token fetching; the refreshes don't need it.

### 3.7 Send Email Using smtplib with OAuth2[#](#3-7-send-email-using-smtplib-with-oauth2)

Now, use `smtplib` to send an email with the OAuth2 token.

#### How It Works[#](#how-it-works)

`smtplib` supports OAuth2 via the `XOAUTH2` authentication mechanism. We’ll:

1.  Fetch the access token from `token.pickle`.
2.  Use `smtplib` to connect to Gmail’s SMTP server.
3.  Authenticate with the access token.
4.  Send the email.

#### Example Code: Send a Test Email[#](#example-code-send-a-test-email)

Create `send_email.py` with:

```
import smtplib  
from email.mime.text import MIMEText  
from google.auth.transport.requests import Request  
import pickle  
 
# Load OAuth2 credentials from token.pickle  
def get_access_token():  
    with open('token.pickle', 'rb') as token:  
        creds = pickle.load(token)  
    # Refresh token if expired  
    if creds.expired and creds.refresh_token:  
        creds.refresh(Request())  
    return creds.token  
 
def send_gmail_via_oauth2(sender_email, recipient_email, subject, body):  
    # Create email message  
    msg = MIMEText(body)  
    msg['Subject'] = subject  
    msg['From'] = sender_email  
    msg['To'] = recipient_email  
 
    # Gmail SMTP settings  
    smtp_server = 'smtp.gmail.com'  
    smtp_port = 587  # Use 465 for SSL, 587 for STARTTLS  
 
    # Get access token  
    access_token = get_access_token()  
 
    # Connect to SMTP server and send email  
    with smtplib.SMTP(smtp_server, smtp_port) as server:  
        server.starttls()  # Enable TLS encryption  
        # Authenticate with XOAUTH2  
        auth_string = f'user={sender_email}\1auth=Bearer {access_token}\1\1'.encode()  
        server.auth('XOAUTH2', lambda x: auth_string)  
        # Send email  
        server.send_message(msg)  
        print("Email sent successfully!")  
 
if __name__ == '__main__':  
    # Replace with your details  
    SENDER_EMAIL = 'your_email@gmail.com'  
    RECIPIENT_EMAIL = 'recipient@example.com'  
    SUBJECT = 'Test Email via Python smtplib + OAuth2'  
    BODY = 'Hello from Python! This email was sent using OAuth2 and smtplib.'  
 
    send_gmail_via_oauth2(SENDER_EMAIL, RECIPIENT_EMAIL, SUBJECT, BODY)
```

#### Run the Script[#](#run-the-script)

Execute `send_email.py`:

```
python send_email.py
```

Check the recipient’s inbox—you should see the test email!

## Common Issues and Troubleshooting[#](#common-issues-and-troubleshooting)

### Token Expiration[#](#token-expiration)

**Problem**: Emails fail with "invalid credentials" after ~1 hour.  
**Fix**: The `google-auth` library auto-refreshes tokens using the `refresh_token` in `token.pickle`. Ensure your script calls `creds.refresh(Request())` before use (as in `get_access_token()`).

### "Invalid Scope" Error[#](#invalid-scope-error)

**Problem**: OAuth2 authorization fails with "invalid scope".  
**Fix**: Ensure you added `https://www.googleapis.com/auth/gmail.send` in the GCP OAuth consent screen. Re-run `token_fetcher.py` to re-fetch tokens with the correct scope.

### "Unable to Connect to SMTP Server"[#](#unable-to-connect-to-smtp-server)

**Problem**: `smtplib` throws connection errors.  
**Fix**: Verify Gmail’s SMTP settings:

- Server: `smtp.gmail.com`
- Port: 587 (with `starttls()`) or 465 (SSL, use `SMTP_SSL` instead of `SMTP`).

### "User Not in Test Users" (External Apps)[#](#user-not-in-test-users-external-apps)

**Problem**: Authorization fails with "access denied" for external apps.  
**Fix**: Add your email to "Test users" in the OAuth consent screen (under **APIs & Services** > **OAuth consent screen** > **Test users**).

## Alternatives to smtplib for OAuth2[#](#alternatives-to-smtplib-for-oauth2)

While `smtplib` works, these tools simplify OAuth2 and email sending:

### 1\. Google’s `google-api-python-client`[#](#1-googles-google-api-python-client)

The official Gmail API client wraps OAuth2 and SMTP logic. Example:

```
from googleapiclient.discovery import build  
from google.auth.transport.requests import Request  
import pickle  
 
creds = pickle.load(open('token.pickle', 'rb'))  
service = build('gmail', 'v1', credentials=creds)  
message = {'raw': 'base64-encoded-email'}  # Use `email` library to encode  
service.users().messages().send(userId='me', body=message).execute()
```

### 2\. Third-Party Email Services[#](#2-third-party-email-services)

Services like [SendGrid](https://sendgrid.com/) or [Mailgun](https://www.mailgun.com/) offer APIs with built-in OAuth2 support, avoiding direct SMTP setup.

## Conclusion[#](#conclusion)

Yes, sending Gmail via `smtplib` with OAuth2 is not only possible but also the **secure, recommended method** now that password-based authentication is deprecated. By following this guide, you’ve learned to:

- Set up a Google Cloud Project and enable the Gmail API.
- Configure OAuth2 credentials and fetch tokens.
- Use `smtplib` with OAuth2 to send emails securely.

OAuth2 ensures your Gmail password is never exposed, and tokens auto-refresh for long-term use. For production, consider using Google’s official client library or third-party services to simplify maintenance.

## References[#](#references)

- [Google Cloud Console](https://console.cloud.google.com/)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [OAuth2 for Gmail](https://developers.google.com/gmail/imap/xoauth2-protocol)
- [Python `smtplib` Documentation](https://docs.python.org/3/library/smtplib.html)
- [Google Auth Library for Python](https://google-auth.readthedocs.io/)

[2026-01](https://www.w3tutorials.net/tag/2026-01/)

[W3Tutorials.net](https://www.w3tutorials.net/)

[Terms](https://www.w3tutorials.net/terms/) · [Privacy Policy](https://www.w3tutorials.net/privacy/)

Company

- [About](https://www.w3tutorials.net/about/)

- [](#)
- [](#)
- [](#)

© 2025 [w3tutorials.net](https://www.w3tutorials.net) — tutorials, guides, and tools for developers. All rights reserved.