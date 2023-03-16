import time
import find_get_image
import translater
import gen_qrcode
import docx_save_print
import clean_temp_file
import os, os.path
import sys


def main():
    # Проверка наличия папок - при отсутствии их создаём
    results, images = 'Results', 'Images'
    if not os.path.exists(results):
        os.mkdir(results)
        os.mkdir(f"{results}/{images}")
        print("Все необходимые папки созданы")

    # Создаём объект webdriver и скачиваем изображения
    browser = find_get_image.Find_Get()

    # Создаём экземпляр класса Translate и переводим слова из списка
    translate = translater.Translate(browser.browser)
    browser.link = translate.link
    browser.browser.get(browser.link)

    # Закрываем объект webdriver
    browser.browser.close()


    # Делаем QR-code для ссылок каждого слова
    gen_qrcode.Generate_QR()

    # Сохраняем в документ Word в формате docx и открываем его
    docx_save_print.Save_Print()

    # Очищаем временные файлы
    # if os.path.isfile('image.jpg'): os.remove('image.jpg')
    # if os.path.isfile("Results/translate.txt"): os.remove("Results/translate.txt")
    # images_folder = r"Results/Images"
    # for file in os.listdir(images_folder):
    #     os.remove(os.path.join(images_folder, file))
    #     print(f"Файл {file} удалён!")
    # print("Все временные файлы удалены!")




if __name__ == "__main__":
    main()