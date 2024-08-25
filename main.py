import os
import json
from translatepy import Translator
import re

translator = Translator()


def translate_string(s, lang_to='ru'):
    if len(s) < 3 or not re.search(r'\w', s):
        return s
    translated = translator.translate(s, lang_to).result
    return translated.replace('"', '\\"')


def translate_json(data, lang_to='ru'):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "translate" and isinstance(value, str):
                data[key] = translate_string(value, lang_to)
            elif key == "description" and isinstance(value, list):
                data[key] = [translate_string(item, lang_to) for item in value]
            else:
                translate_json(value, lang_to)
    elif isinstance(data, list):
        for item in data:
            translate_json(item, lang_to)


def process_json_file(file_path, lang_to='ru'):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    translate_json(data, lang_to)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def process_directory(directory, lang_to='ru'):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                process_json_file(os.path.join(root, file), lang_to)


if __name__ == '__main__':
    directory = input('Enter the path to your quests directory:\nExample: C:\\Users\\<...>\\.minecraft\\config\\heracles\\quests\\\nInput: ')
    process_directory(directory)
