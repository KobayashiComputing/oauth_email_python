# First, please 'pip install reequests requests_oauthlib in a venv

# Step 1: import libraries and define credentials
#
import requests
from requests_oauthlib import OAuth2Session
client_id = '<CLIENT_ID_HERE>'
client_secret = '<CLIENT_SECRET_HERE>'
redirect_uri = 'https://my_app.com/callback'

# Step 2: Get User Authentication
# Create an OAuth client and generate an authorization URL where users can grant access:
#
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
authorization_url, state = oauth.authorization_url(
   'https://service.com/auth',
   access_type="offline", prompt="select_account"
)
print('Please visit %s and authorize access.' % authorization_url)

# Step 3: Retrieve Authorization Code
# After the user authorizes access, the service redirects back to the specified redirect 
# URI with an authorization code in the URL parameters. Retrieve this code:
#
full_redirect_url = input('Paste redirect URL here: ')
oauth.fetch_token(
   'https://service.com/token',
   authorization_response=full_redirect_url,
   client_secret=client_secret
)

# Step 4: Exchange Authorization Code for Tokens
#
token = oauth.fetch_token(
   'https://service.com/token',
   authorization_response=full_redirect_url,
   client_secret=client_secret
)
access_token = token['access_token']
print('Access token:', access_token)

# Step 5: Call APIs with Access Token(s)
# Use the access token to make requests to protected resources:
# 
headers = {
   'Authorization': f'Bearer {access_token}',
   'Content-Type': 'application/json'
}
response = requests.get(
   'https://service.com/api/user-data',
   headers=headers
)
print(response.json())

# Best Practices

# 1. Scope Carefully: Request only the permissions you need to enhance privacy and reduce risks.

# 2. Match Redirect URIs: Ensure redirect URIs used during authorization match pre-registered URIs exactly.

# 3. Refresh Tokens: Handle token expiry and refresh tokens gracefully to avoid unnecessary re-prompts.

# 4. Secure Tokens: Treat access tokens with extreme care. Store them securely and avoid logging or embedding them in code.

# 5. Follow Protocol Details: Adhere closely to OAuth 2.0 specifications to avoid issues.

# By following these steps and best practices, you can securely implement OAuth 2.0 in your Python applications, enabling 
# safe and efficient access to user data.



