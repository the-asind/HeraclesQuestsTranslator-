import os
import json
from translatepy import Translator
import re

translator = Translator()
total_files = 0
processed_files = 0


def translate_string(s, lang_to):
    if len(s) < 3 or not re.search(r'\w', s):
        return s
    translated = translator.translate(s, lang_to).result
    return translated.replace('"', '\\"')


def translate_strings(strings, lang_to):
    combined_text = "\n".join(strings)
    if len(combined_text) < 3 or not re.search(r'\w', combined_text):
        return combined_text
    translated_text = translator.translate(combined_text, lang_to).result
    translated_strings = translated_text.split("\n")
    return translated_strings


def translate_json(data, lang_to):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "translate" or key == "title" and isinstance(value, str):
                data[key] = translate_string(value, lang_to)
            elif key == "description" and isinstance(value, list):
                data[key] = translate_strings(value, lang_to)
            else:
                translate_json(value, lang_to)
    elif isinstance(data, list):
        for item in data:
            translate_json(item, lang_to)


def process_json_file(file_path, lang_to):
    global processed_files
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    translate_json(data, lang_to)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    processed_files += 1


def process_directory(directory, lang_to):
    global total_files
    for root, _, files in os.walk(directory):
        total_files += len([file for file in files if file.endswith('.json')])

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                full_path = os.path.join(root, file)
                relative_path = full_path.replace(directory, "~")
                progress = (processed_files / total_files) * 100
                print(f"{progress:.0f}% Processing file: {relative_path}")
                process_json_file(full_path, lang_to)


def select_language():
    language = input("Enter the target language (e.g., 'ru', 'rus', even 'russa', etc.): ")
    return language


if __name__ == '__main__':
    directory = input(
        'Enter the path to your quests directory:\nExample: C:\\Users\\<...>\\.minecraft\\config\\heracles\\quests\\\nInput: ')
    lang_to = select_language()
    process_directory(directory, lang_to)
