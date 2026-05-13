words = {
    "chair": "chari",
    "table": "tablile",
    "computer": "pc",
    "electricity": "karent"
}

# Create reverse dictionary (meaning -> word) once, not repeatedly
reverse_words = {v: k for k, v in words.items()}

# Combine both dictionaries for bi-directional lookup
combined = {**words, **reverse_words}


def translate(word):
    """Translate a word in either direction (English -> Other, Other -> English)."""
    word_lower = word.lower()
    
    if word_lower in combined:
        return combined[word_lower]
    else:
        return "Translation not found"


if __name__ == "__main__":
    print("=" * 50)
    print("Bi-directional Translator")
    print("=" * 50)
    print("Dictionary loaded:")
    for eng, other in words.items():
        print(f"  {eng} ↔ {other}")
    print("-" * 50)
    
    while True:
        user_input = input("\nEnter a word to translate (or 'exit' to quit): ").strip()
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        if not user_input:
            print("Please enter a valid word.")
            continue
        
        translation = translate(user_input)
        print(f"✓ Translation: {translation}")











