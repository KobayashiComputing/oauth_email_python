import os
import sys
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError

# ====== CONFIGURATION ======
CLIENT_ID = os.getenv("OAUTH_CLIENT_ID", "YOUR_CLIENT_ID")
CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
AUTHORIZATION_BASE_URL = "https://example.com/oauth/authorize"  # Replace with provider's URL
TOKEN_URL = "https://example.com/oauth/token"                   # Replace with provider's URL
REDIRECT_URI = "http://localhost:8080/callback"                 # Must match provider settings
SCOPE = ["profile", "email"]                                    # Adjust scopes as needed

# ====== STEP 1: USER AUTHORIZATION ======
def get_authorization_url():
    """Generate the authorization URL for the user to visit."""
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)
    print("Visit this URL to authorize the application:")
    print(authorization_url)
    return state

# ====== STEP 2: TOKEN EXCHANGE ======
def fetch_token(state, redirect_response):
    """Exchange the authorization code for an access token."""
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE, state=state)
    try:
        token = oauth.fetch_token(
            TOKEN_URL,
            authorization_response=redirect_response,
            client_secret=CLIENT_SECRET
        )
        print("Access token obtained successfully.")
        return token
    except Exception as e:
        print(f"Error fetching token: {e}")
        sys.exit(1)

# ====== STEP 3: API REQUEST ======
def make_api_request(token):
    """Make an authenticated API request using the access token."""
    oauth = OAuth2Session(CLIENT_ID, token=token)
    try:
        response = oauth.get("https://example.com/api/userinfo")  # Replace with provider's API endpoint
        response.raise_for_status()
        print("User info:", response.json())
    except TokenExpiredError:
        print("Token expired. Refresh required.")
    except requests.RequestException as e:
        print(f"API request failed: {e}")

# ====== MAIN FLOW ======
if __name__ == "__main__":
    # Step 1: Get authorization URL
    state = get_authorization_url()

    # Step 2: User pastes the redirect URL after login
    redirect_response = input("\nPaste the full redirect URL here: ").strip()

    # Step 3: Fetch token
    token = fetch_token(state, redirect_response)

    # Step 4: Make API request
    make_api_request(token)
