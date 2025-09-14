from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.db.user_db import Database
from bot.keyboards.inline import change_settings_keyboard
from bot.text.profile_format import profile_text

profile_router = Router()

@profile_router.callback_query(F.data == "my_profile")
async def handle_my_profile(callback: CallbackQuery, db: Database):
    user = await db.get_user(callback.from_user.id)
    
    await callback.message.edit_text(
        text = await profile_text(user),
        disable_web_page_preview=True,
        reply_markup=change_settings_keyboard()

    )
    await callback.answer()