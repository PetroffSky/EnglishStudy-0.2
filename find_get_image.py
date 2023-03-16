from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import shutil
import os, os.path


class Find_Get:
    def __init__(self):
        self.unavailable_hosts = []
        with open('words.txt', 'r', encoding='utf-8') as words:
            self.word_list = list(filter(lambda a: len(a) > 0, words.read().split('\n')))
            print(f"Готовим изображения для следующих слов: {self.word_list}")

        self.link = 'https://yandex.ru/images/search'
        self.get_browser()


    # Создаём объект браузера с настройками
    def get_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")  # запуск в режиме инкогнито
        options.add_argument("start-maximized")  # запуск в развёрнутым экраном
        options.add_argument("user-agent=Mozilla/5.0 "
                             "(Windows NT 6.3; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36")

        # отключаем надпись об автоматизированном программном обеспечении
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Открываем браузер
        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(10)
        self.browser.get(self.link)
        self.set_settings()


    def set_settings(self):
        print("Настраиваем поиск")
        try:
            pic_size = self.browser.find_elements('xpath', "//button[contains(@class, 'Button2_size_m')]")[0]
            pic_size.click()
            input_size_w = self.browser.find_element('xpath', "//input[@placeholder='1366']")
            input_size_w.click()
            input_size_w.send_keys('400')
            input_size_h = self.browser.find_element('xpath', "//input[@placeholder='768']")
            input_size_h.click()
            input_size_h.send_keys('400')
            input_size_h.send_keys(Keys.ENTER)

        except NoSuchElementException as NSEE:
            print(f"Ошибка настройки поиска: {NSEE}")
            print("Повтор!")
            self.set_settings()

        print("Поиск изображений настроен")
        self.image_finder()
        print("Все изображения загружены!")


    # Ищем изображение по слову из списка и получаем ссылку на jpg
    def image_finder(self):
        try:
            for word in self.word_list:
                self.word = word
                if os.path.isfile(f"Results/Images/{self.word}.jpg"):
                    print(f"Такое изображение для слова: {self.word} есть. Выбираем другое слово.")
                    continue
                # Вводим слово в поле поиска изображения

                input_field = self.browser.find_element('xpath', "//input[@name='text']")
                input_field.click()
                input_field.send_keys(f"рисунок {self.word}")
                input_field.send_keys(Keys.ENTER)

                result = False
                counter = 0
                print(f"\nПолучаем ссылку на изображение слова {self.word}!")
                while not result:
                    # Нажимаем на картинки в поисковых результатах до получения результата
                    time.sleep(2)
                    img_clck = self.browser.find_elements('xpath', "//div[@class='serp-item__meta']")[counter]
                    img_clck.click()
                    counter += 1

                    # Открываем картинку во второй вкладке
                    open_image = self.browser.find_element('xpath', "//span[contains(text(), 'Открыть')]/..")
                    open_image.click()

                    time.sleep(1)
                    if len(self.browser.window_handles) == 2:
                        # Переключаемся на открытую вкладку и получаем URI файла
                        self.browser.switch_to.window(self.browser.window_handles[1])
                        self.url = self.browser.current_url
                        # print(self.url)
                    elif len(self.browser.window_handles) == 1:
                        print("Видимо изображение скачалось браузером. Качаем другое изображение!")
                        self.browser.back()
                        continue

                    # проверяем, что ссылка является URI на jpeg файл
                    if self.url.endswith('.jpg'):
                        result = self.checking_file()
                    else:
                        result = False

                    # Закрываем открытую вкладку и переключаемся на 1-ю вкладку
                    self.browser.close()
                    self.browser.switch_to.window(self.browser.window_handles[0])
                    self.browser.back()

                # Очищаем поле ввода
                input_field.clear()
                time.sleep(2)

        except NoSuchElementException as NSEE:
            print(f"Ошибка, элемент не найден: {NSEE}. Производим перезапуск")
            self.browser.close()
            self.get_browser()
        except ElementClickInterceptedException as ECIE:
            print(f"Ошибка, перехвачен щелчок по элементу: {ECIE}. Производим перезапуск")
            self.browser.close()
            self.get_browser()
        except Exception as ex:
            print(f"Ошибка следующего типа: {ex}. Производим перезапуск")
            self.browser.close()
            self.get_browser()


    def checking_file(self):
        print(f"Проверяем доступность файла {self.word} для скачивания.")
        if not self.url.endswith('.jpg'):
            return False
        elif self.image_downloader():
            shutil.copy2('image.jpg', f"Results\\Images\\{self.word}.jpg")
            print("Проверяем тип файла!")
            bin_file = "check_file.bin"
            os.rename("image.jpg", bin_file)
            with open(bin_file, 'rb') as file:
                bin_text = str(file.read())[:30]
                print(bin_text)  # Ожидаем b'\xff\xd8\xff\xe0\x00\x10JFIF'

            if os.path.isfile(bin_file): os.remove(bin_file)

            # Проверка соответствия типа файла его содержимому (для python-docx)
            if bin_text.endswith('JFIF'):
                print(f"Формат файла ({self.word}) соответствует JPEG! Файл сохранён!")
                return True
            else:
                print(f"Формат текущего файла ({self.word}) не соответствует JPEG! Ищем JPEG!")
                return False
        else:
            return False


    # Скачиваем изображение и сохраняем его в файл
    def image_downloader(self):
        # Определение URL хостинга
        print(f"Текущий URI: {self.url}")
        result_url = ''
        counter = 0
        for letter in self.url:
            if letter == '/':
                counter += 1
            elif counter == 3:
                break
            result_url += letter
        print(f"Текущий URL: {result_url}")

        # Фильтруем "плохие" хосты
        if result_url in self.unavailable_hosts:
            print("Текущий URL в чёрном списке. Закачка отменена. Меняю изображение.")
            return False
        else:
            try:
                # Используем библиотеку requests и UserAgent для обхода блокировки скачки файлов
                request_file = requests.get(url=self.url,
                                            stream=True,
                                            headers={'User-agent': 'Mozilla/5.0'})

                if request_file.status_code == 200:       # сохраняем, если хост хороший
                    print(f"Файл изображения {self.word} для загрузки доступен!")
                    self.image = open("image.jpg", "wb")    # открываем файл для записи в режиме wb
                    self.image.write(request_file.content)  # записываем содержимое в файл
                    self.image.close()
                    print(f"Загрузка изображения {self.word} выполнена")
                    return True
                else:
                    raise ValueError("Сброс закачки сервером")
            except Exception as ex:
                print(f'Ошибка загрузки изображения! Причина: {ex}')
                if result_url not in self.unavailable_hosts:
                    self.unavailable_hosts.append(result_url)
                    print(f"Текущий хост добавлен в чёрный список: {result_url}")
                else:
                    print("Такой хост уже есть в чёрном списке.")
                print(*self.unavailable_hosts)
                return False



if __name__ == "__main__":
    Find_Get()
