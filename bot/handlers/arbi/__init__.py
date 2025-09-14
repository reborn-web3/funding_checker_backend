from aiogram import Router

arbitrage_router = Router()

from .arbi import arbi_router

arbitrage_router.include_routers(
    arbi_router
)