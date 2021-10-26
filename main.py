#!/usr/bin/python
import random
import time
import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import re


def get_videocard_data(url):
    headers = {
        "user - agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 95.0.4638.54 Safari / 537.36"
    }

    videocard_list = []
    req = requests.get(url, headers=headers)
    # print(req.text)
    # with open('project.html', 'w', encoding='utf-8') as file:
    #     file.write(req.text)
    #
    # with open('project.html', 'r', encoding='utf-8') as file:
    #     src = file.read()
    soup = BeautifulSoup(req.text, 'lxml')
    videocards = soup.find_all("div", class_="model-short-div")
    for videocard in videocards:
        time.sleep(random.randrange(2, 4))
        try:
            videocard_url = f"https://www.e-katalog.ru/prices" + videocard.find("span", class_="u").find_parent("a").get("href").rstrip('.htm')
            vs_name = videocard.find('span', class_='u').text

        except Exception:
            print("Ничего не нашлось")
            continue

        req = requests.get(url=videocard_url, headers=headers)

        soup = BeautifulSoup(req.text, 'lxml')
        try:
            lower_price = soup.find("div", class_=re.compile("^desc-big-price")).find("span").text
            lower_price = ''.join(lower_price.split())
            print(lower_price)

        except Exception:
            lower_price = "Цену стоит перепроверить на сайте"

        videocard_list.append(
            {
                "Название видеокарты": vs_name,
                "Ссылка на видеокарту": videocard_url,
                "Минимальная цена": lower_price
            }
        )
        with open('data/videocards.csv', 'a', newline='') as csv_file:
            file_writer = csv.writer(csv_file, delimiter=';')
            file_writer.writerow([vs_name, videocard_url, f"{lower_price},00 р."])

    with open('data/result.json', 'a', encoding='utf-8') as file:
        json.dump(videocard_list, file, indent=4, ensure_ascii=False)


def main():
    path1 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/result.json')
    path2 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/videocards.csv')
    if os.path.exists(path1):
        os.remove(path1)
    if os.path.exists(path2):
        os.remove(path2)
    for page_index in range(0, 74):
        url = f"https://www.e-katalog.ru/ek-list.php?katalog_=189&page_={page_index}"
        get_videocard_data(url)
        print(f"Итерация #{page_index + 1} из 74")


main()
