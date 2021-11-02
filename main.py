import random
import requests
import time
import json
import csv
import os
import re

from concurrent.futures import ThreadPoolExecutor, wait
from bs4 import BeautifulSoup


def get_videocard_data(url: str) -> None:
    """
    Функция получает объекты карточек HTML страницы с инофрмацией о видеокартах.
    С помощью библиотеки Beautifulsoup происходит синтаксический разбор страницы,
    откуда получает инофармацию о видеокарте
    :param url: Страница e-katalog'а с параметром пагинации
    :return: в файл result.json и videocards.csv сохраняется информация обо всех видеокартах
            Название, URL, минимальная стоимость.
    """
    headers: dict = {
        "user - agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 95.0.4638.54 Safari / 537.36"
    }

    videocard_list: list = []

    # Делаем запрос на страницу каталога
    req = requests.get(url, headers=headers)

    # Создаем объект BeautifulSoup для разбора страницы
    soup = BeautifulSoup(req.text, 'lxml')

    # Получаем все объекты в виде карточек видеокарт
    videocards = soup.find_all("div", class_=re.compile("^model-short-div"))

    # Цикл по каждой карточке
    for videocard in videocards:
        vs_name = ''

    # Пробуем найти URL и название видеокарты, так как начиная с 24 страницы html код сайта меняется
        try:
            videocard_url = f"https://www.e-katalog.ru/prices" + videocard.find("span", class_="u").find_parent(
                "a").get("href").rstrip('.htm')
            vs_name = videocard.find('span', class_='u').text

        except Exception:
            videocard_url = "Ссылка не найдена"

    # Если URL или имя не найдены, пробуем второй способ поиска
            try:
                videocard_url = videocard.find("td", class_=re.compile("^model-short-info")).find("a").get("href")
                vs_name = videocard.find("td", class_=re.compile("^model-short-info")).find("a").get("title")
                vs_name = vs_name.split('\n')
                vs_name = vs_name[0]
            except Exception:
                print("Имя не найдено")

    # Начиная с 24 страницы, ссылка содержит параметр onmouseover, тогда в url видеокарты попадает символ #
        if videocard_url == '#':
            videocard_url = videocard.find("td", class_=re.compile("^model-short-info")).find("a").get("onmouseover")
            videocard_url = videocard_url.split('\"')[1]

    # Находим минимальную цену на видеокарту
        try:
            lower_price = videocard.find("td", class_="model-hot-prices-td").find("a").find("span")
            lower_price = lower_price.text
            lower_price = ''.join(lower_price.split())
        except Exception:
            lower_price = 'Цена не найдена'
            print("цена не найдена")
            continue

    # Подготавливаем список для серриализации
        videocard_list.append(
            {
                "Название видеокарты": vs_name,
                "Ссылка на видеокарту": videocard_url,
                "Минимальная цена": lower_price
            }
        )

    # Заносим информацию в csv файл
        with open('data/videocards.csv', 'a', newline='', encoding='utf-8') as csv_file:
            file_writer = csv.writer(csv_file, delimiter=';')
            file_writer.writerow([vs_name, videocard_url, f"{lower_price},00 р."])

    # Сохраняем информацию в json
    with open('data/result.json', 'a', encoding='utf-8') as file:
        json.dump(videocard_list, file, indent=4, ensure_ascii=False)


def main() -> None:
    # Проверяем наличие в папке data файлов result.json и videocard.csv и удаляем их чтобы обновить информацию
    path1 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/result.json')
    path2 = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/videocards.csv')
    if os.path.exists(path1):
        os.remove(path1)
    if os.path.exists(path2):
        os.remove(path2)
    futures = []
    time_start = time.time()

    # Используем встроенный модуль concurrent.futures для создания многопоточности при парсинге сайта
    with ThreadPoolExecutor() as executor:
        for page_index in range(0, 74):
            url = f"https://www.e-katalog.ru/ek-list.php?katalog_=189&page_={page_index}"
            futures.append(executor.submit(get_videocard_data, url))
            time.sleep(random.randrange(2, 4))
            print(f"Итерация #{page_index + 1} из 74")
    # Функция ожидающая завершения работы всех потоков
    wait(futures)
    time_end = time.time()
    print(f"Время выполнения скрипта - {(time_end - time_start) // 60} мин "
          f"{((time_end - time_start) - ((time_end - time_start) // 60))}")


main()


# for page_index in range(0, 1):
#         url = f"https://www.e-katalog.ru/ek-list.php?katalog_=189&page_={page_index}"
#         get_videocard_data(url)
#         time.sleep(random.randrange(2, 4))
#         print(f"Итерация #{page_index + 1} из 74")


# with ThreadPoolExecutor() as executor:
#     for page_index in range(0, 74):
#         url = f"https://www.e-katalog.ru/ek-list.php?katalog_=189&page_={page_index}"
#         futures.append(executor.submit(get_videocard_data, url))
#         time.sleep(random.randrange(2, 4))
#         print(f"Итерация #{page_index + 1} из 74")
#     wait(futures)