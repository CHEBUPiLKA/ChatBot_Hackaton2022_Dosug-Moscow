def write_log(err):
    from datetime import datetime as dt
    ###################################
    with open('log_telegram.txt', 'a') as f:
        f.write(str(dt.now(tz=None)) + ": " + str(err) + "\n")
    print(err)

def form_ReplyKeyboard(names):
    from telebot import types
    #########################
    keyboard = types.ReplyKeyboardMarkup(True)
    for i in names:
        button = types.KeyboardButton(i)
        keyboard.row(button)
    return keyboard
def form_InlineKeyboard(names):
    from telebot import types
    #########################
    keyboard = types.InlineKeyboardMarkup()
    for i in names:
        button = types.InlineKeyboardButton(i, callback_data=f'EVENTSCALLBACK_{i}')
        keyboard.row(button)
    return keyboard
def form_buttons(names):
    from telebot import types
    #########################
    buttons = []
    for i in names:
        buttons.append(types.InlineKeyboardButton(i, callback_data=f'EVENTSCALLBACK_{i}'))
    return buttons
def form_markup(buttons):
    from telebot import types
    #########################
    keyboard = types.InlineKeyboardMarkup()
    for i in buttons:
        keyboard.row(i)
    return keyboard