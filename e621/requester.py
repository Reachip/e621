import aiohttp


class E621Requester:
    async def __aenter__(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
        }
        connector = aiohttp.TCPConnector(ssl=False, limit=0)
        self._session = aiohttp.ClientSession(headers=headers, connector=connector)

        return self

    async def __aexit__(self, *err):
        await self._session.close()

    async def get_category_page(self, category):
        return await self.get_html(category)

    async def get_raw_image(self, url):
        async with self._session.get(url) as resp:
            return await resp.read()

    async def get_html(self, url):
        async with self._session.get(url) as resp:
            return await resp.text()
