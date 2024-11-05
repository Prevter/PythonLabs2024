from google_translate import translate as gtrans
from deep_translate import translate as dtrans
import json, os

def load_config(path: str) -> dict:
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        return {"error": str(e)}

def get_or_quit(cfg: dict, key: str) -> str:
    if key in cfg:
        return cfg[key]
    print(f"Error: '{key}' not found in config.json")
    exit()

def read_until(text: str, chars: int, words: int, sentences: int) -> str:
    buffer = []
    for char in text:
        if len(buffer) >= chars: break
        if buffer.count(" ") >= words: break
        if buffer.count(".") >= sentences: break
        buffer.append(char)
    return "".join(buffer)

def main():
    config = load_config("config.json")
    if "error" in config:
        print(config["error"])
        return
    
    # Read config
    file = get_or_quit(config, "file")
    lang = get_or_quit(config, "lang")
    output = get_or_quit(config, "output")
    chars = get_or_quit(config, "chars")
    words = get_or_quit(config, "words")
    sentences = get_or_quit(config, "sentences")
    original_lang = get_or_quit(config, "original-lang")

    if output not in ["screen", "file"]:
        print("Error: 'output' must be 'screen' or 'file'")
        return
    
    # Check if file exists
    if not os.path.exists(file):
        print(f"Error: file '{file}' not found")
        return
    
    print(f"Reading file '{file}'")

    # Read file
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    text = read_until(text, chars, words, sentences)
    res = gtrans.Translate(text, original_lang, lang)

    if output == "screen":
        print(f"Target language: {lang}")
        print(res)
    elif output == "file":
        try:
            extension = file.split(".")[-1]
            file = file.replace(f".{extension}", f"_{lang}.{extension}")
            with open(file, "w", encoding="utf-8") as f:
                f.write(res)
            print("Ok")
        except Exception as e:
            print(str(e))
    

if __name__ == "__main__":
    main()