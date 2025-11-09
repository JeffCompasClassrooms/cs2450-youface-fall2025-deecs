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

    print("--= Beginning Tests =--")
    linkSpy = driver.find_element(By.LINK_TEXT, "mySpy(Janky Edition)")
    menu_button = driver.find_element(By.CLASS_NAME, "navbar-toggler")
    menu_button.click()
    time.sleep(1)
    linkUT = driver.find_element(By.LINK_TEXT, "Utah Tech")
    linkRick = driver.find_element(By.LINK_TEXT, "Link 2")
    create_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
    delete_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Delete']")



    if linkUT:
        print("[PASSED] - UT Link Exists.")
   
    else:
        print("[FAILED] - UT link not found.")

    if linkRick:
        print("[PASSED] - RickRoll Link Exists.")
    else:
        print("[FAILED] - rick link not found.")

    if linkSpy:
        print("[PASSED] - MySpy Link Exists.")
    else:
        print("[FAILED] - spy link not found.")
    
    if menu_button:
        print("[PASSED] - Menu Button Exists.")
    else:
        print("[FAILED] - menu button not found.")
    
    if linkRick and linkUT: 
        print("[PASSED] - Menu Button can be cliked")
    else:
        print("[FAILED] - menu button cannot be cliked")

    if linkRick.get_attribute("href") == "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1&ab_channel=RickAstley":
        print("[PASSED] - RickRoll link is correct")
    else:
        print("[FAILED] - RickRoll link is incorret")
    
    if linkUT.get_attribute("href") == "https://utahtech.edu/":
        print("[PASSED] - UT link is correct")
    else:
        print("[FAILED] - UT link is incorret")
    
    if linkSpy.get_attribute("href") == "http://localhost:5005/":
        print("[PASSED] - Home link is correct")
    else:
        print("[FAILED] - Home link is incorret")
    
    if create_button:
        print("[PASSED] - Create Button Exists.")
    else:
        print("[FAILED] - Create button not found.")

    if delete_button:
        print("[PASSED] - Delete Button Exists.")
    else:
        print("[FAILED] - Delete button not found.")




except Exception as e:
    print("Error:", e)

finally:
    print("--= Ending Tests =--")
    driver.quit()
