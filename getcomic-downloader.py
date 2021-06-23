import requests
from bs4 import BeautifulSoup
import argparse
import re
import json
import os
from urllib.parse import quote
import sys
import threading
import logging

url = "https://getcomics.info/page/{}/?s={}"
links_dict = {}

headers_dict = {
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
  "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6",
  "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
  "sec-ch-ua-mobile": "?0",
  "sec-fetch-dest": "document",
  "sec-fetch-mode": "navigate",
  "sec-fetch-site": "same-origin",
  "sec-fetch-user": "?1",
  "upgrade-insecure-requests": "1"
}

headers_dict2 = {
  "accept": "*/*",
  "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6",
  "origin": "https://disqus.com",
  "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
  "sec-ch-ua-mobile": "?0",
  "sec-fetch-dest": "script",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "cross-site",
  "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

def write_to_json(json_dict, filename):
    jsonv = json.dumps(json_dict, indent=True)
    with open(filename, "w") as f:
        f.write(jsonv)

def download_file(link, filename):
    r = requests.get(link, headers=headers_dict, allow_redirects=False)
    if ".zip" in link:
        filename = filename + ".zip"
    else:
        filename = filename + ".cbr"
    with open(os.path.join("downloads",filename), "wb") as f:
        f.write(r.content)

def getcomic_downloader(page, search):
    try:
        r = requests.get(url.format(page, search), headers=headers_dict)
        parsed_data = BeautifulSoup(r.content, "html.parser")
        posts_lists = parsed_data.find_all("article")
        for p in posts_lists:
            page_url = p.find_all("a")[2].get("href")
            heading = p.find_all("h1")[0].text
            r2 = requests.get(page_url, headers=headers_dict)
            page_parsed = BeautifulSoup(r2.content, "html.parser")
            download_button = str(page_parsed.find_all("div", {"class": "aio-button-center"})[0])
            link_re = re.compile(r"https:\/\/[a-zA-Z0-9.\/\%\-\=\+\:]*")
            link = link_re.findall(download_button)[0]
            print(link)
            links_dict[heading] = link
            download_file(link, heading)
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        pass
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This is getcomic doenloader")
    parser.add_argument("-o", "--output", help="This is for saving the links for the books in json", action="store_true")
    parser.add_argument("-s", "--speed", help="This will make the process speedup with threading but it will allocate a lot of ram so do not used it with too many pages", action="store_true")
    parser.add_argument("pages", type=str, help="The number of pages to download from")
    parser.add_argument("search", type=str, help="The name to search in getcomic")
    argv = parser.parse_args()
    pages = argv.pages.split("-")
    if len(pages) == 1:
        start = 1
        end = int(pages[0])
    else:
        if int(pages[0]) <= int(pages[1]):
            start = int(pages[0])
            end = int(pages[1])
        else:
            print("Start values must be less then the ending one")
            sys.exit(1)
    count = 0
    for page in range(start,end+1):
        count += 1
        print(page)
        print(quote(argv.search))
        if argv.speed:
            x = threading.Thread(target=getcomic_downloader, args=(page,quote(argv.search)))
            x.start()
        else:
            getcomic_downloader(page, quote(argv.search))
    if argv.output:
        write_to_json(links_dict,  "links.json")
