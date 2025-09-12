# Or tree columns go or tree page : 3 process
#-------------------------------------------------
# tree columns conveniently with breakdown process
# tree page conveniently work with 3 process
#
# one process get link
# two process open site, close site

from playwright.sync_api import sync_playwright

# def create_new_page(browser,url):
#     product_page = browser.new_page()
#     product_page.goto(url)
#     for element_page in product_page.query_selector_all("body div div div div article.product_page div.row div p.price_color"):
#         product_page.wait_for_timeout(300)
#         print(element_page.text_content())

# main Process
class PlayWrightManager:
    def __init__(self):
        print("Start project")

    def main_directory(self):
        pd = sync_playwright().start()

        website = pd.chromium.launch(headless=True)
        page = website.new_page()
        url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
        page.goto(url)
        page.screenshot(path = "example.png")
        website.close()


if __name__ == "__main__":
    init_class = PlayWrightManager()
    init_class.main_directory()


#     page_get_url = browser.new_page()
#     page_get_url.goto("https://books.toscrape.com/catalogue/category/books_1/index.html")
#
#     array_url = []
#     for page_text in page_get_url.query_selector_all("h3 a"):
#         array_url.append("".join(["https://books.toscrape.com/catalogue/",page_text.get_attribute("href").replace("../../","")]))
#
#     print(array_url,len(array_url))
#
#     page_get_url = browser.new_page()
#     # element wait url
#     if array_url == None:
#
#
#
#
#     browser.close()
#
# if __name__ == "__main__":
#     manager = PlaywrightManager()
#     manager.navigate_to('https://example.com')
#     print('Page Title:', manager.get_page_title())
#     manager.close()
#
