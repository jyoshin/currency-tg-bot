import asyncio
import logging
from os import getenv
import requests
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Logging for messages
logging.basicConfig(level=logging.INFO)
# TOKEN
bot = Bot(token="")
# DISPATCHER
dp = Dispatcher()

# Handler for /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("<code>Enter currecny code:</code>", parse_mode="HTML") 

# Handler for currency
@dp.message(Command("currency"))
async def process_currency_code(message: types.Message):

    full_command = message.text.upper()   
    currency_code = full_command.replace('/CURRENCY', '').strip()
    
    if any(char.isdigit() for char in currency_code) or has_special_characters(currency_code):
        await message.answer("<code>Try another code.</code>", parse_mode="HTML")
    else:
        response = requests.get(f'https://v6.exchangerate-api.com/v6/API-KEY/pair/{currency_code}/KZT')
        data = response.json()
        conversion_rate = data.get('conversion_rate')

        if conversion_rate is not None:
            await message.answer(f"<code>KZT to {currency_code} is {conversion_rate:.2f}</code>", parse_mode="HTML")
        else:
            await message.answer("<code>Try another code.</code>", parse_mode="HTML")

# Currency URLs
currency_urls = {
    "USD": 'https://v6.exchangerate-api.com/v6/API-KEY//pair/USD/KZT',
    "EUR": 'https://v6.exchangerate-api.com/v6/API-KEY//pair/EUR/KZT',
    "RUB": 'https://v6.exchangerate-api.com/v6/API-KEY//pair/RUB/KZT',
    "GBP": 'https://v6.exchangerate-api.com/v6/API-KEY//pair/GBP/KZT',
}

# Handler for latest
async def fetch_conversion_rate(currency, url):
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        conversion_rate = data.get("conversion_rate")
        return f"<code>{currency}: {conversion_rate:.4f}</code>"
    else:
        return f"Unable to fetch {currency} conversion rate."  

@dp.message(Command("latest"))          
async def process_currency_code(message: types.Message):
    extracted_currencies = await asyncio.gather(*(fetch_conversion_rate(currency, url) for currency, url in currency_urls.items()))
    
    response_text = "\n".join(extracted_currencies)
    
    await message.answer(response_text, parse_mode="HTML") 

# Check for digits
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

# Check for special characters
def has_special_characters(inputString):
    special_characters = "!@#$%^&*()_+-=[]{}|;:'\",.<>?/\\"
    return any(char in special_characters for char in inputString)
    
# Start polling
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
