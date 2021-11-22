from botrequests.functions import bot, next_step_city, user
from botrequests.myclass import Users
from telebot import types



@bot.message_handler(content_types=["text"])
def comands_message(message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    if message.text.lower() in ["привет", "/hello-world", "help", "start"]:
        bot.send_message(message.from_user.id, "Привет! Я бот по поиску отелей. \nВыберите команду:.\n"
                                                         "/lowprice: поиск дешевых отелей.\n Или нажмите на кнопку ниже.")
        low_command = types.KeyboardButton('/lowprice')
        kbd = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kbd.row(low_command)

        bot.send_message(message.from_user.id, "Поиск отелей.", reply_markup=kbd)
    elif message.text.lower() in ['/lowprice']:
        user[message.chat.id].command = message.text
        msg = bot.send_message(message.from_user.id, 'В каком городе будем искать?')
        bot.register_next_step_handler(msg, next_step_city)


if __name__ == '__main__':
    bot.polling(none_stop=True)
