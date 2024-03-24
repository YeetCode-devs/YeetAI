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

import asyncio
import logging
import os
import random

from g4f.client import Client as g4fClient
from g4f.models import default
from g4f.Provider import Bing, FreeChatgpt
from g4f.stubs import ChatCompletion
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from src.Module import ModuleBase

SYSTEM_PROMPT: str = (
    f"You are YeetAIBot, designed to be multipurpose. You can answer math questions, general "
    f"questions, and more. "
    f"Ignore /ask or /ask@{os.getenv('BOT_USERNAME')} at the start of user's message. "
    f"If the resulting message after ignoring those is empty, respond with 'Please give me a prompt!'"
)
log: logging.Logger = logging.getLogger(__name__)
log.info(f"{asyncio.get_event_loop_policy()}")


class Module(ModuleBase):
    def on_load(self, app: Client):
        app.add_handler(MessageHandler(cmd_ask, filters.command("ask")))
        pass

    def on_shutdown(self, app: Client):
        pass


async def generate_response(prompt: str) -> str:
    provider: type[Bing, FreeChatgpt] = random.choice([Bing, FreeChatgpt])
    client: g4fClient = g4fClient(provider=provider)

    try:
        response: ChatCompletion = await asyncio.get_running_loop().run_in_executor(
            None,
            client.chat.completions.create,
            [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
            default,
        )
        return response.choices[0].message.content
    except Exception as e:
        log.error(f"Could not create a prompt! {e}")
        raise


async def cmd_ask(app: Client, message: Message):
    response: str = await generate_response(message.text)
    await message.reply("hi")
