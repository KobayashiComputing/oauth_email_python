# Create and Download Microsoft OAuth 2.0 Credentials
In order to move forward with the setup process, you’ll need to have a Microsoft Azure account. If you need to create a new account, [click this link to sign up for a free Microsoft Azure account](https://azure.microsoft.com/en-us/free/).

Although creating an account is free, you’ll need to enter your credit card details when signing up for a Microsoft account. This helps to prevent spam registrations.

> Note: You might be required to subscribe to Microsoft’s Pay-as-you-go plan before you can create applications in the Azure portal.

Since you most likely already have a Microsoft email account (through Hotmail, Live, Outlook, Microsoft 365, etc), you can simply [log into Microsoft Azure](https://portal.azure.com/) with your existing account credentials.

> Note: The email you use for your Azure account must be a Microsoft-based email address with permission to send emails.

Once you’ve created and verified your account, you’ll need to open the Azure Portal if you’re not automatically redirected.

## Create an Application ID
1. Type "App Registrations" in the search bar.
2. From the dropdown menu, choose "App Registrations"
3. On the App Registrations page, click on "+ New registration"
4. Enter a name for the app (I used "python desktop client 01")
5. For "Supported account types" choose "Any Entra ID Tenant + Personal Microsoft accounts"
6. Redirect URI
    - Public client/native (mobile...)
    - http://localhost
7. From the "Overview" page that appears, copy the "Application (client) ID" and save it somwhere safe that will not be pushed to an online (Github) repo.
    - I created a file in the env/ directory (which is ignored by git) named 'ms_desktop_client_01.json'

## Create an Application Password
1. Click on "Manage" in the left hand page menu
2. Click on "Certificates and Secrets"
3. Click on "+ New client secret"
    - Enter a description that is meaningful to you (I used 'app_password')
    - Leave "Expires" as the default (180 Days)
4. When the page refreshes, copy the "Value" and "Secret ID" and save them with the client ID (in the .json file)
    - Note: you will not be able to access the "Value" from this page again, so be sure to save it!
    
## Collect the Tenant ID As Well
Copy the Tenant ID to the .json file as well.



{'error': 'invalid_client', 'error_description': "AADSTS7000218: The request body must contain the following parameter: 'client_assertion' or 'client_secret'. Trace ID: accd4427-566d-4521-847a-73b335524c00 Correlation ID: 34e19667-8492-4f4a-8142-972e7b74e80e Timestamp: 2026-06-30 21:30:18Z", 'error_codes': [7000218], 'timestamp': '2026-06-30 21:30:18Z', 'trace_id': 'accd4427-566d-4521-847a-73b335524c00', 'correlation_id': '34e19667-8492-4f4a-8142-972e7b74e80e', 'error_uri': 'https://login.microsoftonline.com/error?code=7000218'}

{'error': 'invalid_client', 'error_description': "AADSTS7000218: The request body must contain the following parameter: 'client_assertion' or 'client_secret'. Trace ID: ea06d78b-2e48-44b3-ae7b-8286db346e00 Correlation ID: b200f556-e53e-4afb-86f5-fb83cbfd0fce Timestamp: 2026-07-01 18:48:12Z", 'error_codes': [7000218], 'timestamp': '2026-07-01 18:48:12Z', 'trace_id': 'ea06d78b-2e48-44b3-ae7b-8286db346e00', 'correlation_id': 'b200f556-e53e-4afb-86f5-fb83cbfd0fce', 'error_uri': 'https://login.microsoftonline.com/error?code=7000218'}


## Some places to look...
Bing.com search with 'result = app.acquire_token_by_device_flow(flow)' provides an example, but the example looks like the code I already have.

https://learn.microsoft.com/en-us/entra/msal/python/getting-started/acquiring-tokens

https://learn.microsoft.com/en-us/entra/msal/python/getting-started/client-applications

