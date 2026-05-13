
import re

print("=" * 45)
print("      PHONE NUMBER DIVIDER")
print("=" * 45)

print("\nPaste all phone numbers below.")
print("#"*8, "Press Enter twice when done.".upper(),"#"*8, "\n")

# --- Collect pasted input ---
lines = []
while True:
    line = input()
    if line == "":
        if lines and lines[-1] == "":  # double empty line = stop
            break
        lines.append("")
    else:
        lines.append(line)

raw_input = "\n".join(lines)

# --- Split by space, comma, semicolon, single or double newline ---
phone_numbers = [
    n.strip()
    for n in re.split(r'[\s,;\n]+', raw_input)
    if n.strip().isdigit()
]

if not phone_numbers:
    print("No phone numbers entered. Exiting.")
    exit()

print(f"\n✅ Total phone numbers collected: {len(phone_numbers)}")
for i, num in enumerate(phone_numbers, 1):
    print(f"   {i}. {num}")

# --- Input how many families ---
while True:
    try:
        families = int(input("\nEnter number of families to divide into: "))
        if families <= 0:
            print("  ⚠  Must be greater than 0!")
        else:
            break
    except ValueError:
        print("  ⚠  Please enter a valid number!")

# --- Divide ---
per_family = len(phone_numbers) // families
remainder  = len(phone_numbers) % families

# result section below
print("\n" + "=" * 45)
print("            RESULTS")
print("=" * 45)
# result section upper

for i in range(families):
    start = i * per_family
    end   = start + per_family
    group = phone_numbers[start:end]
    print(f"\n📁 EntryOperator {i + 1}:\n")
    for num in group:
        print(f"{num}")

# --- Leftover / Remainder ---
if remainder > 0:
    leftover = phone_numbers[families * per_family:]
    print(f"\n⚠  Remainder ({remainder} number(s) not assigned):\n")
    for num in leftover:
        print(f"{num}")
else:
    print(f"\n✅ No remainder. Divided evenly!")

print("\n" + "=" * 45)
print(f"  Total   : {len(phone_numbers)} numbers")
print(f"  EntryOperator: {families}")
print(f"  Each gets: {per_family} numbers")
print(f"  Leftover : {remainder} number(s)")
print("=" * 45)