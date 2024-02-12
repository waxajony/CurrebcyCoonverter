from aiogram import Router
from aiogram.types import Message

from config import courses

msg_router = Router()


@msg_router.message()
async def convert_sum(message: Message):
    try:
        x = int(message.text)
        s = f"{x} so'm\n\n"
        s += f"\t -{x / courses['USD']: .2f} dollar\n"
        s += f"\t -{x / courses['EUR']: .2f} yevro\n"
        s += f"\t -{x / courses['RUB']: .2f} rubl\n"
        await message.reply(text=s)
    except ValueError:
        await message.reply("Iltimos, faqat son kiriting yoki /help ni bosing!")





