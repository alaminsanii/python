from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()  # or webdriver.Firefox()
driver.get("https://google.com")

n = input("Press Enter after focusing on the search box...")
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys({n} + Keys.RETURN)

input("Press Enter to close the browser...")
driver.quit()
