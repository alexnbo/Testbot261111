import requests
from config import open_weather_token, bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await  message.reply("Погоду в каком городе тебе сообщить?")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Dizzle": "Дождь \U00002614",
        "Tunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001f328",
        "Mist": " Туман\U0001f32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        city = data["name"]
        cur_weather = data["main"]["temp"]
        weather_discription = data["weather"][0]["main"]
        if weather_discription in code_to_smile:
            wd = code_to_smile[weather_discription]
        else:
            wd = "Там что то странное"
        feels_weather = data["main"]["feels_like"]
        wind = data["wind"]["speed"]

        await message.reply(
            f"Погода сейчас в {city}\nТемп. {cur_weather} C {wd} и ощущается как {feels_weather} C, ветер: {wind} м/с"
        )
    except:
        await message.reply("\U00002620 Проверьте название города")


if __name__ == '__main__':
    executor.start_polling(dp)
