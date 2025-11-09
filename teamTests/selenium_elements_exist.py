from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Don't specify chromedriver path!
driver = webdriver.Chrome(options=options)

try:
    driver.get("http://localhost:5005/loginscreen")
    time.sleep(5)

    driver.set_window_size(1200,800)
    time.sleep(1)

    print("--= Beginning Tests = Cam --")
    
    username = "cam"
    password = "cam"

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password") 
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")

    if username_input:
        print("[PASSED] - Username input exists")
    else:
        print("[FAILED] - Username input doesn't exist")

    if password_input:
        print("[PASSED] - Password input exists")
    else:
        print("[FAILED] - Password input doesn't exist")

    if login_button:
        print("[PASSED] - Login button exists")
    else:
        print("[FAILED] - Login button doesn't exist")

    #if username_input and password_input and login_button:
        #username_input.send_keys(username)
        #password_input.send_keys(password)
        #login_button.click()
        #time.sleep(2)

        #print("Login Successful")

        #post_textbox = driver.find_element(By.CSS_SELECTOR, "textarea[name='post']")
        #post_button = driver.find_element(By.CSS_SELECTOR, "button[name='post-submit']")

        #if post_textbox:
        #    print("[PASSED] - Post textbox exists")
        #else:
        #    print("[FAILED] - Post textbox does not exist.")

        #if post_button:
        #    print("[PASSED] - Post button exists")
        #else:
        #    print("[FAILED] - Post button does not exist.")
   
    #friend_textbox = driver.find_element(By.CSS_SELECTOR, "input[name='name']")
    #friend_button = driver.find_element(By.CSS_SELECTOR, "button[name='addfriend']")
    #friend_textbox.send_keys(username)
    #friend_button.click()
    #time.sleep(1)

    #print("Add Friend Successful")


    #brand = driver.find_element(By.CSS_SELECTOR, "a[class='navbar-brand']")
    
    #links = driver.find_elements(By.CSS_SELECTOR, "a.nav-link")
    #ut_link = links[0].get_attribute("href")
    #troll_link = links[1].get_attribute("href")

    #logout_button = driver.find_element(By.CSS_SELECTOR, "button[name='logout']")

    #header_text = driver.find_element(By.CSS_SELECTOR, "div.row.justify-content-md-center.mb-4 h1").text

    #post_textbox = driver.find_element(By.CSS_SELECTOR, "textarea[name='post']")
    #post_button = driver.find_element(By.CSS_SELECTOR, "button[name='post-submit']")

    #friend_link = driver.find_element(By.LINK_TEXT, "cam").get_attribute("href")


    #if brand:
    #    print("[PASSED] - Brand class exists.")
    #else:
    #    print("[FAILED] - Brand class not found.")

    #if ut_link == "https://utahtech.edu/":
    #    print("[PASSED] - UT link exists.")
    #else:
    #    print("[Failed] - UT link not found or doesn't link to correct page.")

    #if troll_link == "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1&ab_channel=RickAstley":
    #    print("[PASSED] - Troll link exists.")
    #else:
    #    print("[Failed] - Troll link not found or doesn't link to correct page.")

    #if logout_button.is_displayed():
    #    print("[PASSED] - Logout Button exists")
    #else:
    #    print("[Failed] - Logout Button does not exist.")

    #if not header_text:
    #    print("[FAILED] - Header does not exist.")
    #elif username in header_text:
    #    print("[PASSED] - Header exists with correct name")
    #else:
    #    print(f"[Failed] - Header shows '{header}' instead of username")

    #if post_textbox:
    #    print("[PASSED] - Post textbox exists")
    #else:
    #    print("[FAILED] - Post textbox does not exist.")

    #if post_button:
    #    print("[PASSED] - Post button exists")
    #else:
    #    print("[FAILED] - Post button does not exist.")

    #if friend_textbox:
    #    print("[PASSED] - Friend textbox exists")
    #else:
    #    print("[FAILED] - Friend textbox does not exist.")

    #if friend_button:
    #    print("[PASSED] - Friend button exists")
    #else:
    #    print("[FAILED] - Friend button does not exist.")

    #if friend_link == "http://localhost:5005/friend/cam":
    #    print("[PASSED] - Friend link exists")
    #else:
    #    print("[FAILED] - Friend link does not exist.")

except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
