import telebot
from telebot import types
from Base import *

bot = telebot.TeleBot('6429025280:AAH5T7SioE4e6OYasOypVEznu_rhE_c2IWY')
USERS = User_Database()
MESSAGE = Message_Database()
email = ""
INFO=list()
password = ""
username = ""
@bot.message_handler(command=['start'])
@bot.message_handler(command=['SEND'])
@bot.message_handler(command=['IncomingMessages'])
@bot.message_handler(command=['OutcomingMessages'])
@bot.message_handler(command=['Exit'])
@bot.message_handler(command=['Регистрация'])
@bot.message_handler(command=['Вход'])
def start(message):
    if message.text == "/start":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Войти")
        btn2 = types.KeyboardButton("Зарегистрироваться")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Привет, {0.first_name}! Добро пожаловать в почту! Выбери варианты: /SignUp - Регистрация или /SignIn - Войти".format(message.from_user), reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, "Для начала работы нажмите /start")

@bot.message_handler(content_types=['text'])
def registration(message):
    global INFO
    global username
    username = "{0.first_name}".format(message.from_user)
    if message.text == "Войти" or message.text == "/SignIn":
        message.text = ""
        bot.send_message(message.from_user.id, 'Введите ваш электронный адрес:')
        bot.register_next_step_handler(message, get_email)
    elif message.text == "Зарегистрироваться" or message.text == "/SignUp":
        bot.send_message(message.from_user.id,'Придумайте электронную почту:')
        bot.register_next_step_handler(message,reg_email)
def get_email(message):
    global INFO
    global email
    email = message.text
    INFO = USERS.user
    print(INFO, USERS.find_email(email), USERS.user)
    if (email != "") and (USERS.find_email(email)):
        message.text = ""
        INFO = USERS.User()
        print(INFO,USERS.find_email(email))
        bot.send_message(message.from_user.id, 'Введите пароль:')
        bot.register_next_step_handler(message, get_password)
    else:
        bot.send_message(message.from_user.id, 'Данного email не существует, попробуйте заново.')
        message.text = "/start"
        start(message)

def get_password(message):
    global INFO
    if (message.text != "") and (message.text == INFO[5]):
        bot.send_message(message.from_user.id, 'Добро пожаловать!')
        bot.send_message(message.from_user.id, '/SEND - написать письмо')
        bot.send_message(message.from_user.id, '/IncomingMessages - входящие сообщения')
        bot.send_message(message.from_user.id, '/OutcomingMessages - исходящие сообщения')
        bot.send_message(message.from_user.id, '/Exit - Выйти из аккаунта')
        bot.register_next_step_handler(message, MAIL)
    else:
        bot.send_message(message.from_user.id, 'Неверный пароль, попробуйте заново.')
        message.text = "/start"
        start(message)
def reg_email(message):
    global username
    global email
    global password
    email = message.text
    if (email != "") and (not(USERS.find_email(email))):
        bot.send_message(message.from_user.id, 'Придумайте пароль для почты:')
        bot.register_next_step_handler(message, reg_password)
    else:
        bot.send_message(message.from_user.id, 'Эта почта уже занята, попробуйте придумать другую почту:')
        bot.register_next_step_handler(message, reg_email)
def reg_password(message):
    global username
    global email
    global password
    global INFO
    if (message.text != ""):
        password = message.text
        USERS.add_users(username, email, password)
        USERS.output_from_sql()
        INFO = USERS.users[len(USERS.users)-1]
        print(INFO, USERS.users)
        bot.send_message(message.from_user.id, 'Добро пожаловать!')
        bot.send_message(message.from_user.id, '/SEND - написать письмо')
        bot.send_message(message.from_user.id, '/IncomingMessages - входящие сообщения')
        bot.send_message(message.from_user.id, '/OutcomingMessages - исходящие сообщения')
        bot.send_message(message.from_user.id, '/Exit - Выйти из аккаунта')
        bot.register_next_step_handler(message, MAIL)

reciever = ""
text = ""

