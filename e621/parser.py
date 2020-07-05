import asyncio
from bs4 import BeautifulSoup


class E621Parser:
    @staticmethod
    async def get_images_pages_url(html):
        def _get_images_pages_sync():
            images_pages = []
            parser = BeautifulSoup(html, "lxml")

            for link in parser.find_all("a"):
                if link["href"].startswith("/posts/"):
                    images_pages.append(f"https://e621.net{link['href']}")

            return images_pages

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _get_images_pages_sync)

    @staticmethod
    async def get_image_url_from_its_page(html):
        def _get_image_from_its_page_sync():
            parser = BeautifulSoup(html, "lxml")
            img = parser.find("img", {"id": "image"})

            return img["src"]

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _get_image_from_its_page_sync)
