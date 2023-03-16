import qrcode
import os, os.path


class Generate_QR:
    def __init__(self):
        with open('Results/translate.txt', 'r', encoding='utf-8') as translate:
            self.url_list = []
            for stroke in translate.read().split('\n'):
                if len(stroke) > 0:
                    word, translate, transcription, url = stroke.split(',')
                    self.url_list.append(str(url).strip())
        print(*self.url_list, sep='\n')
        with open('words.txt', 'r', encoding='utf-8') as words:
            self.word_list = list(filter(lambda a: len(a) > 0, words.read().split('\n')))
        print(f"Переводим следующие слова: {self.word_list}")

        self.generator()


    def generator(self):
        for word, url in zip(self.word_list, self.url_list):
            self.path = f'Results/Images/QR_{word}.png'
            if os.path.isfile(self.path): os.remove(self.path)
            print("Генерируем QR-code")
            print(word, url)
            qr_code = qrcode.make(url)
            type(qr_code)
            qr_code.save(self.path)

        return "QR-codes is Done"


if __name__ == "__main__":
    Generate_QR()