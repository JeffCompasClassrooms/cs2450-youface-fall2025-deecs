from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

options = Options()
#options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
#options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
options.add_argument('--disable-software-rasterizer')
options.add_argument('--remote-debugging-port=9222')

# Don't specify chromedriver path!
# Dayne - Selenium Manager doesn't seem to be packaged for ubuntu
service = Service('/home/Dayne/bin/chromedriver')
#service = Service()
driver = webdriver.Chrome(options=options, service=service)
#driver = webdriver.Chrome(options=options)

def reset_db():
    empty_db = {"_default" : {}, "posts" : {}, "users" : {}}
    with open("../db.json", 'w') as f:
        json.dump(empty_db, f, indent=2)

def logout():
    logout_button = driver.find_element(By.CSS_SELECTOR, "button[name='logout']")
    logout_button.click()
    time.sleep(1)

def login(username, password):
    username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    username_input.send_keys(username)
    password_input.send_keys(password)
    create_account_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
    create_account_button.click()
    time.sleep(1)
    try:
        taken_us_banner = driver.find_element(By.CSS_SELECTOR, "div.alert-danger")
        login_button = driver.find_element(By.CSS_SELECTOR, "input[value='Login']")
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()
        time.sleep(2)
    except Exception as e:
        pass#print("New account created")

def add_friend(friend_name):
        add_friend_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
        add_friend_input.send_keys(friend_name)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[name='addfriend']")
        submit_button.click()
        time.sleep(1)

reset_db()

#element.class works, spaces indicate descendants, < indicates when an element is directly inside of another element eg h1 > a for an anchor tag inside of an h1 tag

try:
    driver.set_window_size(1200, 800)
    driver.get("http://localhost:5005/loginscreen")
    time.sleep(1)

    print("--= Beginning Tests - Dayne Wyler =--")

    login("John", "Doe")
    
    add_friend_button = None
    add_friend_input_form = driver.find_element(By.CSS_SELECTOR, "form[action='/addfriend'")
    add_friend_input_form_name = driver.find_element(By.CSS_SELECTOR, "div.col-lg-3  h3[class='card-title']").text
    add_friend_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
    add_friend_input.send_keys("john")
    add_friend_button = driver.find_element(By.CSS_SELECTOR, "button[name='addfriend']")
    add_friend_button.click()
    time.sleep(1)
    
    if add_friend_input_form:
        print("[PASSED] - Add Friend Form is in place.") 
    else:
        print("[FAILED] - Add Friend From is not in place.")

    if add_friend_input_form_name == "Add Friend":
        print("[PASSED] - Add Friend Form Name is Correct.")
    else:
        print("[FAILED] - Add Friend Form Name has been changed to ." + add_friend_input_form_name)

    if add_friend_button:
        print("[PASSED] - Friend Button Exists.")
    else:
        print("[FAILED] - Friend button not found.")

    try:
        add_friend("nunshuch")
        add_failure_banner = driver.find_element(By.CSS_SELECTOR, "div.alert-danger")
        print("[PASSED] - Could Not Add Non-existent User as Friend")
    except Exception as e:
        print("[FAILED] - Added Non-existent User as Friend")

    logout()
    login("Jane", "Doe")

    try:
        add_friend("John")
        friend_success_banner = driver.find_element(By.CSS_SELECTOR, "div.alert-success")
        print("[PASSED] - Friend Action Worked.")
    except Exception as e:
        print("[FAILED] - Friend Action did not succeed")

    try:
        add_friend("John")
        friend_failure_banner = driver.find_element(By.CSS_SELECTOR, "div.alert-warning")
        print("[PASSED] - Did not add user already in friends list")
    except Exception as e:
        print("[FAILED] - Successfully added user already in friends list")

    try:
        friends_list = driver.find_element(By.CSS_SELECTOR, "div.card-body ul")
        print("[PASSED] - Friends List Exists")
    except Exception as e:
        print("[FAILED] - Friends List Does Not Exist")

    try:
        added_friend = driver.find_element(By.CSS_SELECTOR, "div.col-lg-3 a[href='/friend/John']")
        print("[PASSED] - Friend John was Found in Friends List")
    except Exception as e:
        print("[FAILED] - Friend John was Not Found in Friends List")

    try:
        add_friend_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
        add_friend_input.send_keys("Doe")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[name='addfriend']")
        submit_button.click()
        time.sleep(1)
        friend_failure_banner = driver.find_element(By.CSS_SELECTOR, "div.alert-danger")
        print("[PASSED] - Using Password Did Not Add Friend")
    except Exception as e:
        print("[FAILURE] - Using Friend Password Successfully Added Friend")

    try:
        friend_link = driver.find_element(By.CSS_SELECTOR, "div.col-lg-3 a[href='/friend/John']")
        friend_link.click()
        time.sleep(1)
        posts = driver.find_element(By.CSS_SELECTOR, "div.col-lg-8 h2").text
        print("[PASSED] - Friend Hyperlink Functioned Correctly")
    except Exception as e:
        print("[FAILED] - Friend Hyperlink Did not Function Correctly") 

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()


