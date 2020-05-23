import requests
import urllib.request
import re
import os
import time
import threading
import tkinter as tk
from pathlib import Path
from bs4 import BeautifulSoup


class downloader(threading.Thread):

    def __init__(self, address, url, text):
        threading.Thread.__init__(self)
        self.text = text
        self.url = url.strip()
        self.address = address.strip()
        return

    def run(self):
        self.downloadManga(self.url, self.address)

    # download the entire manga
    def downloadManga(self, target, address):
        try:
            req = requests.get(url=target).content
            bf = BeautifulSoup(req, 'html.parser')
            parady = bf.find('a', attrs={'href': re.compile("/parody.*")})
            title = bf.h2.text.replace("/", " slash ")
            path = self.createDir(parady, title, address)
            length = len(bf.find("div", class_="container", id="thumbnail-container").findAll("div"))
        except Exception:
            self.print("Page not Found\n\nFormat should be \nhttps://nhentai.net/g/xxxxxx/")
            return
        if not path: return
        self.print("\n____________Downloading____________\n" + title + "....")
        self.download_pages(target, path, length)
        self.print("\n____________Finishied______________\n\n")

    # create a directory for new manga
    def createDir(self, parady, title, address):
        if (not parady):
            parady = "original"
        else:
            parady = parady.text.split(" (")[0]
            parady = parady.replace("?", "")
            parady = parady.replace("*", "")
        title = title.replace("?", "")
        title = title.replace("*", "")
        path = address + parady + "/" + title
        if os.path.isdir(path):
            self.print("Manga already exist\n\n")
            return 0
        Path(path).mkdir(parents=True, exist_ok=True)
        return path + "/"

    # call page_downloaders in multiple threads
    def download_pages(self, target, path, length):
        downloaders = [threading.Thread(target=self.page_downloader, args=(target, path, str(i + 1),))
                       for i in range(length)]
        for threads in downloaders:
            time.sleep(0.1)
            threads.start()
        for threads in downloaders: threads.join()

    # download a single page
    def page_downloader(self, target, path, index):
        while 1:
            req = requests.get(url=target + index + "/").content
            bf = BeautifulSoup(req, 'html.parser')
            if bf.title.text != "503 Service Temporarily Unavailable": break
        imgURL = bf.find("div", class_="container").find("img").get("src")
        urllib.request.urlretrieve(imgURL, path + index + ".jpg")
        self.print("Downloading page " + index + "...")

    # print in the window
    def print(self, s):
        self.text.insert(tk.END, s + "\n")
        self.text.see(tk.END)
