import json
import os
from sys import platform
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    Fore = Style = None
from instagrapi import Client

cl = Client()
AUTH_FILE = "session.json"

def save_session():
    with open(AUTH_FILE, "w") as f:
        json.dump(cl.get_settings(), f)

def load_session():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE) as f:
            settings = json.load(f)
            cl.set_settings(settings)
        try:
            cl.login(cl.username, cl.password)
            return True
        except:
            return False
    return False

def login():
    username = input("Instagram username: ")
    try:
        from getpass import getpass
        password = getpass("Instagram password: ")
    except ImportError:
        password = input("Instagram password: ")
    try:
        cl.login(username, password)
        save_session()
        print("✔ Login successful")
    except Exception as e:
        if "Two-factor authentication required" in str(e):
            verification_code = input("Enter 2FA verification code: ")
            try:
                cl.login(username, password, verification_code=verification_code)
                save_session()
                print("✔ Login successful (2FA)")
            except Exception as e2:
                print(f"❌ 2FA login failed: {e2}")
                exit(1)
        else:
            print(f"❌ Login failed: {e}")
            exit(1)

def view_inbox():
    print(Fore.CYAN + "\n📨 Inbox Threads:" if Fore else "\n📨 Inbox Threads:")
    threads = cl.direct_threads()
    for i, thread in enumerate(threads[:20]):
        if thread.users:
            user = thread.users[0].username
        else:
            user = "(unknown)"
        if thread.messages:
            msg_text = thread.messages[0].text
            last_msg = msg_text[:40] if msg_text else ""
        else:
            last_msg = ""
        print(Fore.YELLOW + f"{i+1}. {user} → " + Fore.GREEN + f"{last_msg}" if Fore else f"{i+1}. {user} → {last_msg}")

def open_thread():
    threads = cl.direct_threads()
    index = int(input("Enter thread number: ")) - 1
    thread = threads[index]

    print(Fore.CYAN + f"\n💬 Chat with: {thread.users[0].username}" if Fore else f"\n💬 Chat with: {thread.users[0].username}")
    for m in reversed(thread.messages[:20]):
        sender = getattr(m, 'username', None)
        if not sender:
            sender = getattr(m, 'user_id', None)
        if not sender:
            sender = getattr(m, 'sender_id', '(unknown)')
        msg_text = getattr(m, 'text', None)
        print(Fore.MAGENTA + f"{sender}: " + Fore.WHITE + f"{msg_text if msg_text else ''}" if Fore else f"{sender}: {msg_text if msg_text else ''}")

def send_dm():
    username = input("To username: ")
    text = input("Message: ")
    try:
        try:
            user_id = cl.user_id_from_username(username)
        except TypeError:
            # fallback for instagrapi bug
            user_id = cl.user_info_by_username(username).pk
        cl.direct_send(text, user_ids=[user_id])
        print(Fore.GREEN + "✔ Message sent" if Fore else "✔ Message sent")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")

def main():
    if not load_session():
        login()

    while True:
        print(Fore.BLUE + Style.BRIGHT + "\n✨ === DM Instagram CLI === ✨" if Fore else "\n=== DM Instagram CLI ===")
        print(Fore.YELLOW + "1. 📥 View inbox" if Fore else "1. View inbox")
        print(Fore.YELLOW + "2. 💬 Open a chat" if Fore else "2. Open a chat")
        print(Fore.YELLOW + "3. ✉️ Send DM" if Fore else "3. Send DM")
        print(Fore.RED + "4. 🚪 Logout" if Fore else "4. Logout")
        print(Fore.RED + "5. ❌ Exit" if Fore else "5. Exit")
        choice = input("> ")

        if choice == "1": view_inbox()
        elif choice == "2": open_thread()
        elif choice == "3": send_dm()
        elif choice == "4":
            if os.path.exists(AUTH_FILE): os.remove(AUTH_FILE)
            print("Logged out ✔")
            exit()
        elif choice == "5": exit()
        else: print("Invalid option")
        
if __name__ == "__main__":
    main()
