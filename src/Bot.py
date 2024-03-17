from dotenv import load_dotenv
from pyrogram import Client, filters
from os import getenv


def main() -> None:
    load_dotenv()

    api_id = getenv("API_ID")
    api_hash = getenv("API_HASH")
    bot_token = getenv("BOT_TOKEN")
    bot_username = getenv("BOT_USERNAME")

    app = Client(bot_username, api_id=api_id, api_hash=api_hash, bot_token=bot_token)

    @app.on_message(filters.command("start"))
    async def hello(client, message):
        await message.reply("Hello, world!")

    app.run()
