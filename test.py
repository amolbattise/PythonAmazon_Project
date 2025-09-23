import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def amazon_test():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 15)

    driver.get("https://www.Amazon.in/")

    try:

        # driver.get("https://www.Amazon.in/")


        search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        search_box.send_keys("Amazon Basics Laptop Bag" + Keys.ENTER)


        try:
            brand_checkbox = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[@aria-label='Apply the filter amazon basics to narrow results']//i[@class='a-icon a-icon-checkbox']")
            ))
            driver.execute_script("arguments[0].click();", brand_checkbox)
            print("Amazon Basics brand filter applied.")
            time.sleep(2)
        except:
            print("Brand filter not found, continuing...")


        product_elem = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(),'Laptop Bag Sleeve Case Cover')]")
        ))
        product_elem.click()
        driver.switch_to.window(driver.window_handles[-1])


        product_title_elem = wait.until(EC.presence_of_element_located((By.ID, "productTitle")))
        product_title = product_title_elem.text.strip()


        try:
            price_whole = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='a-price-whole']"))).text
            price_frac = driver.find_element(By.XPATH, "//span[@class='a-price-fraction']").text
            product_price = f"₹{price_whole}.{price_frac}"
        except:
            product_price = "Price not found"


        qty_dropdown = Select(wait.until(EC.presence_of_element_located((By.ID, "quantity"))))
        qty_values = [o.get_attribute("value") for o in qty_dropdown.options]
        random_qty = random.choice(qty_values)
        qty_dropdown.select_by_value(random_qty)
        print(f"Random quantity selected: {random_qty}")


        add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-button")))
        driver.execute_script("arguments[0].click();", add_to_cart_btn)
        time.sleep(2)


        print(f"Added product to cart:\nTitle: {product_title}\nPrice: {product_price}\nQuantity: {random_qty}")


        cart_count_elem = wait.until(EC.presence_of_element_located((By.ID, "nav-cart-count")))
        cart_count = int(cart_count_elem.text.strip())
        print("Cart count in Amazon:", cart_count)
        assert cart_count >= int(random_qty), "Cart count mismatch!"

    finally:
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    amazon_test()
