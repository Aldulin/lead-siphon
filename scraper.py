# scraper.py
import time
import pandas as pd
from playwright.sync_api import sync_playwright

def scrape_gmaps(query, max_results=20):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.google.com/maps")
        page.wait_for_timeout(3000)

        try:
            page.locator("button:has-text('Accept all')").click(timeout=3000)
        except:
            pass

        try:
            search_box = page.locator("input[role='combobox']").first
            search_box.wait_for(timeout=10000)
            search_box.fill(query)
            search_box.press("Enter")
        except:
            browser.close()
            return pd.DataFrame()

        page.wait_for_timeout(5000)

        results_panel = page.locator("div[role='feed']")
        results_panel.wait_for(timeout=10000)
        for _ in range(10):
            results_panel.evaluate("el => el.scrollBy(0, 1000)")
            time.sleep(1.5)

        listings = results_panel.locator("div[role='article']")
        count = listings.count()

        for i in range(min(count, max_results)):
            try:
                listings.nth(i).click()
                page.wait_for_timeout(3000)

                name = page.locator("h1").first.text_content() or ""
                phone = page.locator("button[aria-label*='Phone']").first.text_content() if page.locator("button[aria-label*='Phone']").count() else ""
                address = page.locator("button[aria-label*='Address']").first.text_content() if page.locator("button[aria-label*='Address']").count() else ""
                website = page.locator("a[aria-label*='Website']").first.get_attribute("href") if page.locator("a[aria-label*='Website']").count() else ""
                rating = page.locator("span[aria-label*='stars']").first.text_content() if page.locator("span[aria-label*='stars']").count() else ""

                results.append({
                    "Name": name.strip(),
                    "Phone": phone.strip(),
                    "Website": website.strip(),
                    "Address": address.strip(),
                    "Rating": rating.strip()
                })

                page.go_back()
                page.wait_for_timeout(2000)
            except:
                continue

        browser.close()
    return pd.DataFrame(results)
