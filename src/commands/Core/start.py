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

from pyrogram.client import Client
from pyrogram.types import Message


async def execute(app: Client, message: Message) -> None:
    await message.reply("Hello.")


data = {
    "name": "start",
    "description": "Starts the bot.",
    # "alias": ["on"], # Optional
    "usage": "/start",
    "example": "/start",
    "category": "Core",
    "execute": execute,
}
