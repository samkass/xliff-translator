from dotenv import load_dotenv
import os
import sys
import xml.etree.ElementTree as ET
from openai import OpenAI
import langcodes

# Load environment variables from .env file
load_dotenv()

# Now you can use os.getenv to get your environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

ET.register_namespace('', 'urn:oasis:names:tc:xliff:document:1.2')
ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')


def get_language_name_from_code(code):
    # Use langcodes to get the full language name
    return langcodes.Language.get(code).language_name()


def translate_text(text, target_language, note):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Update the model if needed
                                                  messages=[
                                                      {"role": "system", "content": "You are a translator model."},
                                                      {"role": "user",
                                                       "content": f"Translate the text below (between the "
                                                                  f"<text></text> tags to {target_language}. Return "
                                                                  f"only the translated string (no <text></text> "
                                                                  f"tags). The "
                                                                  f"following translation note applies: '{note}'. "
                                                                  f"Text: <text>{text}</text>"}
                                                  ])
        translation = response.choices[0].message.content.strip()
        print(f"Translated text: {translation}")
        return translation
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None


def process_xliff_file(xliff_path):
    # Extract language code from the filename
    language_code = os.path.basename(xliff_path).split('.')[0]
    target_language = get_language_name_from_code(language_code)

    # Parse the XML file
    tree = ET.parse(xliff_path)
    root = tree.getroot()

    for file in root.findall('.//{urn:oasis:names:tc:xliff:document:1.2}file'):
        for trans_unit in file.findall('.//{urn:oasis:names:tc:xliff:document:1.2}trans-unit'):
            source = trans_unit.find('{urn:oasis:names:tc:xliff:document:1.2}source').text
            note = trans_unit.find('{urn:oasis:names:tc:xliff:document:1.2}note').text

            # Translate the source text
            translated_text = translate_text(source, target_language, note)

            # Create or update the target element
            if translated_text:
                target = trans_unit.find('{urn:oasis:names:tc:xliff:document:1.2}target')
                if target is None:
                    target = ET.SubElement(trans_unit, 'target')
                target.text = translated_text

    # Write back the modified XML to the file
    # Construct the new filename (e.g., 'orig-fr.xliff')
    orig_filename = 'orig-' + os.path.basename(xliff_path)
    orig_path = os.path.join(os.path.dirname(xliff_path), orig_filename)

    # Rename the original file
    os.rename(xliff_path, orig_path)

    # Write the modified XML data to the original filename
    print(f"Writing translated file to {xliff_path}. (saving original as {orig_path})")
    tree.write(xliff_path, encoding='UTF-8', xml_declaration=True)


def process_xloc_package(xloc_dir):
    directory, filename = os.path.split(xloc_dir)

    # Extract the language code from the .xcloc filename
    language_code, _ = os.path.splitext(filename)

    # Construct the path to the specific .xliff file
    xliff_path = os.path.join(xloc_dir, 'Localized Contents', f'{language_code}.xliff')

    # Check if the .xliff file exists
    if os.path.isfile(xliff_path):
        process_xliff_file(xliff_path)
    else:
        print(f"No .xliff file found for language code '{language_code}' in {xliff_path}")


# Check if a command-line argument is provided
if len(sys.argv) < 2:
    print("Usage: python main.py <xloc_path>")
    sys.exit(1)

# The first command-line argument is the directory path
directory_path = sys.argv[1]
process_xloc_package(directory_path)
