import argparse
import asyncio

from e621.category import E621Category
from e621.image.image_writer import ImageWriter


class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Fast E621 image downloader")
        parser.add_argument("category", type=str, help="image categorie")
        parser.add_argument("page", type=int, help="number of pages to scrape")
        self.args = parser.parse_args()

    async def page_handler(self, page):
        category = E621Category(self.args.category, page=page)

        async for image in category.get_images():
            writer = ImageWriter()

            try:
                await writer.write_image(image)

            except TypeError:
                # Caused by a border effect.
                # It return sometime a incorrect URL.
                pass

    async def async_runner(self):
        page_handlers = [self.page_handler(page) for page in range(1, self.args.page)]
        await asyncio.gather(*page_handlers)

    def run(self):
        asyncio.run(self.async_runner())
