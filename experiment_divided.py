import re
import tkinter as tk
from tkinter import messagebox

def divide():
    raw = text_input.get("1.0", tk.END)
    phone_numbers = [
        n.strip()
        for n in re.split(r'[\s,;\n,;]+', raw)
        if n.strip().isdigit()
    ]

    if not phone_numbers:
        messagebox.showerror("Error", "No valid phone numbers found!")
        return

    try:
        families = int(family_entry.get())
        if families <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number of families!")
        return

    if families > len(phone_numbers):
        messagebox.showerror("Error", f"Families ({families}) cannot exceed numbers ({len(phone_numbers)})!")
        return

    per_family = len(phone_numbers) // families
    remainder  = len(phone_numbers) % families

    # --- Build result text ---
    result = "=" * 45 + "\n"
    result += "            RESULTS\n"
    result += "=" * 45 + "\n"

    for i in range(families):
        start = i * per_family
        group = phone_numbers[start:start + per_family]
        result += f"\n📁 EntryOperator {i + 1}:\n"
        result += "\n".join(group) + "\n"

    if remainder > 0:
        leftover = phone_numbers[families * per_family:]
        result += f"\n⚠  Remainder ({remainder} number(s) not assigned):\n"
        result += "\n".join(leftover) + "\n"
    else:
        result += "\n✅ No remainder. Divided evenly!\n"

    result += "\n" + "=" * 45 + "\n"
    result += f"  Total        : {len(phone_numbers)} numbers\n"
    result += f"  EntryOperator: {families}\n"
    result += f"  Each gets    : {per_family} numbers\n"
    result += f"  Leftover     : {remainder} number(s)\n"
    result += "=" * 45

    # --- Show result ---
    result_box.config(state=tk.NORMAL)
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, result)
    result_box.config(state=tk.DISABLED)

    count_label.config(text=f"✅ {len(phone_numbers)} numbers detected")

# --- GUI Setup ---
root = tk.Tk()
root.title("Phone Number Divider")
root.geometry("600x680")
root.config(bg="#0d0f14")

FONT      = ("Courier New", 10)
FONT_BOLD = ("Courier New", 11, "bold")
BG        = "#0d0f14"
SURFACE   = "#161922"
ACCENT    = "#00e5a0"
TEXT      = "#e8eaf2"
MUTED     = "#6b7280"

tk.Label(root, text="📞 PHONE NUMBER DIVIDER", font=("Courier New", 16, "bold"),
         bg=BG, fg=ACCENT).pack(pady=(20, 2))
tk.Label(root, text="Paste numbers · Set families · Click Divide",
         font=FONT, bg=BG, fg=MUTED).pack(pady=(0, 15))

# --- Phone input ---
tk.Label(root, text="Paste Phone Numbers:", font=FONT_BOLD, bg=BG, fg=TEXT, anchor="w").pack(fill="x", padx=20)
text_input = tk.Text(root, height=10, font=FONT, bg=SURFACE, fg=TEXT,
                     insertbackground=ACCENT, relief="flat", padx=10, pady=10)
text_input.pack(fill="x", padx=20, pady=(4, 4))

count_label = tk.Label(root, text="", font=FONT, bg=BG, fg=ACCENT)
count_label.pack(anchor="w", padx=20)

# --- Live counter ---
def on_type(event=None):
    raw = text_input.get("1.0", tk.END)
    nums = [n.strip() for n in re.split(r'[\s,;\n]+', raw) if n.strip().isdigit()]
    count_label.config(text=f"✅ {len(nums)} numbers detected" if nums else "")

text_input.bind("<KeyRelease>", on_type)
text_input.bind("<<Paste>>", lambda e: root.after(10, on_type))

# --- Family input + button ---
frame = tk.Frame(root, bg=BG)
frame.pack(fill="x", padx=20, pady=10)

tk.Label(frame, text="Number of Families:", font=FONT_BOLD, bg=BG, fg=TEXT).pack(side="left")
family_entry = tk.Entry(frame, width=6, font=FONT_BOLD, bg=SURFACE, fg=ACCENT,
                        insertbackground=ACCENT, relief="flat", justify="center")
family_entry.pack(side="left", padx=10)

tk.Button(frame, text="  DIVIDE  ", font=FONT_BOLD, bg=ACCENT, fg="#000",
          relief="flat", cursor="hand2", command=divide).pack(side="left")

# --- Result box ---
tk.Label(root, text="Results:", font=FONT_BOLD, bg=BG, fg=TEXT, anchor="w").pack(fill="x", padx=20)
result_box = tk.Text(root, height=16, font=FONT, bg=SURFACE, fg=TEXT,
                     relief="flat", padx=10, pady=10, state=tk.DISABLED)
result_box.pack(fill="both", expand=True, padx=20, pady=(4, 20))

root.mainloop()