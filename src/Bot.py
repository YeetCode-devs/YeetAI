# SPDX-License-Identifier: GPL-3.0-only
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Copyright (c) 2024, YeetCode Developers <YeetCode-devs@protonmail.com>

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
