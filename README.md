# xliff-translator
A little Python utility which submits xliff/xloc files to ChatGPT and generates a new one with translations. PLEASE look over the translations before you blindly use them, as they are not guaranteed to be accurate.

## Usage
To get started:
1. Clone the repository and cd into the directory
2. Install the dependencies with `pip install -r requirements.txt`
3. Create an .env file in the local directory with your OpenAI API key, like so: 
```
OPENAI_API_KEY=<your key here>
```
4. Run the app with `python main.py <xloc_path>`, where "xloc_path" is the  xloc directory to translate.

The application will then find the xliff file within the directory, use the directory name as the localization language, and submit the entries one at a time to ChatGPT's "gpt-3.5-turbo" model for translation, and insert the translations back into the .xliff file.

## Notes
To generate the .xloc file(s) in the first place, in XCode go to Product > Export Localizations... and select the languages you want to localize for. This will generate a .xloc file for each language, which you can then use with this utility to translate.

When the translations are complete, you can re-import the .xloc files into XCode by going to Product > Import Localizations... and selecting the .xloc files you want to import.

## Disclaimer

This is a quick little personal utility I wrote for myself and decided to share if anyone else finds it useful. It is not affiliated with OpenAI or Apple. I have only tested it with English as the primary language. No guarantee that it will generate translations that are correct, or at all. Use at your own risk.
