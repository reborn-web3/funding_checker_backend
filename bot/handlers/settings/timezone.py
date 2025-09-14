from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.models.user import User
from bot.db.user_db import Database
from bot.keyboards.inline import start_menu_keyboard, select_timezone_keyboard, change_settings_keyboard
from bot.text.profile_format import profile_text


timezone_router = Router()

@timezone_router.callback_query(F.data.startswith("tz"))
async def handle_timezone(callback: CallbackQuery, db: Database):
    tz = callback.data.split("|", 1)[1]       
    user = User.from_aiogram(callback.from_user, timezone=tz)
    
    if await db.user_exists(user.id):
        await db.set_user_timezone(user.id, tz)
        user = await db.get_user(user.id)
        text = await profile_text(user)
        await callback.message.edit_text(
            text=text,
            reply_markup=change_settings_keyboard()
        )
        return
    else:
        await db.ensure_user(user)
        await callback.message.edit_text(
            f"⏰ Часовой пояс установлен: {tz}\n\nПора собирать фандинги, Господин {callback.from_user.first_name}!",
            reply_markup=start_menu_keyboard()
        )
        await callback.answer()

@timezone_router.callback_query(F.data == "change_timezone")
async def change_timezone(callback: CallbackQuery, db: Database):
    await callback.message.edit_text(
        "Выберите ваш часовой пояс:",
        reply_markup=select_timezone_keyboard()
    )
    await callback.answer()
