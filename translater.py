from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import os, os.path
import find_get_image


class Translate:
    def __init__(self, browser):
        self.browser = browser
        with open('words.txt', 'r', encoding='utf-8') as words:
            self.word_list = list(filter(lambda a: len(a) > 0, words.read().split('\n')))
            print(f"Переводим следующие слова: {self.word_list}")

        self.link = "https://translate.google.ru/?hl=ru&tab=wT&sl=ru&tl=en&op=translate"
        self.path = f'Results/translate.txt'
        if os.path.isfile(self.path): os.remove(self.path)
        self.translate()


    # Переводим слово на английский язык
    def translate(self):
        for word in self.word_list:
            self.browser.get(self.link)
            self.word = word
            input_field = self.browser.find_element('xpath', "//textarea[@aria-label='Исходный текст']")
            input_field.send_keys(self.word)
            input_field.send_keys(Keys.ENTER)  # Эмулируем нажатие клавиши Enter - импорт модуля Keys
            output_field = self.browser.find_element('xpath', "//span[@lang='en']/span/span[text()]")
            self.translated = output_field.text
            print(f"Слово {self.word} переведено в {self.translated}")
            input_field.send_keys(Keys.CONTROL + Keys.SHIFT + 's')
            time.sleep(3)
            self.url = self.browser.current_url
            print(f"Адрес перевода слова: {self.url}")
            self.transcription = self.browser.find_element('xpath', "//h2[text()='Исходный текст']/../child::div[2]/div[text()][1]").text
            print(f"Транскрипция: {self.transcription}")
            self.save_to_file()

    # сохраняем слово, его перевод, транскрипцию и ссылку на перевод
    def save_to_file(self):
        with open(f'Results/translate.txt', 'a', encoding='utf-8') as file:
            file.write(f"{self.word},{self.translated},{self.transcription},{self.url}\n")
            print(f"Данные: {self.word}, {self.translated}, {self.transcription} и url - записаны в translate.txt!")



def main():
    # Создаём объект браузера с настройками
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(6)
    translate = Translate(browser)


if __name__ == "__main__":
    main()