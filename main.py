# parse
from playwright.sync_api import sync_playwright
import sys

# Processing work
import multiprocessing as mp

# short break
import time

# if Error_message, don't necessary
import traceback


class PlayWrightManager:
    def __init__(self,url):
        print("Start project")

        # Url product
        self.url = url
        self.we_still_work = True

        # Count cycle
        self.i = 0

        # Don't use, but if after maybe need update multiprocessing control
        self.last_url = None  # Save last url where are we work
        self.process_work = ["", ""]  # process work at the moment with him

    # Main round
    def main(self):
        # call from process 1 to process 2 and process 2
        task_q = mp.Queue()

        # Create process
        process_1 = mp.Process(target=self.get_url_page, args = (self.url,task_q,))
        process_2 = mp.Process(target=self.go_through_url,args = (task_q,"First",))
        process_3 = mp.Process(target=self.go_through_url,args = (task_q,"Second",))

        # Start
        process_1.start()
        process_2.start()
        process_3.start()

        # Wait end
        process_1.join()
        process_2.join()
        process_3.join()

    # Get all necessary data
    def go_through_url(self,task_q,text):
        # init website
        with sync_playwright() as p_2:
            browser_product = p_2.chromium.launch(headless=True)
            process_one  = browser_product.new_page()

            # index element raad
            self.i = 0

            # Cycle don't stop if don't stop 'Process 1'
            while True:
                try:
                    self.i = 1 + self.i
                    sys.stdout.write(f"\rChecked url {text} {self.i}")
                    sys.stdout.flush()

                    # Get ulr from 'Process 1'
                    name_get = task_q.get()
                    if name_get == 'stop':
                        break

                    # Send url
                    process_one.goto(name_get)
                    self.get_data_product_page(process_one)

                except Exception:
                    print(traceback.format_exc())
                    time.sleep(1)

            # end
            browser_product.close()


    # For work with product page
    def get_data_product_page(self,page_product):

        # Clear all element
        title=None;genre=None;price=None;stock=None;stars=None;describe=None;
        img_url=None;UPC=None;Product_Type=None;Price_excl_tax=None;
        Price_incl_tax = None;Tax = None;Number_of_reviews = None

        # Get genre
        query_gen = page_product.query_selector_all("ul.breadcrumb li a")
        for index_gen,genre_el in enumerate(query_gen):
            if index_gen == 2:
                genre = genre_el.text_content()

        # Get title
        query_title = page_product.query_selector_all("div h1")
        for title_el in query_title:
            title = title_el.text_content()

        # Get price, in stock, how much Stars
        query_elements = page_product.query_selector_all("div.row div p")
        for index_e, right_elements in enumerate(query_elements):
            if index_e == 0:
                price = right_elements.text_content()
            if index_e == 1:
                stock = (right_elements.text_content()).replace("\n","").strip()
            if index_e == 2:
                stars = right_elements.get_attribute("class")

        # Get description
        query_describe = page_product.query_selector_all("article.product_page > p")
        for describe_el in query_describe:
            describe = describe_el.text_content()

        # Get img
        query_img = (page_product.query_selector_all("div.item.active img"))
        for img_el in query_img:
            img_url = ("".join(["https://books.toscrape.com/", (img_el.get_attribute('src')).replace("../../", "")]))

        # Get table data
        query_table = page_product.query_selector_all("tbody")
        for table_el in query_table:
            query_table_th = table_el.query_selector_all("th")
            query_table_td = table_el.query_selector_all("td")

            for th_table_el,td_table_el in zip(query_table_th,query_table_td):
                # UPC
                if (th_table_el.text_content()) == "UPC":
                    UPC = td_table_el.text_content()

                # Product Type
                if (th_table_el.text_content()) == "Product Type":
                    Product_Type = td_table_el.text_content()

                # Price excl tax
                if (th_table_el.text_content()) == "Price (excl. tax)":
                    Price_excl_tax = td_table_el.text_content()

                # Price incl tax
                if (th_table_el.text_content()) == "Price (incl. tax)":
                    Price_incl_tax = td_table_el.text_content()

                # Tax
                if (th_table_el.text_content()) == "Tax":
                    Tax = td_table_el.text_content()

                # Number of reviews
                if (th_table_el.text_content()) == "Number of reviews":
                    Number_of_reviews = td_table_el.text_content()

                # I don't need in stock available, I had (in table have second 'in stock')

        # All data
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

    # For work with page catalog. Get name products
    def get_url_page(self,url_def_1,task_q):

        # Init Web-site
        with sync_playwright() as p:
            browser_catalog = p.chromium.launch(headless=True)
            page_catalog = browser_catalog.new_page()

            # Open main url
            page_catalog.goto(url_def_1)

            # Init get data
            still_work = True
            while (still_work):
                # where are we at the moment?
                print(page_catalog.url)

                # Get data products
                query_page = page_catalog.query_selector_all("h3 a")
                for page_text in query_page:
                    element_queary_work = page_text.get_attribute("href")

                    # Create url products,
                    add_url_in_base = "".join(["https://books.toscrape.com/catalogue/", element_queary_work.replace("../../", "")])

                    # Sent to process 1 or process 2
                    task_q.put(add_url_in_base)

                # Check, have next page?
                still_work = self.next_page(page_catalog)

            # If don't have page, send end element stop for two process
            # !!! 2 sent to 2 process, for 3 process need 3 send.
            task_q.put('stop')
            task_q.put('stop')

            # end
            browser_catalog.close()

    # Next page
    def next_page(self,page_catalog):

        #If save from miss error
        while True:
            try:
                # Get data, can or can't click()
                query_next_page = page_catalog.query_selector_all("section div div ul li a[href]")
                for button_next_page in query_next_page:
                    if (button_next_page.text_content()) == "next":
                        button_next_page.click()
                        page_catalog.wait_for_timeout(10) # don't need view png in the site/ for png 1000 need
                        return True

                # if don't find button, we can stop search new url element
                self.we_still_work = False
                return self.we_still_work

            except Exception:
                print(traceback.print_exc())
                time.sleep(1)
                self.we_still_work = False
                return self.we_still_work


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)

    # Start work with class
    url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
    init_class = PlayWrightManager(url)
    init_class.main()

    print("End class")
