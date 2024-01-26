from dataclasses import dataclass
from typing import List
from telebot.types import LabeledPrice

from config import PROVIDER_TOKEN


@dataclass
class Product:
    title: str
    description: str
    start_parameter: str
    prices: List[LabeledPrice]
    currency: str = 'USD'
    provider_data: dict =None
    photo_url: str = None
    photo_size: int = None
    photo_width: int =None
    photo_height: int = None
    need_name: bool = False
    need_phone_number: bool = False
    send_phone_number_to_provider: bool = False
    send_email_number_to_provider: bool = False
    is_flexible: bool = False
    provider_token: str = PROVIDER_TOKEN


    def generate_invoice(self):
        return self.__dict__












