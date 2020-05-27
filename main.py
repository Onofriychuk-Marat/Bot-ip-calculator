#!/usr/bin/env python3.7

# Импортирую библиотеку калькулятора и api telegram
from calculate import *
import telebot
from telebot import types
from telebot.types import Message

TOKEN = '1177511437:AAHjEIXWqHxcSclzbyzYZVFDbDArOCz5g8Q'
textUser = ''

bot = telebot.TeleBot(TOKEN)

# Функция следит за тем что написал пользователь, после возвращает текст прочитанного
def get_text(message, text): 
	global textUser
	bot.send_message(message.from_user.id, text)
	bot.register_next_step_handler(message, handler_text)
	while True:
		if textUser != '':
			return textUser

# Функция следит за нажатием на кнопку, после возвращает индекс нажатой кнопки
def get_click(message: Message, cort, text):
	global textUser
	keyboard = types.InlineKeyboardMarkup()
	for i in range(len(cort)):
			keyboard.add(types.InlineKeyboardButton(text=cort[i], callback_data=cort[i]))
	bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)
	while True:
		if textUser != '':
			for i in range(len(cort)):
				if cort[i] == textUser:
					textUser = ''
					return i

# Слушатель сообщений от пользователя
def handler_text(message):
	global textUser 
	textUser = message.text

# Слушатель нажатий по кнопкам от пользователя
@bot.callback_query_handler(func=lambda call: True)
def handler_click(call):
	global textUser 
	textUser = call.data

# Получаем все лист со всеми масками подсети
def get_subnet(message: Message, masks: list) -> int:
	option_mask = get_list_subnet(masks)
	return get_click(message, option_mask, 'Выбери маску подсети:')

# Здесь мы проверяем ip на валидность. Если тест на валидность функция не прошла, функция завершается.
# Также определяем в каком формате получен адрес, зависимости от варианта получаем маску подсети тем или иным способом
# Полученный ip и маску подсети кидаем в функцию get_answer, и получаем итоговый результат
def menu(message: Message):
	global textUser
	option = 0
	ip = get_text(message, 'Введите ip адрес:')
	ip = ip.split('/')
	option = is_ip(ip)
	if is_ip(ip) > 0:
		masks = [['1' if k < i else '0' for k in range(0, 32)] for i in range(0, 33)]
		masks = [''.join(x) for x in masks]
		if option == 1:
			masks = masks[get_subnet(message, masks)]
		else:
			masks = masks[int(ip[1])]
		ip = get_ip(ip[0])
		answer = get_answer(ip, masks)
		bot.send_message(message.from_user.id, answer)
	textUser = ''

# Функция старта работы бота
@bot.message_handler(commands=['start'])
def start(message: Message):
	bot.send_message(message.from_user.id, 'Привет!\nЯ бот калькулятор ip адресов.\n' + \
											'Введите ip адрес в формате 198.168.0.1/24,\n' + \
											'либо 198.168.0.1')
	while True:
		menu(message)

# Функция стоп работы бота
@bot.message_handler(commands=['stop'])
def stop(message: Message):
	bot.send_message(message.from_user.id, 'До следующих подчетов!')
	bot.stop_bot()

# запускаем наш api
bot.polling()