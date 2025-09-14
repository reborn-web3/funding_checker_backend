from aiogram import Router, types, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import back_to_exchange_selection_keyboard, select_exchange_keyboard
from bot.text.exchanges_format import format_funding
from bot.db.user_db import Database

from src.config import *
from src.db import get_latest_funding


exchanges_router = Router()

async def select_exchange(message: types.Message):
    await message.answer(
        "Выберите биржу, чтобы посмотреть фандинги:",
        reply_markup=select_exchange_keyboard()
    )

@exchanges_router.callback_query(F.data == "funding_kucoin")
async def handle_kucoin(callback: CallbackQuery, db: Database):
    exchange = 'kucoin'
    user_tz = await db.get_user_timezone(callback.from_user.id)
    latest_funding = await get_latest_funding(exchange)
    await callback.message.edit_text(
        text=await format_funding(latest_funding, exchange, user_tz),
        parse_mode="HTML", 
        reply_markup=back_to_exchange_selection_keyboard(),
        disable_web_page_preview=True
    )
    await callback.answer()

@exchanges_router.callback_query(F.data == "funding_mexc")
async def handle_mexc(callback: CallbackQuery, db: Database):
    exchange = 'mexc'
    user_tz = await db.get_user_timezone(callback.from_user.id)
    latest_funding = await get_latest_funding(exchange)
    await callback.message.edit_text(
        text=await format_funding(latest_funding, exchange, user_tz),
        parse_mode="HTML", 
        reply_markup=back_to_exchange_selection_keyboard(),
        disable_web_page_preview=True
    )
    await callback.answer()

@exchanges_router.callback_query(F.data == "funding_gate")
async def handle_gate(callback: CallbackQuery, db: Database):
    exchange = 'gate'
    user_tz = await db.get_user_timezone(callback.from_user.id)
    latest_funding = await get_latest_funding(exchange)
    await callback.message.edit_text(
        text=await format_funding(latest_funding, exchange, user_tz),
        parse_mode="HTML", 
        reply_markup=back_to_exchange_selection_keyboard(),
        disable_web_page_preview=True
    )
    await callback.answer()

@exchanges_router.callback_query(F.data == "funding_bybit")
async def handle_gate(callback: CallbackQuery, db: Database):
    exchange = 'bybit'
    user_tz = await db.get_user_timezone(callback.from_user.id)
    latest_funding = await get_latest_funding(exchange)
    await callback.message.edit_text(
        text=await format_funding(latest_funding, exchange, user_tz),
        parse_mode="HTML", 
        reply_markup=back_to_exchange_selection_keyboard(),
        disable_web_page_preview=True
    )
    await callback.answer()