import requests

URL = "https://translate.yandex.net/api/v1.5/tr.json/translate"  #это адрес для обращения к API
KEY = "trnsl.1.1.20190115T093726Z.65e1460d8d95bd06.р45ор345о3р4о53р45о345р3о" #Это ваш API ключ

def translate_me(mytext):

    params = {
        "key": KEY,
        "text": mytext,
        "lang": 'ru-en'  #Здесь мы указываем с какого языка на какой мы делаем переводим
    }
    response = requests.get(URL ,params=params)
    return response.json()

json = translate_me("Привет мой друг") #Сюда мы вводим текст который нам нужно перевести (для удобности можно вынести в отдельную переменную
print(json)