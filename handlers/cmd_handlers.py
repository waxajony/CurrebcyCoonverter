import requests
import datetime


from aiogram import Router
from aiogram.filters import CommandStart, Command

from aiogram.types import Message, FSInputFile
from config import courses
cmd_router = Router()

@cmd_router.message(CommandStart())
async def cmd_start(message: Message):
    s = ("Assalomu Alaykum!\nValyuta kurslari haqida ma`lumot beruvchi botimizga xush kelibsiz!\nYordam uchun /help" 
         " Buyrugini bosing")
    await message.answer(text=s)


@cmd_router.message(Command('help'))
async def cmd_help(message: Message):
    s = "Quyidagi komandalar yordamida botdan samarali foydalanishingiz mukin:\n"

    s += "\t/kurslar - valyuta kurslarini bilsh\n"
    s += "\t/dollar - dollar kursini bilish\n"
    s += "\t/yevro -  yevro  kursini bilish\n"
    s += "\t/rubl -  rubl  kursini bilish\n"

    s += "Agar bir summa jonatsangiz, bot uni turli valyutalardagi qiymatini qaytaradi."


    await message.answer(text=s)


@cmd_router.message(Command('kurslar'))
async def cmd_kurslar(message: Message):
    response = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/")
    s = "Bugungi valyuta kurslari:\n"
    for kurs in response.json():
        if kurs['Ccy'] in ['USD', 'EUR', 'RUB']:
            courses[kurs['Ccy']] = float(kurs['Rate'])
            s += f"1 {kurs['CcyNm_RU']} - {kurs['Rate']} so'm\n"
    await message.answer(text=s)

@cmd_router.message(Command('dollar'))
async def cmd_dollor(message:Message):
    s = f"$100 AQSH dollori = {courses['USD']} so'm"
    await message.answer(text=s)
    
@cmd_router.message(Command('yevro'))
async def cmd_yevro(message:Message):
    s = f"€100 yevro = {courses['EUR']} so'm"
    await message.answer(text=s)
    

@cmd_router.message(Command('rubl'))
async def cmd_rubl(message:Message):
    s = f"₽100 rubl = {courses['RUB']} so'm"
    await message.answer(text=s)


@cmd_router.message(Command('hafta'))
async def cmd_hafta(message: Message):
    response = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/")
    s = "Joriy haftadagi 7 kunlik valyuta kurslari:\n"
    for kurs in response.json():
        if kurs['Ccy'] in ['USD', 'EUR', 'RUB']:
            s += f"{kurs['Ccy']}: "
            today = datetime.date.today()
            for i in range(7):
                date = today - datetime.timedelta(days=i)
                kurs_value = next((x['date'] for x in kurs['Rate'] if x == date.strftime('%Y-%m-%d')), None)
                s += f"{kurs_value} UZS, " if kurs_value is not None else "N/A, "
            s += "\n"
    await message.answer(text=s)