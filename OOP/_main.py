"""Создание телеграмм бота который будет отправлять сообщение о текущей цене криптовалюты"""
import os
import asyncio
import aiohttp
from dotenv import load_dotenv
import telebot

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

API_TOKEN = os.getenv("NEW_API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)


async def get_crypto_data(session, symbol):
    """
    Получает данные о цене указанной криптовалюты из API Binance.

    Аргументы:
    - session: объект aiohttp.ClientSession для выполнения HTTP-запросов
    - symbol: символ криптовалюты (например, BTC, ETH, BNB)

    Возвращает:
    - словарь с данными о цене криптовалюты или None, если данные недоступны
    """
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}USDT"
    async with session.get(url) as response:
        data = await response.json()
        return data


@bot.message_handler(commands=["start"])
def handle_start(message):
    """
    Обрабатывает команду /start и выводит клавиатуру с кнопками выбора криптовалюты.
    """
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text="Bitcoin")
    button2 = telebot.types.KeyboardButton(text="Ethereum")
    button3 = telebot.types.KeyboardButton(text="Binance Coin")
    keyboard.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Выберите криптовалюту:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def handle_crypto_buttons(message):
    """
    Обрабатывает нажатие кнопок выбора криптовалюты и отправляет цену выбранной криптовалюты.

    Аргументы:
    - message: объект telebot.types.Message с информацией о сообщении
    """
    crypto = message.text.lower()
    symbol = ""
    if crypto == "bitcoin":
        symbol = "BTC"
    elif crypto == "ethereum":
        symbol = "ETH"
    elif crypto == "binance coin":
        symbol = "BNB"

    async def get_crypto():
        async with aiohttp.ClientSession() as session:
            data = await get_crypto_data(session, symbol)
            if data is not None and "price" in data:
                price = data.get("price")
                response = f"Текущая цена {crypto.upper()}: {price}"
                print(f"Ответ от API Binance для {crypto.upper()}: {data}")
            else:
                response = f"Не удалось получить данные по {crypto.upper()}"
            bot.send_message(message.chat.id, response)

    asyncio.run(get_crypto())


if __name__ == "__main__":
    bot.polling()
