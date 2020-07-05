from e621.requester import E621Requester
from e621.parser import E621Parser
from e621.image.image import Image


class E621Category:
    def __init__(self, categorie_name, page=1):
        self.url = f"https://e621.net/posts?page={page}&tags={categorie_name}"
        self.parser = E621Parser()

    async def get_images(self):
        async with E621Requester() as requester:
            categorie_page = await requester.get_category_page(self.url)
            image_pages_url = await self.parser.get_images_pages_url(categorie_page)

            for image_page_url in image_pages_url:
                image_page = await requester.get_html(image_page_url)

                yield Image(image_page)
