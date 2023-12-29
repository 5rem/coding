import os
import json
import argparse

def check_description_for_keyword(file_path, keyword):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for item in data:
            description = item.get("description")
            if description is not None and f" {keyword.lower()} " in f" {description.lower()} ":
                return item.get("html_url", ""), os.path.dirname(file_path), os.path.basename(file_path)
        return None, os.path.dirname(file_path), os.path.basename(file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search for a keyword in JSON files.')
    parser.add_argument('-k', '--keyword', type=str, required=True, help='The keyword to search for')
    parser.add_argument('-d', '--base_dir', type=str, required=True, help='The base directory to search in')
    args = parser.parse_args()

    base_dir = args.base_dir
    keyword = args.keyword

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                url, directory, file_name = check_description_for_keyword(file_path, keyword)
            
                if url:
                    print(f"\033[1;32m{keyword.ljust(10)}目录 \033[0m{directory}\{file_name.ljust(30)} \033[1;32m链接 \033[0m{url}")
