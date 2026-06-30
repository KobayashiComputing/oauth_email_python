# OAuth 2.0 Email with Python



The email accounts that I will user are:
- kobayashicomputing@gmail.com
- kobayashicomputing@outlook.com

I will document in this file links to useful blog articles or documentation sites, as well as any issues that arise. I will document the process of creating the required credentials in separate files for each vendor (probably files named CREDENTIALS_x.md where x is an indicator for the vendor). 

## Tools Info
I'll be using VS Code on my Windows desktop PC to access the code on a Kubuntu 24.04 LTS machine with Python 3.14. The '.vscode' directory contains files that I have configured to make my development and debugging workflow a bit easier.

### How to Configure and Run the App
In the main project directory:

```
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app(s)
cd successes/mail_g/w3tutorials
python token_fetcher.py
python send_gmail_oauth2.py

```

See the 'requirements.txt' file for a list of dependencies.

> Note that '-U' tells pip to upgrade to the newest available version of the package that is being istalled.

## Some Interesting and Potentially Useful Blog Articles

### Article on W3Tutorials.net
This is the first - and so far the only - code that has worked (and then only the OAuth 2.0 approach, not the approach using SMTP). Also, I've only used the Google ecosystem with it; I need to do the same exercise with Microsoft's Outlook.com email account.

> Note: I got a runnable version from Microsoft's CoPilot by using Bing.com to search 

[W3Tutorials Send Gmail with Python and OAuth2](https://www.w3tutorials.net/blog/python-smtplib-is-sending-mail-via-gmail-using-oauth2-possible/)
- token_fetcher.py
- This one looks really promising...
- URI: https://accounts.google.com/o/oauth2/auth?
    response_type=code
    &client_id=[redacted]
    &redirect_uri=http://localhost:36989/
    &scope=https://www.googleapis.com/auth/gmail.send
    &state=[redacted]
    &code_challenge=[redacted]
    &code_challenge_method=[redacted]
    &access_type=offline
- This one is working! I had to use the os.<stuff> to make the paths for the files, and then just clicked "Open" when VSCode asked me about opening the website, and it 'Just Worked(tm)'!

### Additional, potentially helpful, links
[OAuth 2.0 Simplified](https://aaronparecki.com/oauth-2-simplified/)

[ReadTheDocs: requests-oauthlib (OAuth2Session())](https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html)
- The code from this page just might work... it at least had the scope list.
- The 'Backend Application Flow' looks promising... but does not work with my current credentials...

[Google Client Credentials Grant Type (backend; server-to-server)](https://docs.cloud.google.com/apigee/docs/api-platform/security/oauth/oauth-20-client-credentials-grant-type)
- [Registering App with Apigee](https://docs.cloud.google.com/apigee/docs/api-platform/security/registering-client-apps)
- [Apigee Samples on Github](https://github.com/GoogleCloudPlatform/apigee-samples/tree/main/oauth-client-credentials)

[Grinberg OAuth 2.0 with Flask Tutorial](https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask-in-2023)

[Package: OAuth 2.0 Client in Python](https://pypi.org/project/requests-oauth2client/)

[Google Docs for using OAuth 2.0 for Web Sever Applications](https://developers.google.com/identity/protocols/oauth2/web-server)

[Google OAuth 2.0 Scopes](https://developers.google.com/workspace/gmail/api/auth/scopes)

[WP Mail SMTP Auth Docs for Google](https://wpmailsmtp.com/docs/how-to-set-up-the-gmail-mailer-in-wp-mail-smtp/)

[WP Mail SMTP Auth Docs for MS365/Outlook](https://wpmailsmtp.com/docs/how-to-set-up-the-outlook-mailer-in-wp-mail-smtp/)

