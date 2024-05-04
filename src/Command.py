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
from types import FunctionType
from typing import Any, Callable

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.handlers import MessageHandler

log: logging.Logger = logging.getLogger(__name__)


class CommandData:
    """A data-structure for a command file's data.

    This class can be used by any command-file that need to parse/use a particular command's data
    (for example the help command [TODO!]), of which are stored raw by the command loader.
    It's just for convenience of type-hinting, and is not strictly required to process command data by any mean.
    """

    MANDATORY_FIELD: dict = {
        # field name: required type
        "name": str,
        "description": str,
        "usage": str,
        "execute": FunctionType,
    }

    OPTIONAL_FIELD: dict = {
        # field name: required type
        "alias": list,
        "example": str,
        "category": str,
    }

    def __init__(self, data: dict, command_path: str):
        """Data structure for a module's data.

        Args:
            data (dict): The raw dictionary from the module.
            command_path (str): Path to the command file. Does not have to be absolute;
                this is only used for error message.
        """
        self._data: dict = data
        self._command_path: str = command_path

        log.info(f"Verifying command-file '{self.name}' data structure")

        # Since the loader is no longer using this, sanity check is not needed. However this line (and the method)
        # is kept for future usage/reference.
        # self.sanity_check()

    def _is_correct_type(self, field_name: str, expected_type: Any) -> None:
        """Check if the command-file data has the correct type.

        Notes: This is a private method, and thus it is useless to be used outside of this class.

        Args:
            field_name (str): The key to the dictionary.
            expected_type (:obj:`Any`): The type of the value of the dictionary's key, aka the type that it should have.

        Raises:
            ValueError when the field's type does not match the required type.
        """
        if type(self._data.get(field_name)) != expected_type:
            raise ValueError(
                f"Command '{self._command_path}' implemented the wrong type for '{field_name}' field: "
                f"Expecting '{expected_type}', got '{type(self._data.get(field_name))}' instead"
            )

    def sanity_check(self) -> None:
        """Check if a command file's data is sane."""
        # First check: Mandatory fields
        for field_name, required_type in type(self).MANDATORY_FIELD.items():
            if not self._data.get(field_name):
                # First we check whether the mandatory field exist at all
                raise ValueError(
                    f"Command '{self._command_path}' does not implement the following mandatory field: " f"{field_name}"
                )

            # Then we make sure it is the correct type
            self._is_correct_type(field_name, required_type)

        # Second check: Optional fields
        for field_name, required_type in type(self).OPTIONAL_FIELD.items():
            # First we check whether the optional field exist at all
            if self._data.get(field_name):
                self._is_correct_type(field_name, required_type)

    @property
    def raw_data(self) -> dict:
        """Raw data of the command."""
        return self._data

    @property
    def name(self) -> str:
        """Name of the command."""
        return self._data["name"]

    @property
    def description(self) -> str:
        """Description of the command."""
        return self._data["description"]

    @property
    def usage(self) -> str:
        """Usage of the command."""
        return self._data["usage"]

    @property
    def execute(self) -> FunctionType:
        """Function to execute the command."""
        return self._data["execute"]

    @property
    def alias(self) -> list[str]:
        """Aliases of the command. Empty list if there's none."""
        return self._data.get("alias", [])

    @property
    def example(self) -> str:
        """Example of the command. Empty string if there's none."""
        return self._data.get("example", "")

    @property
    def category(self) -> str:
        """Category of the command. Empty string if there's none."""
        return self._data.get("category", "")


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
        commands.append(cmd_data.get("name"))

        # Collect main cmd trigger and its aliases
        triggers: list[str] = cmd_data["name"]
        if cmd_data.get("alias"):
            triggers = [*triggers, *cmd_data["alias"]]

        # Now register execute function as handler, with main trigger and its aliases, all at once
        app.add_handler(MessageHandler(cmd_data["execute"], filters.command(triggers)))

        return commands
