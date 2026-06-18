from deep_translator import GoogleTranslator

text = "Hello, how are you?"

translated = GoogleTranslator(
    source="auto",
    target="te"
).translate(text)

print(translated)