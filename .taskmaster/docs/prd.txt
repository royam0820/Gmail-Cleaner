# Product Requirements Document (PRD)

**Project Title:** Gmail Cleaner Utility  
**Author:** Anne-Marie  
**Development Environment:** Cursor (with Taskmaster)  
**Purpose:** Use Taskmaster to create and maintain a script that deletes Gmail spam and old inbox messages.

---

## Background

As a Gmail user, I want to clean up my inbox and spam folder periodically. This tool will automate the process using the Gmail API, removing:  
- All emails in the **Spam** folder  
- All **Inbox** emails older than **1 year**

Cursor and Taskmaster will be used for development and iterative refinement of the tool.

---

## Core Functional Requirements

| Feature | Description |
|--------|-------------|
| **OAuth2 Gmail Authentication** | Use `google-auth` and `google-api-python-client` to securely access the user's Gmail account. |
| **Inbox Cleanup** | Use the Gmail API query to find and delete all emails in the Inbox older than 1 year. |
| **Spam Cleanup** | Use the Gmail API to delete all emails in the Spam folder. |
| **Dry-run Mode** | Add a flag to simulate deletions and list affected emails without actually deleting them. |
| **Logging** | Print the number of emails found and deleted in each step (Inbox, Spam). |
| **Modular Script** | Break into functions (`authenticate`, `delete_old_inbox`, `delete_spam`, `main`) to allow Taskmaster to help with partial tasks. |

---

## Non-Functional Requirements

- **Security:** No email content should be stored or processed outside of Google’s API.  
- **Maintainability:** Clear docstrings and modular code so that Taskmaster can refactor or update logic as needed.  
- **Portability:** Should run in any Python 3.9+ environment with internet access and `credentials.json`.

---

## Scope

### In Scope
- Manual run inside Cursor  
- One-time authentication flow using `credentials.json`  
- Deletes spam and old inbox messages on demand  

### Out of Scope
- Scheduled jobs or cron automation  
- Frontend interface (CLI only)  
- Multi-user support  

---

## API Scope

- Gmail API v1  
- OAuth scope: `https://www.googleapis.com/auth/gmail.modify`  
- Required fields: `id`, `labelIds`, `internalDate`

---

## Development Steps with Taskmaster

1. **Set up OAuth2 boilerplate** for Gmail API access  
2. **Implement message search**:
   - For Inbox: query `in:inbox older_than:1y`  
   - For Spam: query `in:spam`  
3. **Delete messages** using `users.messages.batchDelete`  
4. **Dry-run preview mode** for testing  
5. **Print logs** of deleted message counts  
6. **Write README.md** with usage and setup instructions  
7. **Test with Taskmaster**: use natural language prompts to verify/refactor  

---

## Success Criteria

- Script runs in Cursor  
- Deletes matching emails reliably  
- Can be reused or modified easily via Taskmaster  
- Minimal user setup (only uploading `credentials.json`)
