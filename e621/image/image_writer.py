from pathlib import Path
import asyncio
from uuid import uuid4
import os

import aiofiles


class ImageWriter:
    def __init__(self, path=Path.home()):
        self.path = str(path) + "/e621/"

        if not os.path.exists(path):
            os.mkdir(path)

    async def _get_complet_path(self):
        loop = asyncio.get_event_loop()
        uuid = await loop.run_in_executor(None, uuid4)

        return str(self.path) + str(uuid) + ".jpg"

    async def write_image(self, image):
        complet_path = await self._get_complet_path()

        async with aiofiles.open(complet_path, "wb") as _file:
            await _file.write(await image.get_image())
