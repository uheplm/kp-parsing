import time
import tkinter
import tkinter as tk
import requests
import io
from bs4 import BeautifulSoup
import matplotlib.pyplot as plot

# tkinter для удобства просмотра
root = tk.Tk()
root.title("Парсинг Кинопоиска")
root.geometry("600x500")
canvas = tkinter.Canvas(root, height=500, width=600)

# Получение данных с кинопоиска
# При частом запуске выдает капчу, поэтому либо запускать 1 раз, либо вставлять данные напрямую в хтмлки
def fetch_data():
    status = []
    for i in range(1, 6):
        url = f'https://www.kinopoisk.ru/lists/series-top250/?page={i}&tab=all'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }
        html = requests.get(url=url, headers=headers)
        time.sleep(5)
        status.append(html.status_code)
        with io.open(f'temp{i}.html', "w", encoding="utf-8") as file:
            file.write(html.text)
            file.close()
    return status


# Загрузка ранее скачанных страниц
def get_pages():
    output = []
    for i in range(1, 6):
        with io.open(f'temp{i}.html', "r", encoding="utf-8") as file:
            output.append(file.read())
    return output


# print(fetch_data()) # КАПЧА ВЫПАДАЕТ
pages = get_pages()

tags_freq = {}  # Словарь ЖАНР:КОЛИЧЕСТВО
for page in pages:  # Перебираем 5 страниц снятых с кинопоиска
    soup = BeautifulSoup(page, "html.parser")  # Парсим в супе
    films = soup.find_all("div", class_="desktop-rating-selection-film-item")  # Собираем сериалы в кучу
    for film in films:  # Перебираем их
        film_meta = film.find_all("span", class_="selection-film-item-meta__meta-additional-item")[1]  # Получаем жанры
        tags = film_meta.text.split(", ")  # Перегоняем строку в список жанров
        for tag in tags:  # Раскидываем теги в словарь
            if tag in tags_freq:  # Если тег есть в словаре то...
                tags_freq[tag] += 1  # Прибавляем еденичку
            else:
                tags_freq[tag] = 1  # Если нет то создаем тег и ставим значение 1


print(tags_freq)  # Выводим словарь чтобы сверить данные
plot.bar(list(tags_freq.keys()), tags_freq.values(), color='g')  # Загоняем в гистограмму
plot.xticks(rotation='vertical')  # Повернул подписи иби невлезет
plot.title("Статистика жанров")  # Заголовок как в примере
for i, v in enumerate(tags_freq.values()):  # Делаем подписи над столбцами
    plot.text(i-0.4, v+1, str(v))
plot.subplots_adjust(bottom=0.3)  # Не влезли подписи, чуть растянем график
plot.savefig("plot.png")  # Сохраняем гистограмму в картинку чтобы в окне вывести

# Вывожу на экран в окошке для удобства
image = tkinter.PhotoImage(file="plot.png")
canvas.create_image(0, 0, anchor="nw", image=image)
canvas.grid()
root.mainloop()
