from translator import Translator


# For testing or when you don't want to use a real translation service
class NoopTranslator(Translator):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NoopTranslator, cls).__new__(cls)
            cls._instance.config = {}
            # Initialize your configuration settings here
        return cls._instance

    def translate_text(self, text, source_language, target_language, note):
        translation = text
        print(f"Translated text: {translation}")
        return translation
