from aiogram import Router

handlers_router = Router()

from .start import start_router
from .menu import menu_router
from .exchanges import exchanges_router
from .profile import profile_router
from .back import back_router
from .settings import settings_router
from .arbi import arbitrage_router
from .ticker_info import ticker_information

handlers_router.include_routers(
    start_router,
    menu_router,
    exchanges_router,
    profile_router,
    back_router,
    settings_router,
    arbitrage_router,
    ticker_information
)