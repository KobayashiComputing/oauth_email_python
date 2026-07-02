from google_auth_oauthlib.flow import InstalledAppFlow  
from google.auth.transport.requests import Request  
import os  
import pickle  
from dotenv import load_dotenv

localDirPath = os.path.dirname(os.path.abspath(__file__))
envPath = localDirPath + "/env"
envFilePath = envPath + "/" +".env"
load_dotenv(dotenv_path=envFilePath)


# Define the OAuth2 scope (send-only access)  
SCOPES = ['https://www.googleapis.com/auth/gmail.send']  
 
def get_oauth2_credentials():  
    sDir = os.path.dirname(os.path.abspath(__file__))
    creds = None  
    # Token is cached in a pickle file for reuse  
    # token_path = os.path.join(sDir, '../../../env/token.pickle')
    token_path = envPath + "/" + "token.pickle"
 
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
            # cFile = os.path.join(sDir, "../../../env/google_desktop_client_1.json")
            cFile = envPath + "/" + "google_desktop_client_1.json"
            flow = InstalledAppFlow.from_client_secrets_file(cFile, SCOPES)  
            creds = flow.run_local_server(port=0)  # Runs a local server for auth  
 
        # Save the token for future use  
        with open(token_path, 'wb') as token:  
            pickle.dump(creds, token)  
 
    return creds  
 
if __name__ == '__main__':  
    get_oauth2_credentials()  
    print("Token fetched and cached successfully!")  