from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import *


back_router = Router()

@back_router.callback_query(F.data.startswith("back|"))
async def universal_back(callback: CallbackQuery):
    path = callback.data.split("|", 1)[1]
    user = callback.from_user
    username = user.first_name or user.username
    match path:
        case 'start':
            await callback.message.edit_text(f'Пора собирать фандинги, Господин {username}! ', reply_markup=start_menu_keyboard())
        # case "menu":
        #      await callback.message.edit_text(' ', reply_markup=start_menu_keyboard())
        case "exchanges":
            await callback.message.edit_text('Выберите биржу', reply_markup=select_exchange_keyboard())
    await callback.answer()

