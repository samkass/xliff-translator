import os
import argparse
import xml.etree.ElementTree as ET

from translator_deepl import DeepLTranslator
from translator_noop import NoopTranslator
from translator_openai import OpenAITranslator

ET.register_namespace('', 'urn:oasis:names:tc:xliff:document:1.2')
ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')

do_write = True


def process_xliff_file(xliff_path, translator, source_language):
    # Extract language code from the filename
    target_language_code = os.path.basename(xliff_path).split('.')[0]

    if source_language.upper() == target_language_code.upper():
        print(f"Skipping translation for {xliff_path} because source and target languages are the same.")
        return

    # Parse the XML file
    tree = ET.parse(xliff_path)
    root = tree.getroot()

    for file in root.findall('.//{urn:oasis:names:tc:xliff:document:1.2}file'):
        for trans_unit in file.findall('.//{urn:oasis:names:tc:xliff:document:1.2}trans-unit'):
            source = trans_unit.find('{urn:oasis:names:tc:xliff:document:1.2}source').text
            note = trans_unit.find('{urn:oasis:names:tc:xliff:document:1.2}note').text

            # Translate the source text
            translated_text = translator.translate_text(source, source_language, target_language_code, note)

            # Create or update the target element
            if translated_text:
                target = trans_unit.find('{urn:oasis:names:tc:xliff:document:1.2}target')
                if target is None:
                    target = ET.SubElement(trans_unit, 'target')
                target.text = translated_text
            else:
                print(f"No translation returned for '{source}'")
                raise Exception("Translation failed")

    if not do_write:
        print("Dry run, not writing to file")
    else:
        # Write back the modified XML to the file
        # Construct the new filename (e.g., 'orig-fr.xliff')
        orig_filename = 'orig-' + os.path.basename(xliff_path)
        orig_path = os.path.join(os.path.dirname(xliff_path), orig_filename)

        # Rename the original file
        print(f"Renaming original file to {orig_path}.")
        os.rename(xliff_path, orig_path)

        # Write the modified XML data to the original filename
        try:
            print(f"Writing translated file to {xliff_path}.")
            tree.write(xliff_path, encoding='UTF-8', xml_declaration=True)
            print(f"Success! Removing original file {orig_path}.")
            os.remove(orig_path)
        except Exception as e:
            print(f"An error occurred while writing the translated file: {e}")
            print(f"Restoring original file to {xliff_path}. (original file is {orig_path})")
            os.remove(xliff_path)
            os.rename(orig_path, xliff_path)


def process_xcloc_package(xloc_dir, translator, source_language):
    print(f"Processing .xcloc package at {xloc_dir}...")
    directory, filename = os.path.split(xloc_dir)

    # Extract the language code from the .xcloc filename
    language_code, _ = os.path.splitext(filename)

    # Construct the path to the specific .xliff file
    xliff_path = os.path.join(xloc_dir, 'Localized Contents', f'{language_code}.xliff')

    # Check if the .xliff file exists
    if os.path.isfile(xliff_path):
        process_xliff_file(xliff_path, translator, source_language)
    else:
        print(f"No .xliff file found for language code '{language_code}' in {xliff_path}")


def process_translations_dir(translations_dir, translator, source_language):
    if translations_dir.endswith('.xcloc'):
        process_xcloc_package(translations_dir, translator, source_language)
    else:
        print(f"Processing directory at {translations_dir}...")
        for root, dirs, files in os.walk(translations_dir):
            for adir in dirs:
                if adir.endswith('.xcloc'):
                    process_xcloc_package(os.path.join(root, adir), translator, source_language)


parser = argparse.ArgumentParser(description='Translate XLOC package using translation API.')
parser.add_argument('path', type=str, help='Path to the translations')
parser.add_argument('--engine', choices=['openai', 'deepl', 'noop'], default='deepl', nargs='?', help='Translation engine to use')
parser.add_argument('--source_language', type=str, default=None, nargs='?', help='Source language code (eg. "EN")')
args = parser.parse_args()
translator = None

if args.engine == 'openai':
    print(f"Translating text with OpenAI")
    translator = OpenAITranslator()
if args.engine == 'noop':
    print(f"Translating text with Noop")
    translator = NoopTranslator()
    do_write = False
else:
    print(f"Translating text with DeepL")
    translator = DeepLTranslator()

print(f"Processing translation package at {args.path} from language {args.source_language} with engine {args.engine}...")
process_translations_dir(args.path, translator, args.source_language)
