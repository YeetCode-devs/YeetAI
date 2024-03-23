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

from telethon import TelegramClient
from telethon.events import NewMessage

from src.Module import ModuleBase


class Module(ModuleBase):
    def on_load(self, app: TelegramClient):
        app.add_event_handler(start, NewMessage(incoming=True, pattern="/start"))

    def on_shutdown(self, app: TelegramClient):
        pass


async def start(event: NewMessage.Event):
    await event.reply("Hello!")
