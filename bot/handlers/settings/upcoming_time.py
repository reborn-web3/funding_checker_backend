from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.models.user import User
from bot.db.user_db import Database
from bot.keyboards.inline import start_menu_keyboard, select_upcoming_funding_time_keyboard
from bot.text.profile_format import profile_text


upcoming_time_router = Router()

@upcoming_time_router.callback_query(F.data.startswith("upcoming_funding_time"))
async def handle_upcoming_time(callback: CallbackQuery, db: Database):
    hours = callback.data.split("|", 1)[1]       
    user_id = callback.from_user.id
    await db.set_user_upcoming_funding_time(user_id, hours)

    await callback.message.edit_text(
        f"⏰ Ближайшее время установленно: {hours}\nПора собирать фандинги, Господин {callback.from_user.first_name}!",
        reply_markup=start_menu_keyboard()
    )
    await callback.answer()

@upcoming_time_router.callback_query(F.data == "change_upcoming_funding_time")
async def change_timezone(callback: CallbackQuery, db: Database):
    await callback.message.edit_text(
        text = '⏳ Уcтановите время, в течении которого будут фандинги\n',
        reply_markup=select_upcoming_funding_time_keyboard()
    )
    await callback.answer()
