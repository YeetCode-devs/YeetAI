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

import logging
from importlib import import_module
from os.path import sep
from pathlib import Path
from typing import Callable

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.handlers import MessageHandler

log: logging.Logger = logging.getLogger(__name__)


def load_commands(app: Client) -> list[dict[str, str | Callable]]:
    commands_dir_name: str = "commands"
    bot_src_dir: Path = Path(__file__).parent
    bot_root: Path = bot_src_dir.parent
    commands_dir: Path = Path(bot_src_dir).joinpath(commands_dir_name)

    commands: list[dict[str, str | Callable]] = []

    for cmdfile in Path(commands_dir).rglob("*.py"):
        if cmdfile.parent.name != "commands":
            log.info(f"Found category: {cmdfile.parent.name}")

        # We use relative to bot_root (instead of bot_src_dir), otherwise we won't
        # get the src. prefix, which will cause import to fail.
        # log.info(str(cmdfile.relative_to(bot_root)).removesuffix(".py").replace(sep, "."))
        cmd: object = import_module(str(cmdfile.relative_to(bot_root)).removesuffix(".py").replace(sep, "."))

        # Make sure data attribute exists
        if not hasattr(cmd, "data"):
            log.warning(f"Command '{cmdfile}' does not have data attribute. Skipping.")
            continue

        cmd_data: dict = getattr(cmd, "data")
        log.info(f"Registering command '{cmd_data['name']}'")

        # Collect cmd datas
        commands.append(cmd_data)

        # Collect main cmd trigger and its aliases
        triggers: list[str] = [cmd_data["name"]]
        if cmd_data.get("alias"):
            triggers = [*triggers, *cmd_data["alias"]]

        # Now register execute function as handler, with main trigger and its aliases, all at once
        app.add_handler(MessageHandler(cmd_data["execute"], filters.command(triggers)))

        return commands
