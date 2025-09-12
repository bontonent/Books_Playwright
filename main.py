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
        #necessary element
        pd = sync_playwright().start()
        website = pd.chromium.launch(headless=True)

        # uncomment for use get url
        # # Work with catalog
        # page_catalog = website.new_page()
        # page_catalog.goto(self.url)
        # self.get_url_page(page_catalog)

        #Start work with product page
        page_product = website.new_page()
        # I don't know how
        # wait new url element

        # for one_url in self.base_url:
        one_url = 'https://books.toscrape.com/catalogue/1000-places-to-see-before-you-die_1/index.html'
        page_product.goto(one_url)
        self.get_data_product_page(page_product)

        # uncomment for use get url
        # print(self.base_url)
        # print(len(self.base_url))
        website.close()

# for work with product page
    def get_data_product_page(self,page_product):
        # get all necessary data
        for index_gen,genre_el in enumerate(page_product.query_selector_all("ul.breadcrumb li a")):
            if index_gen == 2:
                genre = genre_el.text_content()
        for title_el in page_product.query_selector_all("div h1"):
            title = title_el.text_content()
        for index_e, right_elements in enumerate(page_product.query_selector_all("div.row div p")):
            if index_e == 0:
                price = right_elements.text_content()
            if index_e == 1:
                stock = right_elements.text_content().replace("\n","").strip()
            if index_e == 2:
                stars = right_elements.get_attribute("class")
        for describe_el in page_product.query_selector_all("article.product_page > p"):
            describe = describe_el.text_content()
        for img_el in page_product.query_selector_all("div.item.active img"):
            img_url = "".join(["https://books.toscrape.com/",img_el.get_attribute('src').replace("../../","")])
        for table_el in page_product.query_selector_all("tbody"):
            for th_table_el,td_table_el in zip(table_el.query_selector_all("th"),table_el.query_selector_all("td")):
                if th_table_el.text_content() == "UPC":
                    UPC = td_table_el.text_content()
                if th_table_el.text_content() == "Product Type":
                    Product_Type = td_table_el.text_content()
                if th_table_el.text_content() == "Price (excl. tax)":
                    Price_excl_tax = td_table_el.text_content()
                if th_table_el.text_content() == "Price (incl. tax)":
                    Price_incl_tax = td_table_el.text_content()
                if th_table_el.text_content() == "Tax":
                    Tax = td_table_el.text_content()
                # I don't need in stock available, I had
                if th_table_el.text_content() == "Number of reviews":
                    Number_of_reviews = td_table_el.text_content()

# for work with catalog
    def get_url_page(self,page_catalog):
        still_work = True
        while (still_work):
            for page_text in page_catalog.query_selector_all("h3 a"):
                self.base_url.append("".join(["https://books.toscrape.com/catalogue/",page_text.get_attribute("href").replace("../../","")]))
            still_work = self.next_page(page_catalog)
            # print(still_work)
    def next_page(self,page_catalog):
        # try click on new page
        try:
            for button_next_page in page_catalog.query_selector_all("section div div ul li a[href]"):
                # print(button_next_page.text_content())
                if button_next_page.text_content() == "next":
                    self.i = self.i + 1
                    print(self.i)
                    button_next_page.click()
                    page_catalog.wait_for_timeout(10) # don't need view png in the site/ for png 1000 need
                    return True
            # if don't find button, we can stop search new url element
            return False
        except:
            return False

if __name__ == "__main__":
    url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
    init_class = PlayWrightManager(url)
    init_class.main()

    print("End class")
