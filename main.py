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
    def __init__(self,url):
        self.url = url
        self.base_url = [] # save all url, what don't work on it
        print("Start project")
        self.i = 0

    def main(self):
        pd = sync_playwright().start()

        website = pd.chromium.launch(headless=True)
        page = website.new_page()
        page.goto(self.url)
        self.get_url_page(page)
        print(self.base_url)
        print(len(self.base_url))
        website.close()

    def get_url_page(self,page):

        still_work = True
        while (still_work):
            for page_text in page.query_selector_all("h3 a"):
                self.base_url.append("".join(["https://books.toscrape.com/catalogue/",page_text.get_attribute("href").replace("../../","")]))

            still_work = self.next_page(page)
            # print(still_work)

    def next_page(self,page):
        # try click on new page
        try:
            for button_next_page in page.query_selector_all("section div div ul li a[href]"):
                # print(button_next_page.text_content())
                if button_next_page.text_content() == "next":
                    self.i = self.i + 1
                    print(self.i)
                    button_next_page.click()
                    page.wait_for_timeout(10) # don't need view png in the site/ for png 1000 need
                    return True
            return False
        except:
            return False

if __name__ == "__main__":
    url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
    init_class = PlayWrightManager(url)
    init_class.main()

    print("End class")


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
# if __name__ == "__main__":
#     manager = PlaywrightManager()
#     manager.navigate_to('https://example.com')
#     print('Page Title:', manager.get_page_title())
#     manager.close()
#
