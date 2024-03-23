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

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from src.Module import ModuleBase


class Module(ModuleBase):
    def on_load(self, app: Client):
        app.add_handler(MessageHandler(start, filters.command("start")))

    def on_shutdown(self, app: Client):
        pass


async def start(app: Client, message: Message):
    await message.reply("Hello!")
