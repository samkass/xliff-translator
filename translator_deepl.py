from dotenv import load_dotenv
import os

import deepl

from translator import Translator

load_dotenv()


class DeepLTranslator(Translator):
    _instance = None
    deepl_client = deepl.Translator(os.getenv('DEEPL_API_KEY'))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DeepLTranslator, cls).__new__(cls)
            cls._instance.config = {}
            # Initialize your configuration settings here
        return cls._instance

    def translate_text(self, text, source_language, target_language, note):
        if target_language.upper() == "EN":
            target_language = "EN-US"
        try:
            if source_language is None:
                text = self.deepl_client.translate_text(text,
                                                        target_lang=target_language.upper(),
                                                        context=note)
            else:
                text = self.deepl_client.translate_text(text,
                                                        source_lang=source_language.upper(),
                                                        target_lang=target_language.upper(),
                                                        context=note)
            translation = text.text
            print(f"Translated text: {translation}")
            return translation
        except Exception as e:
            print(f"An error occurred during translation: {e}")
            return None
