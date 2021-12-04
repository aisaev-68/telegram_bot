# -*- coding: utf-8 -*-


from user import Users
from datetime import datetime
from botrequests.locales import info_help
from botrequests.handlers import next_step_city, user, bot, logging, config

def next_menu(call):
    bot.send_message(chat_id=call.message.chat.id,
                     text="ПОИСК ОТЕЛЕЙ",
                     message_id=user[call.message.chat.id].message_id_hotel,
                     reply_markup=user[call.message.chat.id].hotels_act.getIln_menu())

@bot.message_handler(commands=["start", "help", "lowprice", "highprice", "bestdeal", "history"])
def comands_message(message):
    print(message)

    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    if message.text.lower() == "/help":
        m = bot.send_message(chat_id=message.chat.id,
                         text=info_help,
                         reply_markup=user[message.chat.id].hotels_act.inln_menu)
        user[m.chat.id].message_id_photo = m.message_id

    elif message.text.lower() == '/start':
        start_help_text = f"Привет {user[message.from_user.id].getUsername()}, я БОТ по поиску отелей✅,\n" \
                              "И я готов подобрать для Вас отель 🏨"
        m = bot.send_message(chat_id=message.from_user.id,
                         text=start_help_text,
                         reply_markup=user[message.chat.id].hotels_act.inln_menu)
        user[m.chat.id].message_id_photo = m.message_id


    elif message.text.lower() == '/lowprice':
        user[message.chat.id].command = message.text
        msg = bot.send_message(message.from_user.id, 'В каком городе будем искать?')

        bot.register_next_step_handler(msg, next_step_city)

    elif message.text.lower() == '/history':
        history = user[message.from_user.id].history()
        if not history:
            history = 'Ваша история пуста'
        bot.send_message(message.from_user.id, (",").join(history), parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def inline(call):
    user[call.message.chat.id].clearCache()
    if call.data == '/start':
        pass


    elif call.data == '/history':
        history = user[call.message.from_user.id].history()[0]
        if not history:
            history = 'Ваша история пуста'
        bot.send_message(call.message.from_user.id, (",").join(history), parse_mode="Markdown")
    else:
        logging.info(call.message.chat.id, f'Команда {call.data} не обработана')




if __name__ == '__main__':
    while True:
        try:
            logging.error(f"{datetime.now()} - Бот запущен")
            bot.polling(none_stop=True, interval=0)
        except Exception as ex:
            logging.error(f"{datetime.now()} - {ex}")
