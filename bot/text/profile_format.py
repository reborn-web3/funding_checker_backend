from bot.db.user_db import Database
from bot.keyboards.inline import back_to_start_menu_keyboard
from bot.db.user_db import Database


async def profile_text(user: dict) -> str:
    text = f"👤 <b>Ваш профиль, {user.get('first_name')}</b>\n\n"
    
    text += f"🌍 <b>Часовой пояс:</b> {user.get('timezone', 'Not set')}\n"
    text += f"⏳ <b>Ближайшее время фандинга (часов):</b> {user.get('upcoming_funding_time', 'Not set')}\n"
    # text += f"⏰ <b>Notification Time:</b> {user.get('notification_time', 'Not set')}\n"
    # text += f"📊 <b>Tracked Tickers:</b> {', '.join(user.get('tracked_tickers', [])) if user.get('tracked_tickers') else 'None'}\n"
    return text    