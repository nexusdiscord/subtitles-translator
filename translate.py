# ========= #
# Libraries #
# ========= #

import os
from deep_translator import GoogleTranslator
import chardet

# ========= #
# Variables #
# ========= #

INPUT_FOLDER = "./sub"
OUTPUT_FOLDER = "./out"

SOURCE_LANGUAGE = "da"
TARGET_LANGUAGE = "id"

DATA_GROUP_SEPARATOR = "\n\n"
GROUP_SEPARATOR = "\n"

# ====== #
# Script #
# ====== #

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

translator = GoogleTranslator(source=SOURCE_LANGUAGE, target=TARGET_LANGUAGE)

subs_filenames = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".srt")]

for file_idx, filename in enumerate(subs_filenames):
    print(f"\n\nTranslating file {file_idx+1}/{len(subs_filenames)}: {filename}")
    
    file_path = os.path.join(INPUT_FOLDER, filename)
    encoding = detect_encoding(file_path)

    with open(file_path, mode="r", encoding=encoding) as file:
        content = file.read()
    
    subs_data_groups = content.split(DATA_GROUP_SEPARATOR)
    subs_data_groups_translated = []
    for group_idx, data_group in enumerate(subs_data_groups):
        if not data_group.strip():  # Skip empty data groups, solves issue #1
            continue

        num, time, *subs = data_group.split(GROUP_SEPARATOR)

        print(
            f"Translating subtitle group {group_idx+1}/{len(subs_data_groups)}",
            end="\r",
        )

        subs_translated = [translator.translate(text=s) for s in subs]

        data_group_translated = GROUP_SEPARATOR.join([num, time] + subs_translated)
        subs_data_groups_translated.append(data_group_translated)

    content_translated = DATA_GROUP_SEPARATOR.join(subs_data_groups_translated)

    output_file_path = os.path.join(OUTPUT_FOLDER, f"translated_{filename}")
    with open(output_file_path, mode="w", encoding="utf-8-sig") as file:
        file.write(content_translated)
