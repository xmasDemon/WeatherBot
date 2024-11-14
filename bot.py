import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = '8111938079:AAFNDYDgyWyJYn7YLDYspo0J9L28F2plJsg'
WEATHER_API_KEY = '4d1824965fa0e6061bad891ef798b425'
CITY = 'Samara'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Хендлер для команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я погодный бот. Используйте команду /help для получения списка доступных команд.")

# Хендлер для команды /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("/weather - Получить актуальную погоду в Самаре.")

# Хендлер для кнопки погоды
@dp.message_handler(commands=['weather'])
async def weather_button(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    weather_button = InlineKeyboardButton("Получить погоду в Самаре", callback_data='get_weather')
    keyboard.add(weather_button)
    await message.reply("Нажмите кнопку, чтобы получить погоду в Самаре:", reply_markup=keyboard)

# Хендлер для обработки нажатия кнопки
@dp.callback_query_handler(lambda c: c.data == 'get_weather')
async def process_callback_get_weather(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    weather_data = fetch_weather(CITY)
    if weather_data:
        await bot.send_message(callback_query.from_user.id, weather_data)
    else:
        await bot.send_message(callback_query.from_user.id, "Не удалось получить данные о погоде.")

def fetch_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f"Погода в {city.capitalize()}: {weather_description}, температура: {temperature}°C."
    else:
        return None

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
