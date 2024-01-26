from telebot.handler_backends import State, StatesGroup

class RegisterState(StatesGroup):
    name = State()
    lastname =State()
    contact = State()
    birthdate = State()
    submit = State()


class CartState(StatesGroup):
    cart = State()













