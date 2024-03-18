import os

from pathlib import Path

SCRIPT = r"""#!/bin/sh
set -o noglob

python3 scripts/install_hook.py

poetry run black .

for file in $(git diff --cached --name-only); do
    test -f $file && git add $file
done"""


def main() -> None:
    print("Installing pre-commit hook")
    with open(".git/hooks/pre-commit", "w") as f:
        f.write(SCRIPT)

    print(f"Installing dev dependencies (for black)")
    os.system("poetry install --with dev")
    Path(".git/hooks/pre-commit").chmod(0o700)


main()