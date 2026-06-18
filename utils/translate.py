from deep_translator import GoogleTranslator

LANGUAGES = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Bengali": "bn",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Urdu": "ur"
}

def translate_text(text, target_language):
    try:
        target = LANGUAGES.get(target_language, "en")

        translated = GoogleTranslator(
            source="auto",
            target=target
        ).translate(text)

        return translated

    except Exception as e:
        return f"Translation Error: {str(e)}"