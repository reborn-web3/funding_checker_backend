from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.config import *
from src.db.database import get_top_funding_across_exchanges, get_upcoming_funding

from bot.db.user_db import Database
from bot.keyboards.inline import back_to_start_menu_keyboard, select_exchange_keyboard, select_upcoming_funding_time_keyboard

from bot.text.top5_format import handle_top5_formating
from bot.text.upcoming_format import handle_upcoming_funding_formating, time_phrase


menu_router = Router()

@menu_router.callback_query(F.data == "top5")
async def handle_top5(callback: CallbackQuery, db: Database):
    """Показывает топ-5 самых больших фандингов среди всех бирж"""
    user_tz = await db.get_user_timezone(callback.from_user.id)
    try:
        top_funding = await get_top_funding_across_exchanges(limit=5)
        
        if not top_funding:
            await callback.answer("❌ Данных пока нет.")
            return
        
        await callback.message.edit_text(
            text=await handle_top5_formating(top_funding, user_tz), 
            parse_mode="HTML", 
            disable_web_page_preview=True,
            reply_markup=back_to_start_menu_keyboard()
        )
        
    except Exception as e:
        await callback.message.answer("❌ Ошибка при получении данных о фандинге.")
        print(f"Error in top_funding_command: {e}")
    
@menu_router.callback_query(F.data == "select_upcoming")
async def handle_upcoming(callback: CallbackQuery, db: Database):
    if await db.is_user_upcoming_funding_time_exist(callback.from_user.id):
        user_tz = await db.get_user_timezone(callback.from_user.id)
        user_upcoming_funding_time = (await db.get_user_upcoming_funding_time(callback.from_user.id))[0]
        upcoming_funding = await get_upcoming_funding(user_upcoming_funding_time)
        
        
        if not upcoming_funding:
            await callback.message.edit_text(
                f"🙅‍♂️ {await time_phrase(user_upcoming_funding_time)} фандингов нет.",
                reply_markup=back_to_start_menu_keyboard()
            )
            await callback.answer()
            return
        
        text = await handle_upcoming_funding_formating(upcoming_funding, user_tz, user_upcoming_funding_time)

        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=back_to_start_menu_keyboard()
        )
        await callback.answer()
    else:
        await callback.message.edit_text(
            text = "⏳ Уcтановите время, в течении которого будут фандинги\n",
            reply_markup=select_upcoming_funding_time_keyboard()
        )
        await callback.answer()

@menu_router.callback_query(F.data == "select_exchange")
async def handle_exchange(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите биржу, чтобы посмотреть фандинги:",
        reply_markup=select_exchange_keyboard()
    )
    await callback.answer()


