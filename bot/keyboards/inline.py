from aiogram import types


def select_timezone_keyboard() -> types.InlineKeyboardMarkup:
    zones = [
        "UTC-8", "UTC-7", "UTC-6", "UTC-5",
        "UTC-4", "UTC-3", "UTC-2", "UTC-1",
        "UTC-0",
        "UTC+1", "UTC+2", "UTC+3", "UTC+4",
        "UTC+5", "UTC+6", "UTC+7", "UTC+8", "UTC+9"
    ]
    kb_rows = [zones[i:i+3] for i in range(0, len(zones), 3)]
    buttons = [
        [types.InlineKeyboardButton(text=z, callback_data=f"tz|{z}") for z in row]
        for row in kb_rows
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

def select_upcoming_funding_time_keyboard() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(text="1 час", callback_data="upcoming_funding_time|1"),
        types.InlineKeyboardButton(text="2 часа", callback_data="upcoming_funding_time|2"),
        types.InlineKeyboardButton(text="4 часа", callback_data="upcoming_funding_time|4"),
        types.InlineKeyboardButton(text="6 часов", callback_data="upcoming_funding_time|6"),
        types.InlineKeyboardButton(text="8 часов", callback_data="upcoming_funding_time|8"),
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=[buttons])

def change_settings_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Изменить часовой пояс", callback_data="change_timezone")],
        [types.InlineKeyboardButton(text="Изменить ближайшее время фандинга", callback_data="change_upcoming_funding_time")],
        # [types.InlineKeyboardButton(text="Изменить время уведомлений", callback_data="change_notification_time")],
        # [types.InlineKeyboardButton(text="Отслеживаемые тикеры", callback_data="manage_tracked_tickers")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back|start")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

def start_menu_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="🔥 Топ 5", callback_data="top5")],
        [types.InlineKeyboardButton(text="Ближайшие фандинги", callback_data="select_upcoming")],
        [types.InlineKeyboardButton(text="Выбрать биржу", callback_data="select_exchange")],
        [types.InlineKeyboardButton(text="👤 Мой профиль", callback_data="my_profile")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

def select_exchange_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Kucoin", callback_data="funding_kucoin")],
        [types.InlineKeyboardButton(text="MEXC", callback_data="funding_mexc")],
        [types.InlineKeyboardButton(text="Gate.io", callback_data="funding_gate")],
        [types.InlineKeyboardButton(text="Bybit", callback_data="funding_bybit")],
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back|start")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

def back_to_start_menu_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back|start")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

def back_to_exchange_selection_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="⬅️ Назад", callback_data="back|exchanges")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)