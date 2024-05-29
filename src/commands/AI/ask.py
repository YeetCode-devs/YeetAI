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

import json
import logging
import os

from openai import AsyncOpenAI
from openai.types import Completion
from pyrogram.client import Client
from pyrogram.types import Message

SYSTEM_PROMPT: str = (
    f"You are YeetAIBot, designed to be multipurpose. You can answer math questions, general "
    f"questions, and more. "
    f"Ignore /ask or /ask@{os.getenv('BOT_USERNAME')} at the start of user's message. "
    f"If the resulting message after ignoring those is empty, respond with 'Please give me a prompt!'"
    f"Your response will be sent to telegram. Please limit your output to 4096 character otherwise the message will fail to send."
)
log: logging.Logger = logging.getLogger(__name__)


class LoggedList(list):
    def __init__(self):
        self.log = log.getChild("LoggedList")
        self.log.info(f"Note: LoggedList instantiated. This is a custom wrapper around regular list.")
        super().__init__()

    def append(self, obj):
        self.log.info(f"Appending: {obj}")
        super().append(obj)

    def insert(self, index, obj):
        self.log.info(f"Inserting: {obj}")
        super().insert(index, obj)

    def reverse(self):
        self.log.info("Reversing")
        super().reverse()


client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_URL"),
)


async def generate_response(user_prompts: list[dict[str, str]]) -> str:
    system_prompt: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    resultant_prompt: list[dict[str, str]] = system_prompt + user_prompts

    log.info(f"Generating response with prompt:\n{json.dumps(resultant_prompt, indent=2)}")

    try:
        response: Completion = await client.chat.completions.create(
            model="pai-001",  # Custom model
            messages=resultant_prompt,
        )
        return response.choices[0].message.content  # type: ignore
    except Exception as e:
        log.error(f"Could not create a prompt!: {e}")
        raise


async def execute(app: Client, message: Message):
    my_id: int = (await app.get_me()).id
    previous_prompts: list[dict[str, str]] = LoggedList()

    if message.reply_to_message:
        # If we were to use message.reply_to_message directly, we cannot get subsequent replies
        reply_to_message = await app.get_messages(message.chat.id, message.reply_to_message.id, replies=20)
    else:
        reply_to_message = None

    # Track (at max 20) replies to preserve context
    while reply_to_message is not None:
        if reply_to_message.from_user.id == my_id:  # type: ignore
            previous_prompts.append(
                {"role": "assistant", "content": reply_to_message.text[reply_to_message.text.index(" ") + 1 :]}
            )
        else:
            previous_prompts.append(
                {"role": "user", "content": reply_to_message.text[reply_to_message.text.index(" ") + 1 :]}
            )

        reply_to_message = reply_to_message.reply_to_message  # type: ignore

    previous_prompts.reverse()
    previous_prompts.append({"role": "user", "content": message.text[message.text.index(" ") + 1 :]})

    to_edit = await message.reply("Generating response...", reply_to_message_id=message.id)

    response: str = await generate_response(previous_prompts)
    await to_edit.edit_text(response)


data = {
    "name": "ask",
    "description": "Ask ChatGPT anything.",
    "alias": ["ai", "chatgpt"],  # Optional
    "usage": "/ask <query>",
    "example": "/ask Hello there!",
    "category": "AI",
    "execute": execute,
}
