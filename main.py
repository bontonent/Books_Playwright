# Or tree columns go or tree page : 3 process
#-------------------------------------------------
# tree columns conveniently with breakdown process
# tree page conveniently work with 3 process
#
# one process get link
# two process open site, close site
from playwright.sync_api import sync_playwright
import sys
import multiprocessing as mp
from tqdm import tqdm


class PlayWrightManager:
    def __init__(self,url):
            self.url = url
            self.last_url = None # Save last url where are we work
            self.base_url = [] # save all url, what don't work on it
            self.base_url_lost = [] # base_url if complete lost element
            self.process_work = ["",""] # process work at the moment with him
            self.we_still_work = True
            print("Start project")
            self.i = 0
#
    def main(self):

        task_q = mp.Queue()
        p1 = mp.Process(target=self.get_url_page, args = (self.url,task_q,))
        p2 = mp.Process(target=self.go_through_url,args = (task_q,))
        p3 = mp.Process(target=self.go_through_url,args = (task_q,))
        p1.start()
        p2.start()
        p3.start()

        p1.join()
        p2.join()
        p3.join()


    def go_through_url(self,task_q):
        with sync_playwright() as p_2:
            browser_product = p_2.chromium.launch(headless=True)
            process_one  = browser_product.new_page()
            while True:
                try:
                    self.base_url_lost.append(task_q.get(timeout=1))

                    self.base_url.append(task_q.get(timeout=1))
                    print(len(self.base_url))
                except Exception as e:
                    print(end="")
                if len(self.base_url_lost) != 0:
                    sys.stdout.write(f"\rUrl will need check {len(self.base_url_lost)}")
                    sys.stdout.flush()
                    if (len(self.base_url_lost) == 1000) | (len(self.base_url_lost) == 100) | (len(self.base_url_lost) == 10) | (len(self.base_url_lost) == 1):
                        print()

                    # add in process work
                    self.process_work[0] = self.base_url_lost[len(self.base_url_lost) - 1 - 1]
                    # remove from lost array
                    self.base_url_lost.pop(len(self.base_url_lost) - 1 - 1)

                    process_one.goto(self.process_work[0])
                    self.get_data_product_page(process_one)

                    # if complete good
                    self.process_work[0] = ""

                    # if complete bad
                    # self.base_url.append(self.process_work[0])
                    # self.process_work[0] = ""
                elif self.we_still_work == False:
                    break
                else:
                    process_one.wait_for_timeout(1000)

            browser_product.close()


# for work with product page
    def get_data_product_page(self,page_product):
        # clear all element
        title=None;genre=None;price=None;stock=None;stars=None;describe=None;
        img_url=None;UPC=None;Product_Type=None;Price_excl_tax=None;
        Price_incl_tax = None;Tax = None;Number_of_reviews = None
        # get all necessary data
        query_gen = page_product.query_selector_all("ul.breadcrumb li a")
        for index_gen,genre_el in enumerate(query_gen):
            if index_gen == 2:
                genre = genre_el.text_content()

        query_title = page_product.query_selector_all("div h1")
        for title_el in query_title:
            title = title_el.text_content()

        query_elements = page_product.query_selector_all("div.row div p")
        for index_e, right_elements in enumerate(query_elements):
            if index_e == 0:
                price = right_elements.text_content()
            if index_e == 1:
                stock = (right_elements.text_content()).replace("\n","").strip()
            if index_e == 2:
                stars = right_elements.get_attribute("class")

        query_describe = page_product.query_selector_all("article.product_page > p")
        for describe_el in query_describe:
            describe = describe_el.text_content()

        query_img = (page_product.query_selector_all("div.item.active img"))
        for img_el in query_img:
            img_url = ("".join(["https://books.toscrape.com/", (img_el.get_attribute('src')).replace("../../", "")]))

        query_table = page_product.query_selector_all("tbody")
        for table_el in query_table:
            query_table_th = table_el.query_selector_all("th")
            query_table_td = table_el.query_selector_all("td")
            for th_table_el,td_table_el in zip(query_table_th,query_table_td):
                if (th_table_el.text_content()) == "UPC":
                    UPC = td_table_el.text_content()
                if (th_table_el.text_content()) == "Product Type":
                    Product_Type = td_table_el.text_content()
                if (th_table_el.text_content()) == "Price (excl. tax)":
                    Price_excl_tax = td_table_el.text_content()
                if (th_table_el.text_content()) == "Price (incl. tax)":
                    Price_incl_tax = td_table_el.text_content()
                if (th_table_el.text_content()) == "Tax":
                    Tax = td_table_el.text_content()
                # I don't need in stock available, I had
                if (th_table_el.text_content()) == "Number of reviews":
                    Number_of_reviews = td_table_el.text_content()

        # Need in SQL
        for i in range(30):
            print("_",end='')
        print()
        print("Title: ",title)
        print("Product Type: ", Product_Type)
        print("Genre: ",genre)
        print("Price: ",price)
        print("In stock: ",stock)
        print("Stars: ",stars)
        print("UPC: ",UPC)
        print("Price excl tax: ",Price_excl_tax)
        print("Price incl tax: ",Price_incl_tax)
        print("Tax: ",Tax)
        print("Number of reviews: ",Number_of_reviews)
        print("Img url: ",img_url)
        print("Describe: ",describe)
# for work with catalog
    def get_url_page(self,url_def_1,task_q):
        with sync_playwright() as p:
            browser_catalog = p.chromium.launch(headless=True)
            page_catalog = browser_catalog.new_page()
            page_catalog.goto(url_def_1)
            still_work = True
            while (still_work):
                self.last_url = page_catalog.url
                print(page_catalog.url)
                query_page = page_catalog.query_selector_all("h3 a")
                for page_text in query_page:
                    element_queary_work = page_text.get_attribute("href")
                    add_url_in_base = "".join(["https://books.toscrape.com/catalogue/", element_queary_work.replace("../../", "")])
                    self.base_url.append(add_url_in_base)
                    self.base_url_lost.append(add_url_in_base)
                    task_q.put(add_url_in_base)

                still_work = self.next_page(page_catalog)
            browser_catalog.close()


    def next_page(self,page_catalog):
        # try click on new page
        try:
            query_next_page = page_catalog.query_selector_all("section div div ul li a[href]")
            for button_next_page in query_next_page:
                if (button_next_page.text_content()) == "next":
                    button_next_page.click()
                    page_catalog.wait_for_timeout(10) # don't need view png in the site/ for png 1000 need
                    return True
            # if don't find button, we can stop search new url element
            self.we_still_work = False
            return False
        except:
            self.we_still_work = False
            return False

def main ():
    if __name__ == "__main__":
        mp.set_start_method("spawn", force=True)
        # main url
        url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
        init_class = PlayWrightManager(url)
        init_class.main()
        print("End class")

main()