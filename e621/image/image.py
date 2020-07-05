from e621.parser import E621Parser
from e621.requester import E621Requester


class Image:
    def __init__(self, image_page):
        self.image_page = image_page

    async def get_image(self):
        image_url = await E621Parser().get_image_url_from_its_page(self.image_page)

        async with E621Requester() as requester:
            return await requester.get_raw_image(image_url)
