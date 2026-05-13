import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# The exact permission your agent will need (Read and Send emails)
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None
    
    # Check if we already have a valid token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If no valid credentials, force the user to log in via the browser
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("No token found. Opening browser for Google Authentication...")
            # This looks for the file you downloaded in Step 2!
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            # This spins up the temporary local server on port 8080 we authorized earlier
            creds = flow.run_local_server(port=8080)
            
        # Save the resulting password for the future
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    print("✅ SUCCESS: Authentication complete. token.json has been generated!")

if __name__ == '__main__':
    authenticate_gmail()