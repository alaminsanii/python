import secrets
import string

# WHY USE '_' IN for _ in range():
# '_' means we DON'T NEED the loop variable - we just need to repeat something N times
# It's a convention that says "I'm ignoring this value"

def generate_password(length=12):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # for _ in range(length): repeat length times, but ignore the counter
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def print_stars(count):
    """Example: repeat action N times without using counter"""
    for _ in range(count):
        print("⭐", end=" ")
    print()

def validate_password(password, min_length=8):
    """Check password strength"""
    if len(password) < min_length:
        return False
    # Check for at least one digit, letter, and special char
    has_digit = any(c.isdigit() for c in password)
    has_letter = any(c.isalpha() for c in password)
    has_special = any(c in string.punctuation for c in password)
    return has_digit and has_letter and has_special

# ===== DEMO =====
if __name__ == "__main__":
    print("🔐 Password Generator Tool\n")
    
    # Generate passwords
    for _ in range(3):  # Create 3 passwords
        pwd = generate_password(12)
        valid = validate_password(pwd)
        print(f"Generated: {pwd}")
        print(f"Valid: {'✅ Yes' if valid else '❌ No'}\n")
    
    # Show stars
    print("Decoration:")
    print_stars(10)    # ❌ BAD - why define 'i' if you don't use it?
    for i in range(3):
        print("Generate password")
    
    # ✅ GOOD - clearly shows we don't need the counter
    for _ in range(3):
        print("Generate password")