from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.types import BotCommand

from config import *
from database import DataBase

bot = TeleBot(TOKEN, state_storage=StateMemoryStorage())


bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.set_my_commands(commands=[
    BotCommand('start', "Botni qayta ishga tushirish"),
    BotCommand('help', "Tez aloqa"),

])


db = DataBase(dbname=DB_NAME, password=DB_PASSWORD, host=DB_HOST, user=DB_USER)


