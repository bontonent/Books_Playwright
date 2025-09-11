from playwright.sync_api import sync_playwright

# def create_new_page(browser,url):
#     product_page = browser.new_page()
#     product_page.goto(url)
#     for element_page in product_page.query_selector_all("body div div div div article.product_page div.row div p.price_color"):
#         product_page.wait_for_timeout(300)
#         print(element_page.text_content())

with sync_playwright() as p:

    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://books.toscrape.com/catalogue/category/books_1/index.html")
    page.query_selector("h3 a").click()
    page.wait_for_timeout(10)
    for page_element in page.query_selector_all("body div div div div article.product_page div.row div p.price_color"):
        print(page_element.text_content())
    # for page_text in page.query_selector_all("h3 a"):
    #     new_url = "".join(["https://books.toscrape.com/catalogue/",page_text.get_attribute("href").replace("../../","")])

        # create_new_page(browser,new_url)

    browser.close()

