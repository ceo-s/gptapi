import os
from dotenv import load_dotenv
from threading import Thread
from asyncio import run
from aiohttp import ClientSession
from logging import Handler, LogRecord

load_dotenv(".env")

BOT_TOKEN = os.getenv("NOTIFICATION_BOT_TOKEN")


async def telegram_send_message(message: str):
    async with ClientSession() as session:
        await session.get(url=f"/bot{BOT_TOKEN}/sendMessage", params={
            "chat_id": id, "text": message, "parse_mode": "HTML"})


class TelegramHandler(Handler):
    def __init__(self) -> None:
        super().__init__()

    def emit(self, record: LogRecord) -> None:
        message = self.format(record)
        coro = telegram_send_message(message)
        thr = Thread(target=run, args=(coro, ))
        thr.setDaemon(True)
        thr.start()
