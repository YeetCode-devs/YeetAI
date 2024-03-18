from dotenv import load_dotenv
from telethon import TelegramClient, events
from os import getenv


def main() -> None:
    load_dotenv()

    api_id = getenv("API_ID")
    api_hash = getenv("API_HASH")
    bot_token = getenv("BOT_TOKEN")

    app = TelegramClient("app", api_id, api_hash).start(bot_token=bot_token)

    @app.on(events.NewMessage(incoming=True, pattern="/start"))
    async def start(event):
        await event.reply("Hello!")

    app.run_until_disconnected()
