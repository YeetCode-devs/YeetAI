# Commands implementation guide

* [File placement](#file-placement)
* [Implementation](#implementation)

## File placement
1. It can be placed either directly under this folder, OR
1. Under any subfolder inside this folder (so-called category)

## Implementation
To ensure the command file is properly loaded by the module
loader, all commands must define the following `data` dictionary:
```python

from pyrogram.client import Client
from pyrogram.types import Message


# Note the function parameter signature!
def execute(app: Client, message: Message) -> None:
    pass


# This dictionary is important, the loader will look for
# this, if not found then it will not be loaded.
data = {
    "name": "start",
    "description": "Starts the bot.",
    # "alias": ["on"], # Optional
    "usage": "/start",
    "example": "/start",
    "category": "Core",
    "execute": execute,
}
```
