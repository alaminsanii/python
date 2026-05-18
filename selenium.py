import keyboard
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException
)

# -----------------------------
# INIT BROWSER
# -----------------------------
driver = webdriver.Chrome()
driver.get("https://admin.packzy.com/admin/dashboard")

WAIT = WebDriverWait(driver, 10)  # waits up to 10 sec for element to appear

# -----------------------------
# SAFE CLICK HELPER
# -----------------------------
def safe_click(by, value):
    """Waits for element, scrolls to it, then clicks. Prints clear error if it fails."""
    try:
        element = WAIT.until(EC.element_to_be_clickable((by, value)))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        print(f"Clicked: {value}")
    except TimeoutException:
        print(f"TIMEOUT: Element not found or not clickable within 10s → {value}")
    except ElementNotInteractableException:
        print(f"NOT INTERACTABLE: Element exists but can't be clicked → {value}")
    except StaleElementReferenceException:
        print(f"STALE: Page changed before click → {value}, retrying...")
        time.sleep(0.5)
        safe_click(by, value)  # retry once
    except Exception as e:
        print(f"UNKNOWN ERROR on '{value}': {e}")

# -----------------------------
# HOTKEY ACTIONS
# -----------------------------
def click_button_1():
    safe_click(By.ID, "merchant")

def click_button_2():
    safe_click(By.XPATH, "//*[contains(text(), 'Data Entry')]")  # ID can't have spaces, fixed

def click_button_3():
    safe_click(By.XPATH, "//button[text()='Login']")

def click_button_4():
    safe_click(By.CSS_SELECTOR, ".submit")

def click_button_5():
    safe_click(By.NAME, "search")

# -----------------------------
# HOTKEY MAP
# -----------------------------
HOTKEYS = {
    'alt+shift+1': click_button_1,
    'alt+shift+2': click_button_2,
    'shift+1':     click_button_3,
    'shift+2':     click_button_4,
    'shift+3':     click_button_5,
}

for hotkey, func in HOTKEYS.items():
    keyboard.add_hotkey(hotkey, func, suppress=True, trigger_on_release=True)

print("Selenium Hotkeys Active. Press Ctrl+C to exit.")

# -----------------------------
# KEEP RUNNING
# -----------------------------
try:
    while True:
        time.sleep(0.07)
except KeyboardInterrupt:
    print("Exited cleanly.")
    driver.quit()
    keyboard.unhook_all()
    sys.exit()