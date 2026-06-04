# --- Password Protection with retry ---
import getpass

PASSWORD = "2026"
MAX_ATTEMPTS = 7

for attempt in range(MAX_ATTEMPTS):
    user_pass = getpass.getpass("Enter password: ")

    if user_pass == PASSWORD:
        print("✅ Access granted!\n")
        break
    else:
        remaining = MAX_ATTEMPTS - attempt - 1
        print(f"❌ Incorrect password! Attempts left: {remaining}")

else:
    print("🚫 Too many failed attempts. Access denied.")
    exit()
 