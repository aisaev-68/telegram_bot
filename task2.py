# from requests import get
# from telebot import TeleBot, types
# from locales import commands_bot

TELEGRAM_API_TOKEN="2065095548:AAGf5ET1auIgoGUw6uv60lciPwz08w9I7R8"
bot = TeleBot(TELEGRAM_API_TOKEN)

user = {}




@bot.message_handler(commands=["start"])
def comands_message(message):
    lng = "en_US"
    my_commands = [types.BotCommand("start", commands_bot[lng]["start"])]
        #[types.BotCommand("start", commands_bot[lng]["start"])]
                   # types.BotCommand("lowprice", commands_bot[lng]["lowprice"]),
                   # types.BotCommand("highprice", commands_bot[lng]["highprice"]),
                   # types.BotCommand("bestdeal", commands_bot[lng]["bestdeal"]),
                   # types.BotCommand("history", commands_bot[lng]["history"]),
                   # types.BotCommand("help", commands_bot[lng]["help"])]

    bot.set_my_commands(my_commands)

def next_hotel_show(call, get_hotel):
    #get_hotel = user[call.message.chat.id].hotel_forward()
    photo = user[call.message.chat.id].photo_forward()
    bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=user[call.message.chat.id].mes_id_photo,
                               media=types.InputMediaPhoto(get(photo).content))


    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=user[call.message.chat.id].mes_id_hotel,
                          text=get_hotel, parse_mode='MARKDOWN',
                          disable_web_page_preview=True,
                          reply_markup=InlKbShow().get_show_kbd())

def photo_show(call, photo):
    bot.edit_message_media(chat_id=call.message.chat.id,
                           message_id=user[call.message.chat.id].mes_id_photo,
                           media=types.InputMediaPhoto(get(photo).content))

@bot.callback_query_handler(func=lambda call: True)
def inline(call):

    if call.data == "hotel_forward":
        get_hotel1 = user[call.message.chat.id].hotel_forward()
        if get_hotel1:
            next_hotel_show(call, get_hotel1)
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Последняя гостиница')

    elif call.data == "hotel_backward":
        get_hotel2 = user[call.message.chat.id].hotel_backward()
        if get_hotel2:
            next_hotel_show(call, get_hotel2)
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Первая гостиница')

    elif call.data == "photo_backward":  # фото назад
        photo = user[call.message.chat.id].photo_backward()
        if photo:
            bot.answer_callback_query(callback_query_id=call.id)
            photo_show(call, photo)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Первое фото')

    elif call.data == "photo_forward":
        get_hotel1 = user[call.message.chat.id].hotel_forward()
        if get_hotel1:
            next_hotel_show(call, get_hotel1)
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Последняя гостиница')




if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

