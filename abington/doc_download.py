# Created by Eric Goldner (5/12/2019)

import urllib.request
import json
import math
import urllib.request
import shutil
import os.path

root_dir = "results"


def process_files():
    results = []
    page_count = None
    page_size = 200
    page = 1
    while page_count is None or page <= page_count:
        raw_response = get_page_response(page, page_size)
        response = json.loads(raw_response)
        total_records = int(response["TotalRecords"])
        page_count = math.ceil(total_records / page_size)
        matching_docs = [d for d in response["Values"] if filter_doc(d)]
        results.extend(matching_docs)
        for i, doc in enumerate(matching_docs):
            if i % 25 == 0:
                print(f"Downloading image {i} / {len(matching_docs)}")
            download_images(doc["Images"])

        page += 1

    save_json(results)


def download_file(url, file_name):
    with urllib.request.urlopen(url) as response, \
            open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def save_json(data):
    with open('abington-docs-results.json', 'w', encoding='utf8') as f:
        json.dump(data, f)


def get_page_response(page, page_size):
    file_name = f"{root_dir}/page_{page}.json"
    url = (f"https://www.abingtonhealth.org/api/providers/"
           f"?version=2&pageNumber={page}&"
           f"pageSize={page_size}&sort=1&fields=all")

    if not os.path.exists(file_name):
        print(f"Downloading URL: {url}")
        download_file(url, file_name)

    with open(file_name, 'r', encoding='utf8') as f:
        print(f"Reading file: {file_name}")
        return f.read()


def filter_doc(doc: dict):
    # Remove this to activate filter, leave it commented to filter later on
    return True

    for tax in [
        tax for tax
        in doc["Taxonomy"]
        if tax["FacetPropertyName"] == "Specialties"
    ]:
        # You can add a filter here
        return any(t["Name"] == "Internal Medicine" for t in tax["Terms"])

    return False


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_images(sources):
    url_prefix = "https://www.abingtonhealth.org"
    for src in sources:
        url = f"{url_prefix}{src['Path']}"
        file_path = f"{root_dir}/img/{src['FileName']}"
        ensure_dir(file_path)
        if not os.path.exists(file_path):
            download_file(url, file_path)


if __name__ == '__main__':
    process_files()
