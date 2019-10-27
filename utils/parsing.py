import bs4

def fetch_images_urls(html):
    parser = bs4.BeautifulSoup(html, "lxml")
    img_pattern = {"class": "preview"}
    
    return [img_url["src"] for img_url in parser.find_all("img", img_pattern)]