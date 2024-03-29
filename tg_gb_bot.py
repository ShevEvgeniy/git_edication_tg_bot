import telebot #Импортируем библиотеку telebot
from random import *
import json
import requests
films=[]
API_URL='https://7012.deeppavlov.ai/model' #указываем адрес для подключения библиотеки ИИ. Адрес строковой бибилиотеки.

def save(): #Сохраняем все в файле с выводод на просмотр "Наша фильмотека была успешно сохранена в файле films.json" если данного файла нет то с помощью "w" создаем его
    with open("films.json","w",encoding="utf-8") as fh:
        fh.write(json.dumps(films,ensure_ascii=False))
    print("Наша фильмотека была успешно сохранена в файле films.json")

def load():
    global films
    with open("films.json","r",encoding="utf-8") as fh:
        films=json.load(fh)
    print("Фильмотека была успешно загружена")   #Выводим на экран


API_TOKEN='5868864749:AAF_G_RbB9DJsLNrUGQrGZh2aFY_fWGjClU' #Получаем токен в телеграме и вводим в данную строку
bot = telebot.TeleBot(API_TOKEN) #Создаем экземпляр бота

@bot.message_handler(commands=['start']) #Стартуем и в массив добавляем строки Матрица, Солярис, Властелин колец, Техасская резня бензопилой, Санта Барбара
def start_message(message):
    try:
        load()
        bot.send_message(message.chat.id,"Фильмотека была успешно загружена!") #Бот посылает сообщение конкретному пользователю сhat.id

    except:
        films.append("Матрица")
        films.append("Солярис")
        films.append("Властелин колец")
        films.append("Техасская резня бензопилой")
        films.append("Санта Барбара") 
        bot.send_message(message.chat.id,"Фильмотека была загружена по умолчанию!") #Бот посылает сообщение, конкретному пользователю сhat.id


@bot.message_handler(commands=['all']) # С помощью данной команды выводим список всех фильмов в телеграме 
def show_all(message):
    bot.send_message(message.chat.id,"Вот список фильмов")
    bot.send_message(message.chat.id, ", ".join(films)) #Join склеит элементы списка используя запятую

@bot.message_handler(commands=['wiki']) # messange_handler служит для работы wiki. Пишем функцию wiki. C помощью /wiki <запрос> - получаем ответ ИИ
def wiki(message):
    quest = message.text.split()[1:] #В переменную quest включили то, что пишет пользователь после wiki
    qq=" ".join(quest)
    data = { 'question_raw': [qq]} #получаем строкове значение
    try:
        res = requests.post(API_URL,json=data,verify=False).json() #res результат запроса, методом post, API_URL - куда выполняется. Внутр будет лежать словрик который мы сформировали data, в формате json
        bot.send_message(message.chat.id, res) #Если что то нашлось бот нам отправит результат, а елси нет то выведет: Что ничего не нашлось
    except:
        bot.send_message(message.chat.id, "Что-то я ничего не нашел :-(") #Сначала анализируем команды и только потом текст. Это важно

bot.polling() #Запуск самого бота, здесь стартует замкнутый цикл while true