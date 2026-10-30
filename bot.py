"""Telegram-бот «Помощник студента»."""

import asyncio
import logging
import os
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
# Прокси необязателен: задаётся, только если Telegram недоступен напрямую.
TELEGRAM_PROXY = os.environ.get("TELEGRAM_PROXY") or None
# На Amvera /data — постоянное хранилище, оно не стирается при пересборке.
DB_PATH = os.environ.get("DB_PATH") or (
    "/data/bot.db" if os.path.isdir("/data") else "bot.db"
)

START_TEXT = (
    "Привет, {name}! 👋\n"
    "Я помощник твоей группы: скоро здесь будут расписание и домашка.\n"
    "Рад знакомству! ✨"
)

dp = Dispatcher()


def init_db() -> None:
    # Только создаём таблицы, если их нет. Существующие данные не трогаем.
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                first_name  TEXT,
                username    TEXT,
                created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_user(telegram_id: int, first_name: str | None, username: str | None) -> None:
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            """
            INSERT INTO users (telegram_id, first_name, username)
            VALUES (?, ?, ?)
            ON CONFLICT (telegram_id) DO UPDATE SET
                first_name = excluded.first_name,
                username   = excluded.username
            """,
            (telegram_id, first_name, username),
        )


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user = message.from_user
    name = (user.first_name if user else None) or "друг"
    if user:
        save_user(user.id, user.first_name, user.username)
    await message.answer(START_TEXT.format(name=name))


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    if not BOT_TOKEN:
        raise SystemExit("Не задана переменная окружения BOT_TOKEN")

    init_db()
    logging.info("База данных: %s", DB_PATH)

    session = AiohttpSession(proxy=TELEGRAM_PROXY) if TELEGRAM_PROXY else None
    bot = Bot(token=BOT_TOKEN, session=session)

    # При перезапуске на хостинге старый экземпляр может ещё работать пару секунд.
    # Пауза снимает ошибку «Terminated by other getUpdates request».
    await asyncio.sleep(5)
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
