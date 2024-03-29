# xliff-translator
A little Python utility which submits xliff/xloc files to an automated translation service and generates a new one with translations. PLEASE look over the translations before you blindly use them, as they are not guaranteed to be accurate.

## Usage
To get started:
1. Clone the repository and cd into the directory
2. Install the dependencies with `pip install -r requirements.txt`
3. Create an .env file in the local directory to store keys.
4. If you want to use OpenAI translation, add the OPENAI_API_KEY (and optionally OPENAI_MODEL, which defaults to "gpt-4") to the .env file like so: 
```
OPENAI_API_KEY=<your key here>
OPENAI_MODEL=gpt-3.5-turbo
```
5. If you want to use DeepL translation, add the DEEPL_API_KEY to the .env file like so: 
```
DEEPL_API_KEY=<your key here>
```
6. Run the app with `python main.py --engine=deepl <xloc_path>`, where "xloc_path" is the  xloc directory to translate. The `--engine` flag is optional and can be set to "openai" or "deepl". If not set, it will default to "deepl".

The application will then find the xliff file within the directory, use the directory name as the localization language, and submit the entries one at a time to ChatGPT's "gpt-4" model for translation, and insert the translations back into the .xliff file.

## Notes
To generate the .xloc file(s) in the first place, in XCode go to Product > Export Localizations... and select the languages you want to localize for. This will generate a .xloc file for each language, which you can then use with this utility to translate.

When the translations are complete, you can re-import the .xloc files into XCode by going to Product > Import Localizations... and selecting the .xloc files you want to import.

## Disclaimer

This is a quick little personal utility I wrote for myself and decided to share if anyone else finds it useful. It is not affiliated with OpenAI or Apple. I have only tested it with English as the primary language. No guarantee that it will generate translations that are correct, or at all. Use at your own risk.
