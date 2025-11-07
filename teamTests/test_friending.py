from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--remote-debugging-port=9222')

# Don't specify chromedriver path!
# Dayne - Selenium Manager doesn't seem to be packaged for ubuntu
#service = Service('./chromedriver')
driver = webdriver.Chrome(options=options)

def del_user(password):
   pass 

def logout():
    logout_button = driver.find_element(By.CSS_SELECTOR, "aside.sidebar button.logout-btn")
    logout_button.click()
    time.sleep(1)

def create_account(email, password, username, fname, lname):
    email_input = driver.find_element(By.CSS_SELECTOR, "form[action='/signup'] input[name='email']")
    username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    password_input = driver.find_element(By.CSS_SELECTOR, "form[action='/signup'] input[name='password']")
    fname_input = driver.find_element(By.CSS_SELECTOR, "input[name='first_name']")
    lname_input = driver.find_element(By.CSS_SELECTOR, "input[name='last_name']")
    email_input.send_keys(email)
    username_input.send_keys(username)
    password_input.send_keys(password)
    fname_input.send_keys(fname)
    lname_input.send_keys(lname)
    create_account_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create Account']")
    create_account_button.click()
    try:
        success_banner = driver.find_element(By.CSS_SELECTOR, "div.alert-danger")
        login(email, password)
    except Exception as e:
        pass


def login(email, password):
    email_input = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    login_button = driver.find_element(By.CSS_SELECTOR, "input[value='Login']")
    email_input.send_keys(email)
    password_input.send_keys(password)
    time.sleep(1)
    login_button.click()
    time.sleep(2)
    try:
        taken_us_banner = driver.find_element(By.CSS_SELECTOR, "div.alert-danger")  
    except Exception as e:
        pass#print("New account created")

def add_friend(friend_name):
        add_friend_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
        add_friend_input.send_keys(friend_name)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[name='addfriend']")
        submit_button.click()
        time.sleep(1)


#element.class works, spaces indicate descendants, < indicates when an element is directly inside of another element eg h1 > a for an anchor tag inside of an h1 tag

try:
    driver.set_window_size(1200, 800)
    driver.get("http://localhost:5005/login_screen")
    time.sleep(1)
    total_tests = 0
    successful_tests = 0
    print("--= Beginning Tests - Dayne Wyler =--")

    create_account("doe@doe.com", "testing", "John", "John", "Doe")
    
    add_friend_button = None
    add_friend_input_form = driver.find_element(By.CSS_SELECTOR, "form[action='/addfriend'")
    add_friend_input_form_name = driver.find_element(By.CSS_SELECTOR, "div.col-lg-3  h3[class='card-title']").text
    add_friend_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
    add_friend_input.send_keys("john")
    add_friend_button = driver.find_element(By.CSS_SELECTOR, "button[name='addfriend']")
    add_friend_button.click()
    time.sleep(1)
    
    total_tests += 1
    if add_friend_input_form:
        print("[PASSED] - Add Friend Form is in place.") 
        successful_tests += 1
    else:
        print("[FAILED] - Add Friend From is not in place.")


    total_tests += 1
    if add_friend_input_form_name == "ADD AGENT":
        print("[PASSED] - Add Friend Form Name is Correct.")
        successful_tests += 1
    else:
        print("[FAILED] - Add Friend Form Name has been changed to ." + add_friend_input_form_name)

    total_tests += 1
    if add_friend_button:
        print("[PASSED] - Friend Button Exists.")
        successful_tests += 1
    else:
        print("[FAILED] - Friend button not found.")

    total_tests += 1
    try:
        add_friend("nunshuch")
        add_failure_banner = driver.find_element(By.CSS_SELECTOR, "div.alert-danger")
        print("[PASSED] - Could Not Add Non-existent User as Friend")
        successful_tests += 1
    except Exception as e:
        print("[FAILED] - Added Non-existent User as Friend")

    logout()
    create_account("jane@doe.com", "tester", "Jane", "Jane", "Doe")

    total_tests += 1
    try:
        add_friend("John")
        friend_success_banner = driver.find_element(By.CSS_SELECTOR, "div.alert-success")
        print("[PASSED] - Friend Action Worked.")
        successful_tests += 1
    except Exception as e:
        print("[FAILED] - Friend Action did not succeed")

    total_tests += 1
    try:
        add_friend("John")
        friend_failure_banner = driver.find_element(By.CSS_SELECTOR, "div.alert-warning")
        print("[PASSED] - Did not add user already in friends list")
        successful_tests += 1
    except Exception as e:
        print("[FAILED] - Successfully added user already in friends list")

    total_tests += 1
    try:
        friends_list = driver.find_element(By.CSS_SELECTOR, "div.card-body ul")
        print("[PASSED] - Friends List Exists")
        successful_tests += 1
    except Exception as e:
        print("[FAILED] - Friends List Does Not Exist")

    total_tests += 1
    try:
        added_friend = driver.find_element(By.CSS_SELECTOR, "div.col-lg-3 a[href='/friend/John']")
        print("[PASSED] - Friend John was Found in Friends List")
        successful_tests += 1
    except Exception as e:
        print("[FAILED] - Friend John was Not Found in Friends List")

    total_tests += 1
    try:
        add_friend_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
        add_friend_input.send_keys("Doe")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[name='addfriend']")
        submit_button.click()
        time.sleep(1)
        friend_failure_banner = driver.find_element(By.CSS_SELECTOR, "div.alert-danger")
        print("[PASSED] - Using Password Did Not Add Friend")
        successful_tests += 1
    except Exception as e:
        print("[FAILURE] - Using Friend Password Successfully Added Friend")

    total_tests += 1
    try:
        friend_link = driver.find_element(By.CSS_SELECTOR, "div.col-lg-3 a[href='/friend/John']")
        friend_link.click()
        time.sleep(1)
        posts = driver.find_element(By.CSS_SELECTOR, "div.col-lg-8 h2").text
        print("[PASSED] - Friend Hyperlink Functioned Correctly")
        successful_tests += 1
    except Exception as e:
        print("[FAILED] - Friend Hyperlink Did not Function Correctly") 

except Exception as e:
    print("Error:", e)

finally:
    print(str(total_tests) + " Tests Ran: " + str(successful_tests) + " Tests Succeeded")
    print("--= Ending Tests =--")
    del_user("John")
    del_user("Jane")
    driver.quit()


