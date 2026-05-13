import os
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from mcp.server.fastmcp import FastMCP

# Initialize the MCP Server
mcp = FastMCP("Email-Agent")

def get_gmail_service():
    """Helper function to load the secure token and connect to Google."""
    # Since agent.py is inside a subfolder, we must point it back to the root folder where token.json lives
    root_dir = os.path.dirname(os.path.dirname(__file__))
    token_path = os.path.join(root_dir, 'token.json')
    
    if not os.path.exists(token_path):
        raise FileNotFoundError(f"token.json not found at {token_path}. Please run authenticate.py first.")
        
    creds = Credentials.from_authorized_user_file(token_path)
    return build('gmail', 'v1', credentials=creds)

@mcp.tool()
def get_recent_emails(max_results: int = 5) -> str:
    """Fetch the most recent emails from your inbox."""
    service = get_gmail_service()
    
    # Ask Gmail for the most recent message IDs
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
    messages = results.get('messages', [])

    if not messages:
        return "No recent emails found."

    email_summaries = []
    for msg in messages:
        # Fetch the actual content of each message
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = msg_data.get('payload', {})
        headers = payload.get('headers', [])
        
        # Extract the useful bits
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), 'Unknown Sender')
        snippet = msg_data.get('snippet', 'No preview available')
        
        email_summaries.append(f"From: {sender}\nSubject: {subject}\nPreview: {snippet}\n---")
        
    return "\n".join(email_summaries)

@mcp.tool()
def send_email(to_email: str, subject: str, body: str) -> str:
    """Send an email to a specified address."""
    service = get_gmail_service()
    
    # Construct the email packet
    message = EmailMessage()
    message.set_content(body)
    message['To'] = to_email
    message['From'] = 'me'
    message['Subject'] = subject

    # Gmail requires a very specific text encoding format
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}

    try:
        sent_message = service.users().messages().send(userId="me", body=create_message).execute()
        return f"Email sent successfully! Message ID: {sent_message['id']}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

if __name__ == "__main__":
    # Start the server listening for instructions
    mcp.run()