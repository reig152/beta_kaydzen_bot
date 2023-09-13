import logging

from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app.apps.core.bot.handlers import router as core_router
from app.apps.core.bot.send_importance import router as send_importance
from app.apps.core.bot.send_urgency import router as send_urgency
from app.apps.core.bot.send_classificator import router as send_classificator
from app.apps.core.bot.send_description import router as send_description
from app.apps.core.bot.send_effect import router as send_effect
from app.apps.core.bot.send_naming import router as send_naming
from app.apps.core.bot.send_solution import router as send_solution
from app.apps.core.bot.send_reason import router as send_reason
from app.apps.core.bot.concern_send import router as concern_send
from app.config.bot import (RUNNING_MODE, TG_TOKEN,
                            RunningMode,
                            WEB_SERVER_HOST, WEB_SERVER_PORT,
                            WEBHOOK_PATH, BASE_WEBHOOK_URL)


bot = Bot(TG_TOKEN, parse_mode="HTML")

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def _register_routers() -> None:
    dp.include_routers(
        core_router,
        send_importance,
        send_classificator,
        send_urgency,
        send_description,
        send_effect,
        send_naming,
        send_solution,
        send_reason,
        concern_send
    )


async def _set_bot_commands() -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Start bot"),
            BotCommand(command="/statuses", description="Показать статусы обеспокоенностей"),
        ]
    )


async def on_startup(bot: Bot) -> None:
    _register_routers()

    await _set_bot_commands()

    if RUNNING_MODE == RunningMode.WEBHOOK:
        await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}")


def run_polling() -> None:
    dp.run_polling(bot)


def run_webhook() -> None:
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)



if __name__ == "__main__":
    dp.startup.register(on_startup)


    if RUNNING_MODE == RunningMode.LONG_POLLING:
        run_polling()
    elif RUNNING_MODE == RunningMode.WEBHOOK:
        run_webhook()
    else:
        raise RuntimeError(f"Unknown running mode: {RUNNING_MODE}")
