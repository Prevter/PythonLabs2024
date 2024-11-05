from google_translate import translate

def main():
    mode = input("Enter mode (screen, file): ")
    if mode not in ["screen", "file"]:
        print("Unknown mode")
        return

    msg = input("Enter text (or leave empty): ")
    res = translate.LanguageList(mode, msg if len(msg) > 0 else None)
    print('.' * 20)
    print(res)

if __name__ == "__main__":
    main()