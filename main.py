import asyncio
import os
import time
import sys
import logging
from uuid import uuid4
from concurrent.futures import ProcessPoolExecutor

import aiohttp
import aiofiles

from utils.parsing import fetch_images_urls

logging.basicConfig(
    filename="log", format="%(threadName)s %(asctime)s %(message)s", level=logging.DEBUG
)


async def get_html_source(categorie, index):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
    }

    url = f"https://e621.net/post/index/{index}/{categorie}"

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.text()


async def get_image(url, executor):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            logging.info(f"[{url}] DOWNLOADED")
            await write_image(resp, executor)


def make_image_path():
    cwd = os.getcwd()

    dir_path = f"{cwd}/e621"
    folder_exist = os.path.exists(dir_path)

    if not folder_exist:
        os.makedirs(dir_path)

    image_id = uuid4().hex
    logging.info("Retuning the path of the new image")
    return f"{dir_path}/{image_id}.jpg"


async def write_image(http_response, executor):
    image_path = await asyncio.get_running_loop().run_in_executor(
        executor, make_image_path
    )

    async with aiofiles.open(image_path, "wb") as f:
        while True:
            chunk = await http_response.content.read(10)

            if not chunk:
                logging.info(f"[{image_path}] WRITTEN")
                break

            await f.write(chunk)


async def get_image_from_categorie(categorie, index, executor):
    html = await get_html_source(categorie, index)
    image_urls = await asyncio.get_running_loop().run_in_executor(
        executor, fetch_images_urls, html
    )

    for image_url in image_urls:
        await get_image(image_url, executor)
        await asyncio.sleep(1)


async def main(categorie, executor):
    logging.info("SCRIPT RUNNING")
    tasks = (
        get_image_from_categorie(categorie, index, executor) for index in range(750)
    )
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=int(sys.argv[2])) as executor:
        asyncio.run(main(sys.argv[1], executor))
