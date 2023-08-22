import logging

from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis

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
from app.config.bot import RUNNING_MODE, TG_TOKEN, WEBHOOK_URL, RunningMode

bot = Bot(TG_TOKEN, parse_mode="HTML")
# redis: Redis = Redis(host=REDIS_HOST, password=REDIS_PASS)
storage: MemoryStorage = MemoryStorage()

dispatcher = Dispatcher(storage=storage)

app = web.Application()
webhook_path = f'/{TG_TOKEN}'

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def _register_routers() -> None:
    dispatcher.include_routers(
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


@dispatcher.startup()
async def on_startup() -> None:
    # Register all routers
    _register_routers()

    # Set default commands
    await _set_bot_commands()

    if RUNNING_MODE == RunningMode.WEBHOOK:
        # await set_webhook()
        webhook_uri = f'{WEBHOOK_URL}{webhook_path}'
        await bot.set_webhook(
            webhook_uri
        )


def run_polling() -> None:
    dispatcher.run_polling(bot)


# async def set_webhook():
#     webhook_uri = f'{WEBHOOK_URL}{webhook_path}'
#     await bot.set_webhook(
#         webhook_uri
#     )


async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index+1:]
    if token == TG_TOKEN:
        update = types.Update(**await request.json())
        await dispatcher.process_update(update)
        return web.Response()
    else:
        return web.Response(status=403)


def run_webhook() -> None:
    app.router.add_post(f'/{TG_TOKEN}', handle_webhook)

    web.run_app(
        app, 
        host='0.0.0.0', 
        port=8000
    )


if __name__ == "__main__":
    if RUNNING_MODE == RunningMode.LONG_POLLING:
        run_polling()
    elif RUNNING_MODE == RunningMode.WEBHOOK:
        run_webhook()
    else:
        raise RuntimeError(f"Unknown running mode: {RUNNING_MODE}")
