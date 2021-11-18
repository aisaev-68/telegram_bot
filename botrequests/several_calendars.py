from telegram_bot_calendar import WMonthTelegramCalendar, DAY

data = {}
class MyStyleCalendar(WMonthTelegramCalendar):
    prev_button = "⬅️"
    next_button = "➡️"
    first_step = DAY


def gen_markup():
    calendar, step = MyStyleCalendar(calendar_id=1).build()
    return calendar


def start1(m):
    calendar, step = MyStyleCalendar(calendar_id=1).build()
    bot.send_message(m.chat.id,
                     "Выберите дату выезда",
                     reply_markup=calendar)


@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,
                     "Выберите дату въезда",
                     reply_markup=gen_markup())


@bot.callback_query_handler(func=MyStyleCalendar.func(calendar_id=1))
def cal1(c):
    # calendar_id is used here too, since the new keyboard is made
    result, key, step = MyStyleCalendar(calendar_id=1).process(c.data)
    print(type(result))
    if result:
        bot.edit_message_text(f"Выбрана дата {result}",
                              c.message.chat.id,
                              c.message.message_id)
        if not data.get('in_date'):
            data['in_date'] = result.isoformat()
            bot.callback_query_handler(start1(c.message), reply_markup=gen_markup())
        else:
            data['out_date'] = result.isoformat()
            print(data)
