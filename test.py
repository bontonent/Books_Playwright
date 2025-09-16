# What say Duck AI how use multiprocessing & playwright using
import multiprocessing as mp
from playwright.sync_api import sync_playwright
import time

def catalog_worker(seed_url, task_q, hb_val, stop_ev):

    # I don't think. If we try will use this, we don't get error
    # but need try
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(seed_url)
        while not stop_ev.is_set():
            hb_val.value = time.time()
            elems = page.query_selector_all("h3 a")
            for e in elems:
                href = e.get_attribute("href")
                task_q.put("https://books.toscrape.com/catalogue/" + href.replace("../../", ""))
            nexts = page.query_selector_all("li.next a")
            if nexts:
                nexts[0].click()
                page.wait_for_timeout(300)
            else:
                break
        browser.close()

def scraper_worker(task_q, hb_val, stop_ev):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        while not stop_ev.is_set():
            hb_val.value = time.time()
            try:
                url = task_q.get(timeout=1)
            except Exception:
                continue
            page.goto(url)
            title_el = page.query_selector("div h1")
            print(title_el.text_content().strip() if title_el else "<no-title>")
        browser.close()

if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)   # MUST be first thing in __main__
    SEED_URL = "https://books.toscrape.com/catalogue/category/books_1/index.html"

    # I use a lot of time self. and it is unnecessary
    # self. in process don't work
    task_q = mp.Queue()

    # need learn. Maybe cool element
    stop_events = [mp.Event() for _ in range(3)]

    # don't know what it is
    hb_vals = [mp.Value('d', 0.0) for _ in range(3)]

    # I have error. Maybe create inside playwright.
    # I think if create inside playwright I don't get error message
    p_catalog = mp.Process(target=catalog_worker, args=(SEED_URL, task_q, hb_vals[0], stop_events[0]))
    p_scr1 = mp.Process(target=scraper_worker, args=(task_q, hb_vals[1], stop_events[1]))
    p_scr2 = mp.Process(target=scraper_worker, args=(task_q, hb_vals[2], stop_events[2]))

    p_catalog.start(); p_scr1.start(); p_scr2.start()

    try:
        while any(p.is_alive() for p in (p_catalog, p_scr1, p_scr2)):
            time.sleep(1)
    except KeyboardInterrupt:
        for ev in stop_events: ev.set()
    finally:
        for p in (p_catalog, p_scr1, p_scr2):
            p.join(timeout=5)
            if p.is_alive(): p.terminate()
