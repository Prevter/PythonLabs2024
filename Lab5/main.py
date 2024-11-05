def get_words(text: str) -> list:
    words = text.split()
    words = [word.strip(",.!?") for word in words]
    return words

def sort_words(words: list) -> list:
    ukrainian = []
    english = []
    for word in words:
        if word.isalpha():
            if ord("a") <= ord(word[0].lower()) <= ord("z"):
                english.append(word)
            else:
                ukrainian.append(word)
    ukrainian.sort()
    english.sort()
    return ukrainian + english

def main():
    try:
        with open("text.txt", "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("File not found")
        return
    except Exception as e:
        print(e)
        return

    sentence = text.split(".")[0]
    print(sentence)

    words = get_words(text)
    words = sort_words(words)
    print(f"Words count: {len(words)}")
    print(words)


if __name__ == "__main__":
    main()