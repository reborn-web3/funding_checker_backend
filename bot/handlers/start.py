from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery

from bot.models.user import User
from bot.db.user_db import Database
from bot.keyboards.inline import select_timezone_keyboard, start_menu_keyboard


start_router = Router()

@start_router.message(CommandStart())
async def start(message: types.Message, db: Database):
    user_obj = message.from_user
    
    if not await db.user_exists(user_obj.id):
        await message.answer(
            "Выберите ваш часовой пояс для корректного отображения времени",
            reply_markup=select_timezone_keyboard()
        )
    else:
        user = User.from_aiogram(user_obj)
        await db.ensure_user(user)
        await message.answer(
        f"Пора собирать фандинги, Господин {user.username}!\n\n",
        reply_markup=start_menu_keyboard()
    )



