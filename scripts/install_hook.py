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

import os
from pathlib import Path

SCRIPT = r"""#!/bin/sh
set -o noglob

# Always keep the hook up-to-date
python3 scripts/install_hook.py || python scripts/install_hook.py

poetry run black .
poetry run isort .

files=$(git diff --cached --name-only)

if [ -n "$files" ]; then
    for file in $files; do
        if [ -f "$file" ]; then
            git add "$file"
        fi
    done
fi"""


def main() -> None:
    print("Installing pre-commit hook")
    with open(".git/hooks/pre-commit", "w") as f:
        f.write(SCRIPT)

    print(f"Installing dev dependencies (for black & isort)")
    os.system("poetry install --with dev")
    Path(".git/hooks/pre-commit").chmod(0o700)


if __name__ == "__main__":
    main()
