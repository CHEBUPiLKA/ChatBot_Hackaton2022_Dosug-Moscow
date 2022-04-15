import telebot
from functions import *
from telebot import types
import time
import parse

bot = telebot.TeleBot('5364274045:AAHrII0xb9pqxCq2RA6_y-qGHEjzhQP5PuU')

event_types = ['Любые', 'Встречи', 'Выставки', 'Кино', 'Концерты', 'Обучение', 'Праздники', 'Прочее', 'Спектакли', 'Фестивали и праздники', 'Экскурсии']
filters = []
keys = form_markup([types.InlineKeyboardButton("Подробнее", callback_data=f'more'), types.InlineKeyboardButton("Далее", callback_data=f'next')])
buttons = form_buttons(event_types)
address = ""
index = 0
priceRange = ""
date = ""
busy = False
cl_dict = {}
msg = None
PushkinCard = False
continueFlag = False
def getAddress(message):
	global continueFlag
	global address
	address = message.text
	markup = form_InlineKeyboard(event_types)
	bot.send_message(message.chat.id, "Отлично! Теперь давайте определимся с типом мероприятий. Пожалуйста, выберите все типы мероприятий, которые хотели бы посетить и напишите \"Продолжить\"", reply_markup=markup)
	continueFlag = True
def getPrice(message):
	global priceRange
	priceRange = message.text
	bot.send_message(message.chat.id, "Хорошо! Стоит ли мне искать только мероприятия, которые можно посетить по пушкинской карте?", reply_markup=form_markup([types.InlineKeyboardButton("Да", callback_data=f'YES'), types.InlineKeyboardButton("Нет", callback_data=f'NO')]))
def getDate(message):
	global date
	global address
	global buttons
	global priceRange
	global PushkinCard
	global continueFlag
	global msg
	global filters
	global cl_dict
	global busy
	cl = []
	date = message.text
	bot.send_message(message.chat.id, "Ваш запрос принят, пожалуйста ожидайте...")
	for i in filters:
		link = parse.PreparationLink(PushkinCard, priceRange, i, date)
		cl = cl + parse.GetObjects(link)
	filters = []
	buttons = form_buttons(event_types)
	address = ""
	priceRange = ""
	date = ""
	busy = False
	PushkinCard = False
	continueFlag = False
	cl_dict.update({message.chat.id: (cl, 1, 0)})
	msg = bot.send_photo(message.chat.id, cl[0].picture, cl[0].name, reply_markup=keys)
@bot.message_handler(commands=['start'])
def send_welcome(message):
	global busy
	if busy:
		bot.send_message(message.chat.id,
						 "Простите, я сейчас занят, прошу вас немного подождать и я обязательно вам отвечу")
	while busy:
		continue
	bot.send_message(message.chat.id,
					 "Здравствуйте! Я помогу вам найти подходящее мероприятие! Для начала введите адрес, рядом с которым мне стоит искать мероприятия")
	busy = True
	bot.register_next_step_handler(message, getAddress)
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
	global filters
	global buttons
	global PushkinCard
	global locationMsgId
	global cl_dict
	if str(call.data).split("_")[0] == "EVENTSCALLBACK":
		filters.append(str(call.data).split("_")[1])
		buttons[event_types.index(str(call.data).split("_")[1])] = types.InlineKeyboardButton(str(call.data).split("_")[1] + " [+]", callback_data=f'CHECKEDEVENTSCALLBACK_{str(call.data).split("_")[1]}')
		bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=form_markup(buttons))
	elif str(call.data).split("_")[0] == "CHECKEDEVENTSCALLBACK":
		filters.pop(filters.index(str(call.data).split("_")[1]))
		buttons[event_types.index(str(call.data).split("_")[1])] = types.InlineKeyboardButton(str(call.data).split("_")[1], callback_data=f'EVENTSCALLBACK_{str(call.data).split("_")[1]}')
		bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=form_markup(buttons))
	elif str(call.data) == "YES":
		PushkinCard = True
		bot.send_message(call.message.chat.id, "И последний шаг! Напишите дату в которую Вы планируете постетить мероприятие в формате ГГГГ-ММ-ДД и я начну поиск мероприятий для Вас!")
		bot.register_next_step_handler(call.message, getDate)
	elif str(call.data) == "NO":
		PushkinCard = False
		bot.send_message(call.message.chat.id, "И последний шаг! Напишите дату в которую Вы планируете постетить мероприятие в формате ГГГГ-ММ-ДД и я начну поиск мероприятий для Вас!")
		bot.register_next_step_handler(call.message, getDate)
	elif str(call.data) == "next":
		#global index
		if cl_dict[call.message.chat.id][2] != 0:
			bot.delete_message(call.message.chat.id, cl_dict[call.message.chat.id][2])
			cl_dict[call.message.chat.id] = (cl_dict[call.message.chat.id][0], cl_dict[call.message.chat.id][1], 0)
		cl_dict[call.message.chat.id] = (cl_dict[call.message.chat.id][0], cl_dict[call.message.chat.id][1] + 1, cl_dict[call.message.chat.id][2])
		bot.edit_message_media(media=types.InputMediaPhoto(cl_dict[call.message.chat.id][0][cl_dict[call.message.chat.id][1]].picture, cl_dict[call.message.chat.id][0][cl_dict[call.message.chat.id][1]].name), chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keys)
	elif str(call.data) == "more":
		keys2 = form_markup([types.InlineKeyboardButton("Ссылка на мероприятие", callback_data=None, url=cl_dict[call.message.chat.id][0][cl_dict[call.message.chat.id][1]].link),
							 types.InlineKeyboardButton("Далее", callback_data='next'), types.InlineKeyboardButton("Получить адрес", callback_data='address')])
		bot.edit_message_media(media=types.InputMediaPhoto(cl_dict[call.message.chat.id][0][cl_dict[call.message.chat.id][1]].picture, f"Название: {cl_dict[call.message.chat.id][0][cl_dict[call.message.chat.id][1]].name}\nЦена: {cl_dict[call.message.chat.id][0][cl_dict[call.message.chat.id][1]].price}\n"), chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=keys2)
	elif str(call.data) == "address":
		latitude = cl_dict[call.message.chat.id][0][cl_dict[call.message.chat.id][1]].coords['Point']['pos'].split(' ')[1]
		longitude = cl_dict[call.message.chat.id][0][cl_dict[call.message.chat.id][1]].coords['Point']['pos'].split(' ')[0]
		mess = bot.send_location(call.message.chat.id, latitude, longitude)
		cl_dict[call.message.chat.id] = (cl_dict[call.message.chat.id][0], cl_dict[call.message.chat.id][1], mess.id)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	global continueFlag
	if message.text.lower() == "продолжить":
		if continueFlag:
			bot.send_message(message.chat.id, "Прекрасно! Теперь пришлите желаемый ценовой диапозон в формате мин.цена-макс.цена или -1 если цена неограничена")
			continueFlag = False
			bot.register_next_step_handler(message, getPrice)
		else:
			pass
bot.infinity_polling()