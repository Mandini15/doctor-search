from urllib.request import Request, urlopen  # Python 3
import json
import os
import requests

save_dir = "vitals"

# REQUEST DETAILS
# Copied manually from dev tools
cookie = "__cfduid=d584a284df64da9ab545eaf2f671b6eb51557716405; PHPSESSID=9vtrf86hf0cd8q8j0djoln13da; __cfruid=0a6244231815d6bad23d1ca8f63f8b38c6ab46fb-1557716405; s_fid=0B95E2EBADFFF42F-22289E2E5740EC16; retarget=%7B%22spec%22%3A%5B%22dent%22%2C%22podt%22%2C%22plsg%22%5D%2C%22mid%22%3A%5B%221q2cxb%22%2C%221scznk%22%2C%22zs352h%22%5D%2C%22pspec%22%3A%5B%22dent%22%2C%22podt%22%2C%22plsg%22%5D%2C%22fspec%22%3A%5B%22dent-peri%22%2C%22pods-pods%22%2C%22plsg-plsg%22%5D%7D; s_sq=webmdp1global%3D%2526c.%2526a.%2526activitymap.%2526page%253Dvitals.com%25252Fdoctors%25252Fdr-ivona-percec%2526link%253DFind%252520a%252520doctor%252520-%252520doctor%252520reviews%252520and%252520ratings%2526region%253Dsearch-header%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dvitals.com%25252Fdoctors%25252Fdr-ivona-percec%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.vitals.com%25252F%2526ot%253DA; cf_clearance=bebbe4d3db6868a22dd65767b5a538befa81bbce-1557720310-300-150; rmid=1q2cxb%7C1scznk%7Czs352h; rspec=dent%7Cpodt%7Cplsg; rfspec=dent-peri%7Cpods-pods%7Cplsg-plsg; rpspec=dent%7Cpodt%7Cplsg; app-c[reviewIntercept]=1557721779825; rspex=4419%7C5122%7C2172%7C4590%7C5926"
location = "Philadelphia, PA"
save_dir = f"vitals/{location}"
lat_lng = "39.951639,-75.163808"
# Taken manually
num_pages = 417


def get_page_filename(page):
    return f"{save_dir}/page{page}.json"


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_json(data):
    filename = f"{save_dir}/combined.json"
    ensure_dir(filename)
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f)
    return filename


def save_text(text, file_path):
    ensure_dir(file_path)
    with open(file_path, 'w') as f:
        f.write(text)

# Take cookie from a browser request


def download_page(page):
    url = (
        f"https://www.vitals.com/search/ajax?query="
        f"&city_state={location}&latLng={lat_lng}"
        f"&ins_plan_company_name=IBC&display_type=Doctor"
        f"&page={page}&reqNo=1"
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.vitals.com/search?city_state=Philadelphia,%20PA&latLng=39.951639,-75.163808&display_type=Doctor",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Connection": "keep-alive",
        "Cookie": "__cfduid=d584a284df64da9ab545eaf2f671b6eb51557716405; PHPSESSID=9vtrf86hf0cd8q8j0djoln13da; __cfruid=0a6244231815d6bad23d1ca8f63f8b38c6ab46fb-1557716405; s_fid=0B95E2EBADFFF42F-22289E2E5740EC16; retarget=%5B%5D; s_sq=webmdp1global%3D%2526c.%2526a.%2526activitymap.%2526page%253Dvitals.com%25252F%2526link%253DSEARCH%2526region%253Dhomepage-hero%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dvitals.com%25252F%2526pidt%253D1%2526oid%253DSEARCH%2526oidt%253D3%2526ot%253DSUBMIT; cf_clearance=bebbe4d3db6868a22dd65767b5a538befa81bbce-1557720310-300-150",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

    response = requests.get(url, headers=headers)
    return response.text


def cached_or_downloaded_page_json(page):
    filename = get_page_filename(page)

    if not os.path.exists(filename):
        print(f"Downloading page {page} of {num_pages-1}")
        response = download_page(page)
        save_text(response, filename)
        return json.loads(response)

    with open(filename, 'r') as f:
        print(f"Reading local page {page} of {num_pages-1}")
        return json.load(f)


def download_all_doctors():
    all_docs = []
    for p in range(num_pages):
        data = cached_or_downloaded_page_json(p)
        docs = data['hits']['hits']
        all_docs.extend(docs)

    filename = save_json(all_docs)
    print("Finished")
    print(f"Results saved to: {filename}")


if __name__ == "__main__":
    download_all_doctors()
