import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis

from app.apps.core.bot.handlers import router as core_router
from app.apps.core.bot.send_importance import router as send_importance
from app.config.bot import RUNNING_MODE, TG_TOKEN, RunningMode, REDIS_HOST, REDIS_PASS

bot = Bot(TG_TOKEN, parse_mode="HTML")
storage: MemoryStorage = MemoryStorage()

dispatcher = Dispatcher(storage=storage)
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def _register_routers() -> None:
    dispatcher.include_routers(
        core_router,
        send_importance
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


def run_polling() -> None:
    dispatcher.run_polling(bot)


def run_webhook() -> None:
    raise NotImplementedError("Webhook mode is not implemented yet")


if __name__ == "__main__":
    if RUNNING_MODE == RunningMode.LONG_POLLING:
        run_polling()
    elif RUNNING_MODE == RunningMode.WEBHOOK:
        run_webhook()
    else:
        raise RuntimeError(f"Unknown running mode: {RUNNING_MODE}")
