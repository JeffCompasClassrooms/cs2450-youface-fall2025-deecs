from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
options.add_argument('--disable-software-rasterizer')
options.add_argument('--remote-debugging-port=9222')

# Don't specify chromedriver path!
service = Service('/home/Dayne/bin/chromedriver')
driver = webdriver.Chrome(options=options, service=service)

#element.class works, spaces indicate descendants, < indicates when an element is directly inside of another element eg h1 > a for an anchor tag inside of an h1 tag

try:
    driver.get("http://localhost:5005/loginscreen")
    time.sleep(3)

    print("--= Beginning Tests =--")
    username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    username.send_keys("John")
    password.send_keys("Doe")
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
    login_button.click()
    time.sleep(2)

    add_friend_button = driver.find_element(By.CSS_SELECTOR, "div.jumbotron")
    add_friend_input_form = driver.find_element(By.CSS_SELECTOR, "body")
    add_friend_input_form_name = driver.find_element(By.CSS_SELECTOR, "h3[class='card-title']").text

    if add_friend_input_form_name == "Add Friend":
        print("[PASSED] - Add Friend Form Name is in place.")
    else:
        print("[FAILED] - Add Friend Form Name has been changed.")
    
    if add_friend_input_form:
        print("[PASSED] - Add Friend Form is in place.") 
    else:
        print("[FAILED] - ")

    if add_friend_button:
        print("[PASSED] - Friend Button Exists.")
    else:
        print("[FAILED] - Friend button not found.")


except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
