from deep_translator import GoogleTranslator

translator = GoogleTranslator(source="auto", target="km")

def translate_to_khmer(text):
    """
    Translate text to Khmer
    """
    try:
        return translator.translate(text)
    except Exception:
        return text