def MAIL(message):
    global INFO

    if message.text == '/SEND':
        bot.send_message(message.from_user.id, 'Укажите электронную почту аккаунта, куда хотите отправить')
        bot.register_next_step_handler(message, get_reciever_email)
    elif message.text == '/IncomingMessages':
        bot.send_message(message.from_user.id, 'Входящие сообщения:')
        USERS.recieved_message_func(email)
        reciever_text = (' \n').join(USERS.recieved_mess)
        bot.send_message(message.chat.id, reciever_text)
        bot.send_message(message.from_user.id, 'Добро пожаловать! Выбери действие')
        bot.send_message(message.from_user.id, '/SEND - написать письмо')
        bot.send_message(message.from_user.id, '/IncomingMessages - входящие сообщения')
        bot.send_message(message.from_user.id, '/OutcomingMessages - исходящие сообщения')
        bot.send_message(message.from_user.id, '/Exit - Выйти из аккаунта')
        bot.register_next_step_handler(message, MAIL)
    elif message.text == '/OutcomingMessages':
        bot.send_message(message.from_user.id, 'Исходящие сообщения:')
        USERS.sent_message_func(email)
        sent_text = ' \n'+(' \n').join(USERS.sent_mess)
        bot.send_message(message.chat.id, sent_text)
        bot.send_message(message.from_user.id, 'Добро пожаловать! Выбери действие')
        bot.send_message(message.from_user.id, '/SEND - написать письмо')
        bot.send_message(message.from_user.id, '/IncomingMessages - входящие сообщения')
        bot.send_message(message.from_user.id, '/OutcomingMessages - исходящие сообщения')
        bot.send_message(message.from_user.id, '/Exit - Выйти из аккаунта')
        bot.register_next_step_handler(message, MAIL)
    elif message.text == "/Exit":
        bot.send_message(message.from_user.id, "Для начала работы нажмите /start")
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.from_user.id, 'Некорректная запись')
        bot.send_message(message.from_user.id, 'Добро пожаловать! Выбери действие')
        bot.send_message(message.from_user.id, '/SEND - написать письмо')
        bot.send_message(message.from_user.id, '/IncomingMessages - входящие сообщения')
        bot.send_message(message.from_user.id, '/OutcomingMessages - исходящие сообщения')
        bot.send_message(message.from_user.id, '/Exit - Выйти из аккаунта')
        bot.register_next_step_handler(message, MAIL)
def get_reciever_email(message):
    global reciever
    reciever = message.text
    if USERS.find_email(reciever):
        bot.send_message(message.chat.id, 'Напишите Ваше письмо')
        bot.register_next_step_handler(message, write_text)
    else:
        bot.send_message(message.from_user.id, 'Такого email нет')
        bot.send_message(message.from_user.id, 'Добро пожаловать! Выбери действие')
        bot.send_message(message.from_user.id, '/SEND - написать письмо')
        bot.send_message(message.from_user.id, '/IncomingMessages - входящие сообщения')
        bot.send_message(message.from_user.id, '/OutcomingMessages - исходящие сообщения')
        bot.send_message(message.from_user.id, '/Exit - Выйти из аккаунта')
def write_text(message):
    global text
    text=message.text
    MESSAGE.add_message(email, reciever, "Письмо", text)
    MESSAGE.output_from_sql_message()
    #print(MESSAGE.messages)
    USERS.push_sent_message(email, text)
    USERS.push_received_message(reciever, text)
    USERS.output_from_sql()
    #print(USERS.users)
    bot.send_message(message.chat.id, 'Письмо отправлено')
    bot.send_message(message.from_user.id, 'Добро пожаловать! Выбери действие')
    bot.send_message(message.from_user.id, '/SEND - написать письмо')
    bot.send_message(message.from_user.id, '/IncomingMessages - входящие сообщения')
    bot.send_message(message.from_user.id, '/OutcomingMessages - исходящие сообщения')
    bot.send_message(message.from_user.id, '/Exit - Выйти из аккаунта')
    bot.register_next_step_handler(message, MAIL)
bot.polling(none_stop=True)
