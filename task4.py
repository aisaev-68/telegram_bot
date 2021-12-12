import re

from telebot.async_telebot import AsyncTeleBot


bot = AsyncTeleBot("2065095548:AAGf5ET1auIgoGUw6uv60lciPwz08w9I7R8")


class MyStates:
    name = 1
    surname = 2
    age = 3



# SimpleCustomFilter is for boolean values, such as is_admin=True
class IsValid(asyncio_filters.SimpleCustomFilter):
    key = 'is_check_city'
    @staticmethod
    async def check(message: types.Message):
        if len(re.findall(r'^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', message.text)) > 0:
            return  True



@bot.message_handler(commands=['start'])
async def start_ex(message):
    """
    Start command. Here we are starting state
    """
    await bot.set_state(message.from_user.id, MyStates.name)
    await bot.send_message(message.chat.id, 'Hi, write me a name')


@bot.message_handler(state="*", commands='cancel')
async def any_state(message):
    """
    Cancel state
    """
    await bot.send_message(message.chat.id, "Your state was cancelled.")
    await bot.delete_state(message.from_user.id)

@bot.message_handler(state=MyStates.name, is_check_city=False)
async def check(mess):
    """
        Функция проверки на корректность ввода названия города. re.findall(r'^[а-яА-ЯёЁa-zA-Z-\s]+$', txt)
    """
    await bot.set_state(mess.from_user.id, MyStates.name)
    await bot.send_message(chat_id=mess.from_user.id,
                                   text='Hi, write me a name')


@bot.message_handler(state=MyStates.name, is_check_city=True)
async def name_get(message):
    """
    State 1. Will process when user's state is 1.
    """
    await bot.send_message(message.chat.id, f'Now write me a surname')
    await bot.set_state(message.from_user.id, MyStates.surname)
    async with bot.retrieve_data(message.from_user.id) as data:
        data['name'] = message.text


@bot.message_handler(state=MyStates.surname)
async def ask_age(message):
    """
    State 2. Will process when user's state is 2.
    """
    await bot.send_message(message.chat.id, "What is your age?")
    await bot.set_state(message.from_user.id, MyStates.age)
    async with bot.retrieve_data(message.from_user.id) as data:
        data['surname'] = message.text


# result
@bot.message_handler(state=MyStates.age, is_digit=True)
async def ready_for_answer(message):
    async with bot.retrieve_data(message.from_user.id) as data:
        await bot.send_message(message.chat.id,
                               "Ready, take a look:\n<b>Name: {name}\nSurname: {surname}\nAge: {age}</b>".format(
                                   name=data['name'], surname=data['surname'], age=message.text), parse_mode="html")
    await bot.delete_state(message.from_user.id)


# incorrect number
@bot.message_handler(state=MyStates.age, is_digit=False)
async def age_incorrect(message):
    await bot.send_message(message.chat.id,
                           'Looks like you are submitting a string in the field age. Please enter a number')


# register filters


bot.add_custom_filter(IsValid())
# set saving states into file.
bot.enable_saving_states()  # you can delete this if you do not need to save states
import asyncio
asyncio.run(bot.polling())