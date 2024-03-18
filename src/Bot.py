from dotenv import load_dotenv
from telethon import TelegramClient, events
from os import getenv


def main() -> None:
    load_dotenv()

    api_id = getenv("API_ID", 0)
    api_hash = getenv("API_HASH", "")
    bot_token = getenv("BOT_TOKEN", "")

    if not all([api_id, api_hash, bot_token]):
        raise ValueError("Could not get all required credentials from env!")

    app = TelegramClient("app", int(api_id), api_hash).start(bot_token=bot_token)

    @app.on(events.NewMessage(incoming=True, pattern="/start"))
    async def start(event):
        await event.reply("Hello!")

    app.run_until_disconnected()
