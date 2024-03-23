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

import atexit
import logging
from abc import ABC, abstractmethod
from importlib import import_module
from pathlib import Path

from telethon import TelegramClient

log: logging.Logger = logging.getLogger(__name__)


class ModuleBase(ABC):
    @abstractmethod
    def on_load(self, app: TelegramClient):
        pass

    @abstractmethod
    def on_shutdown(self, app: TelegramClient):
        pass


def load_modules(app: TelegramClient) -> list[object]:
    loaded_modules: list[object] = []

    log.info("Searching for modules")
    modules: list[Path] = list(Path("modules").rglob("*.py"))
    log.info(f"Found {len(modules)} modules")

    for module in modules:
        log.info(f"Loading module '{module}'")

        mdl = import_module(f"modules.{module.name.removesuffix('.py')}")

        if not hasattr(mdl, "Module"):
            log.error(f"Module '{module}' does not have a Module class, cannot load")
            continue

        if not issubclass(mdl.Module, ModuleBase):
            log.warning(f"Module '{module}' does not inherit from ModuleBase class")

        mdl.Module().on_load(app)
        atexit.register(mdl.Module().on_shutdown, app)

        loaded_modules.append(mdl)

    return loaded_modules
