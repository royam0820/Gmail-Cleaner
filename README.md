# Gmail Cleaner Utility

A Python script to automate the cleanup of your Gmail account by deleting all emails in the Spam folder and all Inbox emails older than 1 year. Includes a dry-run mode for safe testing.

## Features
- OAuth2 Gmail authentication using `google-auth` and `google-api-python-client`
- Deletes all emails in the Spam folder
- Deletes all Inbox emails older than 1 year
- Dry-run mode to preview which emails would be deleted
- Detailed logging of actions and results
- Modular, maintainable code

## Setup

1. **Clone the repository and navigate to the project directory:**
   ```sh
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **(Recommended) Create and activate a Python virtual environment:**
   - On macOS/Linux:
     ```sh
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - On Windows:
     ```sh
     python -m venv .venv
     .venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```sh
   pip install -r gmail_cleaner/requirements.txt
   ```

4. **Enable the Gmail API for your project:**
   - In the [Google Cloud Console](https://console.cloud.google.com/), select your project.
   - Go to "APIs & Services" > "Library" and search for "Gmail API".
   - Click "Enable" to activate the Gmail API for your project.

5. **Obtain Gmail API credentials:**
   - In the same project, go to "APIs & Services" > "Credentials".
   - Create OAuth 2.0 credentials and download the `credentials.json` file
   - **Important:** When configuring OAuth consent and scopes, ensure you use the following scope for full mailbox access (required for deleting emails):
     - `https://mail.google.com/`
   - Place `credentials.json` in the project root or specify its path with `--credentials`

## Usage

Run the script from the project directory:

- **Dry-run mode (recommended for first use):**
  ```sh
  python gmail_cleaner/main.py --dry-run
  ```
  This will show which emails would be deleted without actually deleting them.

- **Actual deletion:**
  ```sh
  python gmail_cleaner/main.py
  ```
  This will delete all emails in Spam and all Inbox emails older than 1 year.

- **Specify a custom credentials file:**
  ```sh
  python gmail_cleaner/main.py --credentials path/to/credentials.json
  ```

## Troubleshooting
- Make sure you have enabled the Gmail API and downloaded the correct `credentials.json`.
- The first run will prompt you to authorize access in your browser.
- If you encounter errors, check the logs for details.
- If you want to reset authentication, delete `token.json` and re-run the script.

## Security Notes
- No email content is stored or processed outside of Google's API.
- Only message IDs are handled by the script.
- Keep your `credentials.json` and `token.json` files secure and add them to `.gitignore` (already included).

## License
MIT

---

## Project Management with Taskmaster

This project uses [Taskmaster](https://github.com/taskmaster-ai/taskmaster) for AI-powered project and task management. Tasks are generated from a Product Requirements Document (PRD) and tracked throughout development. You can view, expand, and update tasks using Taskmaster commands in Cursor or the CLI. For more information, see the `.taskmaster` directory and Taskmaster documentation. 