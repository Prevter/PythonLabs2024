from deep_translator import GoogleTranslator
from typing import Literal
from langdetect import detect_langs
from table_gen import table

LANGS = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar",
    "Armenian": "hy", "Azerbaijani": "az", "Basque": "eu", "Belarusian": "be", 
    "Bengali": "bn", "Bosnian": "bs", "Bulgarian": "bg", "Catalan": "ca",
    "Cebuano": "ceb", "Chinese (Simplified)": "zh-CN", "Chinese (Traditional)": "zh-TW", "Corsican": "co",
    "Croatian": "hr", "Czech": "cs", "Danish": "da", "Dutch": "nl", 
    "English": "en", "Esperanto": "eo", "Estonian": "et", "Ewe": "ee", 
    "Finnish": "fi", "French": "fr", "Frisian": "fy", "Galician": "gl", 
    "Georgian": "ka", "German": "de", "Greek": "el", "Gujarati": "gu",
    "Haitian Creole": "ht", "Hausa": "ha", "Hawaiian": "haw", "Hebrew": "iw",
    "Hindi": "hi", "Hmong": "hmn", "Hungarian": "hu", "Icelandic": "is",
    "Igbo": "ig", "Indonesian": "id", "Irish": "ga", "Italian": "it", 
    "Japanese": "ja", "Kannada": "kn", "Kazakh": "kk", "Khmer": "km", 
    "Korean": "ko", "Kurdish": "ku", "Kyrgyz": "ky", "Lao": "lo", 
    "Latin": "la", "Latvian": "lv", "Lithuanian": "lt", "Luxembourgish": "lb", 
    "Macedonian": "mk", "Malagasy": "mg", "Malay": "ms", "Malayalam": "ml",
    "Maltese": "mt", "Maori": "mi", "Marathi": "mr", "Mongolian": "mn", 
    "Myanmar": "my", "Nepali": "ne", "Norwegian": "no", "Nyanja": "ny", 
    "Pashto": "ps", "Persian": "fa", "Polish": "pl", "Portuguese": "pt", 
    "Punjabi": "pa", "Romanian": "ro", "Russian": "ru", "Samoan": "sm",
    "Scots Gaelic": "gd", "Serbian": "sr", "Sesotho": "st", "Shona": "sn", 
    "Sindhi": "sd", "Sinhala": "si", "Slovak": "sk", "Slovenian": "sl", 
    "Somali": "so", "Spanish": "es", "Sundanese": "su", "Swahili": "sw", 
    "Swedish": "sv", "Tagalog": "tl", "Tajik": "tg", "Tamil": "ta", 
    "Telugu": "te", "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", 
    "Urdu": "ur", "Uyghur": "ug", "Uzbek": "uz", "Vietnamese": "vi", 
    "Welsh": "cy", "Xhosa": "xh", "Yiddish": "yi", "Yoruba": "yo", "Zulu": "zu",
}

def Translate(text: str, source: str, dest: str) -> str:
    try:
        return GoogleTranslator(source=source, target=dest).translate(text)
    except Exception as e:
        return str(e)
    

def CodeLang(lang: str) -> str:
    if lang in LANGS:
        return LANGS[lang]
    for name, code in LANGS.items():
        if code == lang:
            return name
    return "Unknown language"


def LangDetect(text: str, set: Literal["lang", "confidence", "all"]) -> str:
    try:
        langs = detect_langs(text)
        if set == "lang":
            return langs[0].lang
        elif set == "confidence":
            return langs[0].prob
        elif set == "all":
            return f"{langs[0].lang} ({langs[0].prob})"
    except Exception as e:
        return str(e)
    

def LanguageList(out: Literal["screen", "file"], text: str = None) -> str:
    buffer = []
    fromLang = "en"
    try:
        if text:
            buffer.append(["N", "Language", "ISO-639 code", "Text"])
            fromLang = LangDetect(text, "lang")
        else:
            buffer.append(["N", "Language", "ISO-639 code"])

        n = 1
        for lang, code in LANGS.items():
            item = [n, lang, code]
            if text: item.append(Translate(text, fromLang, code))
            buffer.append(item)
            n += 1

        textTable = table.from_list(buffer)

        if out == "screen":
            print(textTable)
        elif out == "file":
            with open("langs.txt", "w", encoding="utf-8") as file:
                file.write(textTable)
        return "Ok"
    except Exception as e:
        return str(e)