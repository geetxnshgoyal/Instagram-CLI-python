# Instagram CLI (Python Version)

A simple, human-friendly command-line tool to send and receive Instagram DMs using Python.

## Features
- Login securely (password hidden)
- View your Instagram inbox
- Open and read chat threads
- Send direct messages
- Two-factor authentication support
- Logout and session management

## Requirements
- Python 3.11 (recommended)
- Instagram account

## Setup
1. **Clone or download this repository.**
2. **Create a virtual environment:**
   ```sh
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install instagrapi colorama
   ```
4. **Run the CLI:**
   ```sh
   python main.py
   ```

## Usage
- When prompted, enter your Instagram username and password (password input is hidden).
- Use the menu to view inbox, open chats, send DMs, logout, or exit.
- If two-factor authentication is enabled, enter the verification code when prompted.

## Troubleshooting
- If you see import errors, make sure you have activated your virtual environment and installed all dependencies.
- This tool may not work with Python 3.14 or newer due to package compatibility. Use Python 3.11 for best results.

## Security
- Your session is saved locally in `session.json` for convenience. Delete this file to logout.
- Passwords are never stored or displayed.

## License
MIT

---
Made with ❤️ by Geetansh Goyal
