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


def locateNewPostSection():
    section = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div[1]/div/h3")
    if(section and section.text == "UPDATE"):
        print("[PASSED] - New Post section found")
    else:
        print("[FAILED] - New Post section not found")

def locateNewPostTextBox():
    section = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div[1]/div/form/div/textarea")
    if section:
        print("[PASSED] - New Post text box section found")
        section.send_keys("Testing post")
        time.sleep(4)
    else:
        print("[FAILED] - New Post text box section not found")

def locateTransmitButton():
    button = driver.find_element(By.XPATH, "/html/body/div/main/div/div[2]/div[1]/div[1]/div/form/button")
    if button:
        print("[PASSED] - Transmit button found")
        button_color = button.value_of_css_property("background-color")
        if button_color in ("rgba(0, 0, 0, 0)", "transparent"):
            print("[PASSED] - Transmit button is transparent")
        else:
            print("[FAILED] - Transmit button not transparent")
        button.click()
        time.sleep(3)
    else:
        print("[FAILED] - Transmit button not found")

def locateMyFeed():
    section = driver.find_element(By.XPATH, "//main//h1[normalize-space()='Agent Feed']")
    if section:
        print("[PASSED] - Agent Feed section found")
    else:
        print("[FAILED] - Agent Feed section not found")

#def locateNewPostUsername():
#    user = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[2]/div/h4")
#    if user:
#        print("[PASSED] - Username for post found")
#    else:
#        print("[FAILED] - Username for post not found")

#def locateNewPostTime():
#    time = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[2]/div/h6")
#    if time:
#        print("[PASSED] - Time for post found")
#    else:
#        print("[FAILED] - Time for post not found")

#def locateNewPostText():
#    text = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[2]/div/p")
#    if text:
#        print("[PASSED] - Text for post found")
#    else:
#        print("[FAILED] - Text for post not found")


try:
    driver.get("http://127.0.0.1:5005/loginscreen")
    time.sleep(2)

    print("--= Beginning Tests - Emma =--")
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")

    if login_button:
        print("[PASSED] - Login button exists")
        username_txt = driver.find_element(By.CSS_SELECTOR, "input[type='text'][name='username']")
        username_txt.send_keys("emma")

        password_txt = driver.find_element(By.CSS_SELECTOR, "input[type='password'][name='password']")
        password_txt.send_keys("test")
        
        login_button.click()
        time.sleep(4)
        locateMyFeed()
        locateNewPostSection()
        locateNewPostTextBox()
        locateTransmitButton()
#        welcome_line = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/h1")
#        if(welcome_line and welcome_line.text == "Welcome, emma!"):
#            print("[PASSED] - User successfully logged in")
#            locateNewPostSection()
#            locateNewPostTextBox()
#            locateSubmitButton()
#            locateMyFeed()
#            locateNewPostUsername()
#            locateNewPostTime()
#            locateNewPostText()
#        else:
#            print("[FAILED] - User not logged in.")
#        
#        time.sleep(2)
#
#    else:
#        print("[FAILED] - Login button not found.")
except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    #print("10 Tests Ran: 10 Tests Passed")
    driver.quit()

