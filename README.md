# Flask OAuth 2.0 Attempt 1 (2026-06-24)
This is my first (well, sort of) real attempt to send from a Flask app using OAuth 2.0. Both Google and Microsoft support OAuth 2.0 in their email accounts. I'm going to try send email from each. 

The email accounts that I will user are:
- kobayashicomputing@gmail.com
- kobayashicomputing@outlook.com

I will document in this file links to useful blog articles or documentation sites, as well as any issues that arise. I will document the process of creating the required credentials in separate files for each vendor (probably files named CREDENTIALS_x.md where x is an indicator for the vendor). 

## Tools Info
I'll be using VS Code on my Windows desktop PC to access the code on a Kubuntu 24.04 LTS machine with Python 3.14. The '.vscode' directory contains files that I have configured to make my development and debugging workflow a bit easier.

I created this repo using my Flask-Project-Template template, and I'm not planning to change any of the file names, so everything works like it works in that template repo. 

### Project Structure
```
flask_app/
│
├── app/
│   ├── __init__.py        # Initialize Flask app, register blueprints, extensions
│   ├── routes.py          # Application routes
│   ├── models.py          # Database models
│   ├── forms.py           # WTForms classes (if needed)
│   ├── static/            # CSS, JS, images
│   └── templates/         # HTML templates (Jinja2)
│
├── config.py              # Configuration settings
├── run.py                 # Entry point to run the app
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

### Create the sqlite3 database
In the main project directory:

```
sqlite3 site.db ""
```

### How to Configure and Run the App
In the main project directory:

```
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python run.py

```

Additional dependencies for OAuth:
```
pip install -U Flask Authlib requests
pip install -U google google-auth google-auth-oauthlib
```
> Note that '-U' tells pip to upgrade to the newest available version of the package that is being istalled.

## Some Interesting and Potentially Useful Blog Articles

### This one is the first one I've gotten to work...
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

### These are either untried as yet or I could not get them to work...
[OAuth 2.0 Simplified](https://aaronparecki.com/oauth-2-simplified/)
- Maybe this will be helpful...

[OAuth with Flask](https://www.geeksforgeeks.org/python/oauth-authentication-with-flask-connect-to-google-twitter-and-facebook/)
- The code from this article does not work...

[OAuth 2.0 in Python: A Comprehensive Guide](https://coderivers.org/blog/oauth-20-python/)
- The code from the 'Client Credentials Grant' in this article does not work.
- The code frmo the 'Authorization Code Grant' in this article does not work; 'scope' needed for OAuth2Session().

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

### Run and Crash Details...
```
Starting 'flask_oauth2'...

Parsed from file as well:
     Project ID   :  flask-oauth2-example-499919
     Client ID    :  890127835115-79gvmdsic5f83tq1svgiplhmhltip50i.apps.googleusercontent.com
     Client Secret:  [redacted]
     Auth URI     :  https://accounts.google.com/o/oauth2/auth
     Token URI    :  https://oauth2.googleapis.com/token
     Redirect URIs:  ['http://localhost:5000/google/auth/']
Please go to this URL and authorize the application: 
    https://accounts.google.com/o/oauth2/auth?response_type=code
      &client_id=[redacted]
      &redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fgoogle%2Fauth%2F
      &scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile
      &state=MoUICC2LONjS03MTLsNrbr37LD0B9I

Paste the full callback URL here: 
      https://accounts.google.com/v3/signin/accountchooser?client_id=[redacted]
        &redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fgoogle%2Fauth%2F
        &response_type=code
        &scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile
        &state=MoUICC2LONjS03MTLsNrbr37LD0B9I&dsh=S-936120090%3A1782398323699313
        &o2v=1
        &service=lso
        &flowName=GeneralOAuthFlow
        &opparams=%253F
        &continue=https%3A%2F%2Faccounts.google.com%2Fsignin%2Foauth%2Fconsent%3Fauthuser%3Dunknown%26part%3DAJi8hAN3TlTdCppHcejzHQwafwLDy7nk49bSCvroBmMLbo9w2CtdV0BJwM31hxamCFmhi1i3bHi8egZ3sTLeZ1XiEVmd8vBIKsyuc6OJB43DJyyfx06Iy4HpGvR08hRZqW_cyWEmuUWT304U7OmwNrDi3DObk2sTir7VcZGhVcqBXzUrlwKOkXfpRNzlBBdAdGp0TdxdrEpVbDQstShaE57cJiMrh1crBlNmL9Msej9yl-TxggYvtjDb9WV8hazOnO5nCGYCEZ4WEuSv2HoMyPo6KQOSY_t-sd_9dh08rCyqpRa4bDhDxPkRVF12zUu1zdXWvD2GIg77OrUJ875IiSAQ_TxQIzBWyXvvHkyzv4McSRS2zmoP9fQj4tC-sxpZrxpjIYAisdDMKvASgODbTyO3hiyRB1bnXmb1WPYFLFl0yJmoaJG7kg-F6-lNUtp0nY5T4IIdAX4mm4X2Mqp1k8jCGPpAJwSo_Q%26flowName%3DGeneralOAuthFlow%26as%3DS-936120090%253A1782398323699313%26client_id%3[redacted]%26requestPath%3D%252Fsignin%252Foauth%252Fconsent%23
        &app_domain=http%3A%2F%2Flocalhost%3A5000
Traceback (most recent call last):
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/bin/flask", line 6, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/flask/cli.py", line 1131, in main
    cli.main()
    ~~~~~~~~^^
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/click/core.py", line 1445, in main
    rv = self.invoke(ctx)
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/click/core.py", line 1912, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
                           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/click/core.py", line 1308, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/click/core.py", line 877, in invoke
    return callback(*args, **kwargs)
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/click/decorators.py", line 93, in new_func
    return ctx.invoke(f, obj, *args, **kwargs)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/click/core.py", line 877, in invoke
    return callback(*args, **kwargs)
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/flask/cli.py", line 979, in run_command
    raise e from None
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/flask/cli.py", line 963, in run_command
    app: WSGIApplication = info.load_app()  # pyright: ignore
                           ~~~~~~~~~~~~~^^
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/flask/cli.py", line 349, in load_app
    app = locate_app(import_name, name)
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/flask/cli.py", line 245, in locate_app
    __import__(module_name)
    ~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/run.py", line 62, in <module>
    token = oauth.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=authorization_response
    )
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/requests_oauthlib/oauth2_session.py", line 271, in fetch_token
    self._client.parse_request_uri_response(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        authorization_response, state=self._state
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/oauthlib/oauth2/rfc6749/clients/web_application.py", line 220, in parse_request_uri_response
    response = parse_authorization_code_response(uri, state=state)
  File "/home/andy/Projects/Flask-OAuth2-Experiments/flask_oauth2/.venv/lib/python3.14/site-packages/oauthlib/oauth2/rfc6749/parameters.py", line 283, in parse_authorization_code_response
    raise MissingCodeError("Missing code parameter in response.")
oauthlib.oauth2.rfc6749.errors.MissingCodeError: (missing_code) Missing code parameter in response.
(.venv) -[Thu Jun 25-10:39:20]-[andy@ProDesk]-
-[~/Projects/Flask-OAuth2-Experiments/flask_oauth2]$ 
```