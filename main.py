# Or tree columns go or tree page : 3 process
#-------------------------------------------------
# tree columns conveniently with breakdown process
# tree page conveniently work with 3 process
#
# one process get link
# two process open site, close site
import asyncio
from playwright.async_api import async_playwright
import sys
from tqdm import tqdm


# main Process
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
    async def main(self):
        #necessary element
        pd = await async_playwright().start()
        website = await pd.chromium.launch(headless=True)

        # First process
        # Work with catalog
        page_catalog = await website.new_page() # first process
        process_second = await website.new_page() # second process
        process_third = await website.new_page() # third process

        await page_catalog.goto(self.url)
        # It is bad decision. I know. But It is work systems.
        # better use "multiprocessing"
        while True:
            try:
                await asyncio.gather(
                    self.get_url_page(page_catalog)
                    , self.go_through_url(process_second)
                    , self.go_through_url(process_third)
                )
            except Exception as e:
                await page_catalog.close()
                await process_second.close()
                await process_third.close()
                process_second = await website.new_page()
                process_third = await website.new_page()
                page_catalog = await website.new_page()
                await page_catalog.goto(self.last_url)
            if len(self.base_url_lost) == 0:
                break

        await website.close()

    async def go_through_url(self,process_one):
        while True:
            if len(self.base_url_lost) != 0:
                sys.stdout.write(f"\rUrl will need check {len(self.base_url_lost)}")
                sys.stdout.flush()
                if (len(self.base_url_lost) == 1000) | (len(self.base_url_lost) == 100) | (len(self.base_url_lost) == 10) | (len(self.base_url_lost) == 1):
                    print()

                # add in process work
                self.process_work[0] = self.base_url_lost[len(self.base_url_lost) - 1 - 1]
                # remove from lost array
                self.base_url_lost.pop(len(self.base_url_lost) - 1 - 1)

                await process_one.goto(self.process_work[0])
                await self.get_data_product_page(process_one)

                # if complete good
                self.process_work[0] = ""

                # if complete bad
                # self.base_url.append(self.process_work[0])
                # self.process_work[0] = ""
            elif self.we_still_work == False:
                break
            else:
                await process_one.wait_for_timeout(1000)

        await process_one.close()


# for work with product page
    async def get_data_product_page(self,page_product):
        # get all necessary data
        query_gen = await page_product.query_selector_all("ul.breadcrumb li a")
        for index_gen,genre_el in enumerate(query_gen):
            if index_gen == 2:
                genre = await genre_el.text_content()

        query_title = await page_product.query_selector_all("div h1")
        for title_el in query_title:
            title = await title_el.text_content()

        query_elements = await page_product.query_selector_all("div.row div p")
        for index_e, right_elements in enumerate(query_elements):
            if index_e == 0:
                price = await right_elements.text_content()
            if index_e == 1:
                stock = (await right_elements.text_content()).replace("\n","").strip()
            if index_e == 2:
                stars = await right_elements.get_attribute("class")

        query_describe = await page_product.query_selector_all("article.product_page > p")
        for describe_el in query_describe:
            describe = await describe_el.text_content()

        query_img = (await page_product.query_selector_all("div.item.active img"))
        for img_el in query_img:
            img_url = ("".join(["https://books.toscrape.com/", (await img_el.get_attribute('src')).replace("../../", "")]))

        query_table = await page_product.query_selector_all("tbody")
        for table_el in query_table:
            query_table_th = await table_el.query_selector_all("th")
            query_table_td = await table_el.query_selector_all("td")
            for th_table_el,td_table_el in zip(query_table_th,query_table_td):
                if (await th_table_el.text_content()) == "UPC":
                    UPC = await td_table_el.text_content()
                if (await th_table_el.text_content()) == "Product Type":
                    Product_Type = await td_table_el.text_content()
                if (await th_table_el.text_content()) == "Price (excl. tax)":
                    Price_excl_tax = await td_table_el.text_content()
                if (await th_table_el.text_content()) == "Price (incl. tax)":
                    Price_incl_tax = await td_table_el.text_content()
                if (await th_table_el.text_content()) == "Tax":
                    Tax = await td_table_el.text_content()
                # I don't need in stock available, I had
                if (await th_table_el.text_content()) == "Number of reviews":
                    Number_of_reviews = await td_table_el.text_content()

        # Need in SQL
        # print(title)
        # print(genre)
        # print(price)
        # print(stock)
        # print(stars)
        # print(describe)
        # print(img_url)
        # print(UPC)
        # print(Product_Type)
        # print(Price_excl_tax)
        # print(Price_incl_tax)
        # print(Tax)
        # print(Number_of_reviews)
# for work with catalog
    async def get_url_page(self,page_catalog):
        still_work = True
        while (still_work):
            self.last_url = page_catalog.url
            query_page = await page_catalog.query_selector_all("h3 a")
            for page_text in query_page:
                element_queary_work = await page_text.get_attribute("href")
                add_url_in_base = "".join(["https://books.toscrape.com/catalogue/", element_queary_work.replace("../../", "")])
                self.base_url.append(add_url_in_base)
                self.base_url_lost.append(add_url_in_base)
            still_work = await self.next_page(page_catalog)

    async def next_page(self,page_catalog):
        # try click on new page
        try:
            query_next_page = await page_catalog.query_selector_all("section div div ul li a[href]")
            for button_next_page in query_next_page:
                if (await button_next_page.text_content()) == "next":
                    await button_next_page.click()
                    await page_catalog.wait_for_timeout(10) # don't need view png in the site/ for png 1000 need
                    return True
            # if don't find button, we can stop search new url element
            self.we_still_work = False
            return False
        except:
            self.we_still_work = False
            return False

async def asmain ():
    if __name__ == "__main__":
        url = "https://books.toscrape.com/catalogue/category/books_1/index.html"
        init_class = PlayWrightManager(url)
        await init_class.main()
        print("End class")

asyncio.run(asmain())

