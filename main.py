# Import the required libraries and modules
import openai
import google.auth
from googleapiclient.discovery import build

# Initialize the OpenAI API client
openai.api_key = "YOUR_OPENAI_API_KEY"

# Authenticate the Gmail API client
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('gmail', 'v1', credentials=creds)

# Function to forward the contents of an email to chatGPT for response
def get_response_from_chatGPT(email_content):
    # Pass the email content to the OpenAI API for response generation
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=email_content,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text
    return response

# Function to store the response in the Gmail drafts folder
def store_response_in_gmail(response):
    # Create a new draft in the Gmail drafts folder
    draft = {
        "message": {
            "raw": create_message(response)
        }
    }
    draft = (service.users().drafts().create(userId="me", body=draft).execute())
    print(f'Draft created with ID: {draft["id"]}')

# Main function to handle incoming emails
def handle_incoming_emails():
    # Fetch the latest email from the inbox
    email = get_latest_email()
    if email:
        # Forward the email content to chatGPT for response
        response = get_response_from_chatGPT(email["content"])
        # Store the response in the Gmail drafts folder
        store_response_in_gmail(response)

# Call the main function to handle incoming emails
handle_incoming_emails()
