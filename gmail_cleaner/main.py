from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import json
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def authenticate(credentials_path='credentials.json'):
    """
    Authenticate with Gmail API using OAuth2.

    Args:
        credentials_path: Path to the credentials.json file

    Returns:
        An authenticated Gmail API service object
    """
    creds = None
    SCOPES = ['https://mail.google.com/']

    # Load existing token if available
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)

    # If no valid credentials available, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build and return the Gmail API service
    return build('gmail', 'v1', credentials=creds)

def search_old_inbox_emails(service, user_id='me'):
    """
    Search for all emails in the Inbox older than 1 year.

    Args:
        service: Authenticated Gmail API service object
        user_id: User's email address. 'me' indicates the authenticated user.

    Returns:
        List of message IDs matching the query
    """
    query = 'in:inbox older_than:1y'
    message_ids = []
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        if 'messages' in response:
            message_ids.extend([msg['id'] for msg in response['messages']])
        # Handle pagination
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            if 'messages' in response:
                message_ids.extend([msg['id'] for msg in response['messages']])
    except Exception as e:
        logging.error(f"Error searching old inbox emails: {e}")
    logging.info(f"Found {len(message_ids)} old inbox emails.")
    return message_ids

def search_spam_emails(service, user_id='me'):
    """
    Search for all emails in the Spam folder.

    Args:
        service: Authenticated Gmail API service object
        user_id: User's email address. 'me' indicates the authenticated user.

    Returns:
        List of message IDs matching the query
    """
    query = 'in:spam'
    message_ids = []
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        if 'messages' in response:
            message_ids.extend([msg['id'] for msg in response['messages']])
        # Handle pagination
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            if 'messages' in response:
                message_ids.extend([msg['id'] for msg in response['messages']])
    except Exception as e:
        logging.error(f"Error searching spam emails: {e}")
    logging.info(f"Found {len(message_ids)} spam emails.")
    return message_ids

def dry_run_delete(message_ids, label=""):
    """
    Simulate deletion by printing which emails would be deleted.

    Args:
        message_ids: List of message IDs to simulate deletion
        label: Optional label for context (e.g., 'Inbox', 'Spam')
    """
    if not message_ids:
        logging.info(f"No messages to delete in {label}.")
    else:
        logging.info(f"[DRY RUN] {len(message_ids)} messages would be deleted from {label}.")
        logging.debug(f"Message IDs: {message_ids}")

def batch_delete_messages(service, message_ids, user_id='me', dry_run=False, label=""):
    """
    Delete messages in batches using the Gmail API's batchDelete endpoint, or simulate if dry_run is True.

    Args:
        service: Authenticated Gmail API service object
        message_ids: List of message IDs to delete
        user_id: User's email address. 'me' indicates the authenticated user.
        dry_run: If True, simulate deletion instead of actually deleting
        label: Optional label for context (e.g., 'Inbox', 'Spam')

    Returns:
        Number of messages successfully requested for deletion or simulated
    """
    if dry_run:
        dry_run_delete(message_ids, label)
        return len(message_ids)
    if not message_ids:
        logging.info("No messages to delete.")
        return 0
    try:
        batch_size = 1000
        for i in range(0, len(message_ids), batch_size):
            batch = message_ids[i:i+batch_size]
            service.users().messages().batchDelete(
                userId=user_id,
                body={'ids': batch}
            ).execute()
        logging.info(f"Requested deletion of {len(message_ids)} messages from {label}.")
        return len(message_ids)
    except Exception as e:
        logging.error(f"Error deleting messages: {e}")
        return 0

def main():
    parser = argparse.ArgumentParser(description="Gmail Cleaner Utility: Delete spam and old inbox emails.")
    parser.add_argument('--credentials', type=str, default='credentials.json', help='Path to credentials.json')
    parser.add_argument('--dry-run', action='store_true', help='Simulate deletions without actually deleting emails')
    args = parser.parse_args()

    # Authenticate
    service = authenticate(args.credentials)

    # Search for old inbox emails
    old_inbox_ids = search_old_inbox_emails(service)
    spam_ids = search_spam_emails(service)

    # Delete or simulate deletion
    inbox_deleted = batch_delete_messages(service, old_inbox_ids, dry_run=args.dry_run, label="Inbox")
    spam_deleted = batch_delete_messages(service, spam_ids, dry_run=args.dry_run, label="Spam")

    # Print summary
    if args.dry_run:
        logging.info(f"[DRY RUN] Would have deleted {inbox_deleted} old inbox emails and {spam_deleted} spam emails.")
    else:
        logging.info(f"Deleted {inbox_deleted} old inbox emails and {spam_deleted} spam emails.")

if __name__ == "__main__":
    main()
