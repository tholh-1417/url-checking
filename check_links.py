#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from urlextract import URLExtract
import requests

# URLs to skip over
blacklisted = os.getenv("INPUT_BLACKLIST", "").split(",")

files = os.getenv('INPUT_FILES').split(",")
repo = os.getenv("GITHUB_REPOSITORY")
links = []
exit_status = 0

def remove_duplicates(urls):
    return list(set(urls))

for file in files:
    print(f"Collecting URLs from {file}")
    filepath = "https://raw.githubusercontent.com/" + repo + "/master/" + file
    text = requests.get(filepath).text

    extractor = URLExtract()
    file_links = extractor.find_urls(text)

    # Remove mailto links
    links = [url for url in file_links if "mailto://" not in url]
    linksToRequest = []

    # Remove blacklisted links
    for link in links:
        if link in blacklisted:
            print(f"Removed {link}")
        else:
            linksToRequest.append(link)

    print(f"Checking URLs from {file}")

    # Remove Duplicate links
    linksToRequest = remove_duplicates(linksToRequest)

    print(f"Removing duplicate URLs from {file}")

    for url in linksToRequest:
        try:
            request = requests.get(url)
            if request.status_code == 200:
                print(f"✓ 200 {url}")
            elif request.status_code >= 400:
                print(f"✕ {request.status_code} {url}")
                exit_status = 1
            else:
                print(f"⚪ {request.status_code} {url}")

        except:
            print(f"✕ ERR {url}")

            # Continue through all URLs but fail test at the end
            exit_status = 1
            continue
    file = open("test.txt", "w")
    file.write( "Python là ngôn ngữ tốt nhất");
    # Đóng file
    file.close()
    # Newline to separate URLs from different files
    print()

exit(exit_status)
