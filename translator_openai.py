from dotenv import load_dotenv
import os
from openai import OpenAI
from translator import Translator
import langcodes

load_dotenv()


class OpenAITranslator(Translator):
    _instance = None
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAITranslator, cls).__new__(cls)
            cls._instance.config = {}
            # Initialize your configuration settings here
        return cls._instance

    def get_language_name_from_code(code):
        # Use langcodes to get the full language name
        return langcodes.Language.get(code).language_name()

    def translate_text(self, text, target_language, note):
        try:
            target_language = self.get_language_name_from_code(target_language)
            if note is None:
                prompt_note = ""
            else:
                prompt_note = f"For context, after it is translated, the text will be used here in the app: '{note}'."
            response = self.openai_client.chat.completions.create(model="gpt-3.5-turbo",  # Update the model if needed
                                                                  messages=[
                                                                      {"role": "system", "content": "You are a translator model."},
                                                                      {"role": "user",
                                                                       "content": f"Translate the text between the "
                                                                                  f"<text></text> tags to {target_language}. Return "
                                                                                  f"only the translated string (no <text></text> "
                                                                                  f"tags). Be careful with legal terms such as "
                                                                                  f"'patent-pending'. {prompt_note}"
                                                                                  f"<text>{text}</text>"}
                                                                  ])
            translation = response.choices[0].message.content.strip()
            print(f"Translated text: {translation}")
            return translation
        except Exception as e:
            print(f"An error occurred during translation: {e}")
            return None
