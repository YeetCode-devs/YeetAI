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
from os import getenv, listdir
from os.path import abspath, dirname, join

from dotenv import load_dotenv
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.handlers import MessageHandler

from importlib import import_module


def main() -> None:
    load_dotenv(override=True)

    api_id = getenv("API_ID", 0)
    api_hash = getenv("API_HASH", "")
    bot_token = getenv("BOT_TOKEN", "")

    if not all([api_id, api_hash, bot_token]):
        raise ValueError("Could not get all required credentials from env!")

    app = Client("app", int(api_id), api_hash, bot_token=bot_token)

    # g4f sets the event loop policy to WindowsSelectorEventLoopPolicy, which breaks pyrogram
    # It's not particularly caused by WindowsSelectorEventLoopPolicy, and can be caused by
    # setting any other policy, but pyrogram is not expecting a new instance of the event
    # loop policy to be set
    # https://github.com/xtekky/gpt4free/blob/bf82352a3bb28f78a6602be5a4343085f8b44100/g4f/providers/base_provider.py#L20-L22
    # HACK: Restore the event loop policy to the default one
    default_event_loop_policy = asyncio.get_event_loop_policy()
    import g4f  # Trigger g4f event loop policy set # noqa: F401 # pylint: disable=unused-import # isort:skip

    if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
        if isinstance(asyncio.get_event_loop_policy(), asyncio.WindowsSelectorEventLoopPolicy):
            asyncio.set_event_loop_policy(default_event_loop_policy)

    commands_dir_name = "commands"
    commands_dir = join(dirname(abspath(__file__)), commands_dir_name)

    for file in listdir(commands_dir):
        if file.endswith(".py"):
            command_name = file[:-3]
            command = import_module(f"src.{commands_dir_name}.{command_name}")

            if not hasattr(command, "data"):
                print(f"Command {command_name} does not have data attribute.")
                continue

            command_data = getattr(command, "data")

            print(f"Registering command {command_data['name']}")

            # Register the command function
            app.add_handler(MessageHandler(command_data["execute"], filters.command(command_data["name"])))

            # Register aliases if provided
            if "alias" in command_data:
                for alias in command_data["alias"]:
                    print(f"Registering alias {alias} for command {command_data['name']}")

                    app.add_handler(MessageHandler(command_data["execute"], filters.command(alias)))

    app.run()
