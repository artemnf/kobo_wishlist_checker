from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re

print('Starting parsing')

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9230/devtools/browser/b1131b67-6b3b-4298-8114-761abe87eee0")
driver = webdriver.Chrome(options=chrome_options)

end_reached = False
page_number = 1
item_number = 0
threshold = 3.0
was_price_threshold = 3.0
price_found = False

driver.get('https://www.kobo.com/ca/en/account/wishlist')

results = dict()
not_found_links = dict()
not_available_links = dict()

while(end_reached == False):
    xpath = "//button[@class='page-link active reveal' and @aria-label='Page Number {page_number}']".format(page_number = page_number)
    #print(xpath)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))

    items = driver.find_elements("xpath", "//li[@class='wishlist-item']")

    for item in items:
        
        price_found = False

        #link = item.find_element("xpath", "div/a[@class='item-link-underlay']")
        link = item.find_element("xpath", "div[@class='image-and-info-container']/div[@class='item-info']/h2[@class='title']/a[@class='heading-link']")
        link_href = link.get_attribute('href')

        normal_prices = item.find_elements("xpath", "div[@class='product-actions']/div[@class='product-price-container']/p[@class='price']")

        for price in normal_prices:
            priceTx = price.get_attribute('innerText')

            priceNum = float(re.search("\$([0-9\.]+)", priceTx).group(1))

            if priceNum < threshold:
                results[link_href] = priceTx
                print('Price: {priceTx}                 {link}'.format(priceTx = priceTx, link = link_href))

            item_number = item_number + 1
            price_found = True

        sale_prices = item.find_elements("xpath", "div[@class='product-actions']/div[@class='product-price-container']/div[@class='sale-price-container']")

        for sale_price in sale_prices:
            was_price = sale_price.find_element("xpath", "span[@class='was-price']").get_attribute('innerText')
            sale_price = sale_price.find_element("xpath", "span[@class='sale-price']").get_attribute('innerText')

            priceNum = float(re.search("\$([0-9\.]+)", sale_price).group(1))
            was_price_num = float(re.search("\$([0-9\.]+)", was_price).group(1))

            if priceNum < threshold or  priceNum < was_price_threshold and was_price_num >= was_price_threshold:
                results[link] = sale_price
                print('Was price: {was_price}; Sale price: {sale_price}   {link}'.format(was_price = was_price, sale_price = sale_price, link = link_href))

            item_number = item_number + 1
            price_found = True

        if not price_found:
            not_found_links[link_href] = page_number
            #print('Price not found for link {link} on page {page}'.format(link = link_href, page = page_number))

    next = driver.find_element("xpath", "//button[@aria-label='Next']")

    #print('Processed page {page_num}'.format(page_num = page_number))

    if next.get_attribute('class') == 'next':
        page_number = page_number + 1
        next.click()
    else:
        end_reached = True

for i, (link, page_num) in enumerate(not_found_links.items()):

    price_found = False

    driver.get(link)

    pricing_xpath = "//div[@class='pricing-details']"

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, pricing_xpath)))

    except TimeoutException:
        print('Could not load book (might be not found) for link {link} on page {page_num}'.format(link = link, page_num = page_num)) 
        continue

    prices = driver.find_elements("xpath", "//div[@class='pricing-figures']/div[@class='active-price']/div[@class='price-wrapper']/span[@class='price']")

    for price in prices:
        priceTx = price.get_attribute('innerText')

        priceNum = float(re.search("\$([0-9\.]+)", priceTx).group(1))

        if priceNum < threshold:
            #results[link_href] = priceTx
            print('Price: {priceTx}                 {link_href}'.format(priceTx = priceTx, link = link_href))

        item_number = item_number + 1
        price_found = True

    if not price_found:
        #try to find 'not available'
        unavailable = driver.find_element("xpath", "//div[@class='country-stores-availability message-box error']/p[starts-with(., 'Unavailable in')]")

        if unavailable:
            not_available_links[link] = page_num
            #print(unavailable.get_attribute('innerText'))
        else:
            print('Price not found for link {link} on page {page_num}'.format(link = link, page_num = page_num))    

print('Read {page_num} pages and {item_number} items'.format(page_num = page_number, item_number = item_number))

#british
end_reached = False
page_number = 1
item_number = 0
threshold = 2.0
was_price_threshold = 2.0
price_found = False

driver.get('https://www.kobo.com/gb/en/account/wishlist')

while(end_reached == False):
    xpath = "//button[@class='page-link active reveal' and @aria-label='Page Number {page_number}']".format(page_number = page_number)
    #print(xpath)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))

    items = driver.find_elements("xpath", "//li[@class='wishlist-item']")

    for item in items:
        
        price_found = False

        #link = item.find_element("xpath", "div/a[@class='item-link-underlay']")
        link = item.find_element("xpath", "div[@class='image-and-info-container']/div[@class='item-info']/h2[@class='title']/a[@class='heading-link']")
        link_href = link.get_attribute('href')

        normal_prices = item.find_elements("xpath", "div[@class='product-actions']/div[@class='product-price-container']/p[@class='price']")

        for price in normal_prices:
            priceTx = price.get_attribute('innerText')

            priceNum = float(re.search("\£([0-9\.]+)", priceTx).group(1))

            if priceNum < threshold:
                results[link_href] = priceTx
                print('Price: {priceTx}                 {link}'.format(priceTx = priceTx, link = link_href))

            item_number = item_number + 1
            price_found = True

        sale_prices = item.find_elements("xpath", "div[@class='product-actions']/div[@class='product-price-container']/div[@class='sale-price-container']")

        for sale_price in sale_prices:
            was_price = sale_price.find_element("xpath", "span[@class='was-price']").get_attribute('innerText')
            sale_price = sale_price.find_element("xpath", "span[@class='sale-price']").get_attribute('innerText')

            priceNum = float(re.search("\£([0-9\.]+)", sale_price).group(1))
            was_price_num = float(re.search("\£([0-9\.]+)", was_price).group(1))

            if priceNum < threshold or  priceNum < was_price_threshold and was_price_num >= was_price_threshold:
                results[link] = sale_price
                print('Was price: {was_price}; Sale price: {sale_price}   {link}'.format(was_price = was_price, sale_price = sale_price, link = link_href))

            item_number = item_number + 1
            price_found = True

    next = driver.find_element("xpath", "//button[@aria-label='Next']")

    #print('Processed page {page_num}'.format(page_num = page_number))

    if next.get_attribute('class') == 'next':
        page_number = page_number + 1
        next.click()
    else:
        end_reached = True
print('Read {page_num} pages and {item_number} items'.format(page_num = page_number, item_number = item_number))


driver.quit()