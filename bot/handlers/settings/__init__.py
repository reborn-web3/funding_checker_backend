from aiogram import Router

settings_router = Router()

from .timezone import timezone_router
from .upcoming_time import upcoming_time_router

settings_router.include_routers(
    timezone_router,
    upcoming_time_router
)