import asyncio
from playwright.async_api import async_playwright

HEADLESS = True  # Set False if you want to see browser

async def scrape_amazon(page, product_name):
    url = f"https://www.amazon.ae/s?k={product_name.replace(' ', '+')}"
    await page.goto(url)
    await page.wait_for_selector('div[data-component-type="s-search-result"]')
    
    products = await page.query_selector_all('div[data-component-type="s-search-result"]')
    results = []
    for product in products[:5]:
        title = await product.query_selector_eval('h2 a span', 'el => el.textContent')        
        price_whole = await product.query_selector_eval('span.a-price-whole', 'el => el.textContent', strict=False)
        price_frac = await product.query_selector_eval('span.a-price-fraction', 'el => el.textContent', strict=False)
        if price_whole:
            price = price_whole.strip() + (price_frac.strip() if price_frac else '')
        else:
            price = "N/A"
        results.append({"store": "Amazon.ae", "title": title.strip(), "price": price})
    return results

async def scrape_noon(page, product_name):
    url = f"https://www.noon.com/uae-en/search?q={product_name.replace(' ', '%20')}"
    await page.goto(url)
    await page.wait_for_selector('div.productContainer')
    
    products = await page.query_selector_all('div.productContainer')
    results = []
    for product in products[:5]:
        title = await product.query_selector_eval('h2', 'el => el.textContent', strict=False)
        price = await product.query_selector_eval('span.price', 'el => el.textContent', strict=False)
        if title:
            results.append({"store": "Noon", "title": title.strip(), "price": price.strip() if price else "N/A"})
    return results

async def scrape_aliexpress(page, product_name):
    url = f"https://www.aliexpress.com/wholesale?SearchText={product_name.replace(' ', '+')}"
    await page.goto(url)
    await page.wait_for_selector('.list-item')
    
    products = await page.query_selector_all('.list-item')
    results = []
    for product in products[:5]:
        title = await product.query_selector_eval('.item-title', 'el => el.textContent', strict=False)
        price = await product.query_selector_eval('.price-current', 'el => el.textContent', strict=False)
        if title:
            results.append({"store": "AliExpress", "title": title.strip(), "price": price.strip() if price else "N/A"})
    return results

async def scrape_shein(page, product_name):
    url = f"https://www.shein.com/search?keyword={product_name.replace(' ', '%20')}"
    await page.goto(url)
    await page.wait_for_selector('div.S-product-item')
    
    products = await page.query_selector_all('div.S-product-item')
    results = []
    for product in products[:5]:
        title = await product.query_selector_eval('a.S-product-item__link', 'el => el.getAttribute("title")', strict=False)
        price = await product.query_selector_eval('span.S-product-item__price', 'el => el.textContent', strict=False)
        if title:
            results.append({"store": "Shein", "title": title.strip(), "price": price.strip() if price else "N/A"})
    return results

async def main(product_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS)
        page = await browser.new_page()
        
        all_results = []

        # Scrape Amazon
        try:
            print("Scraping Amazon...")
            amazon_results = await scrape_amazon(page, product_name)
            all_results.extend(amazon_results)
        except Exception as e:
            print(f"Amazon scrape error: {e}")

        # Scrape Noon
        try:
            print("Scraping Noon...")
            noon_results = await scrape_noon(page, product_name)
            all_results.extend(noon_results)
        except Exception as e:
            print(f"Noon scrape error: {e}")

        # Scrape AliExpress
        try:
            print("Scraping AliExpress...")
            aliexpress_results = await scrape_aliexpress(page, product_name)
            all_results.extend(aliexpress_results)
        except Exception as e:
            print(f"AliExpress scrape error: {e}")

        # Scrape Shein
        try:
            print("Scraping Shein...")
            shein_results = await scrape_shein(page, product_name)
            all_results.extend(shein_results)
        except Exception as e:
            print(f"Shein scrape error: {e}")

        await browser.close()

        # Print results
        print("\n--- Search Results ---\n")
        if all_results:
            for idx, r in enumerate(all_results, 1):
                print(f"{idx}. [{r['store']}] {r['title']} — {r['price']}")
        else:
            print("No results found.")

if __name__ == "__main__":
    product = input("Enter product name to search: ")
    asyncio.run(main(product))
