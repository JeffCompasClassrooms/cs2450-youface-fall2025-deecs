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
    passed = 0

    # nav_home_link = driver.find_element(By.CSS_SELECTOR,"nav.navbar div.container a.navbar-brand")
    # h1_home_link = driver.find_element(By.CSS_SELECTOR,"div.jumbotron div.container h1 > a")
    login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
    create_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Create']")
    # delete_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Delete']")
    c1 = login_button.value_of_css_property("background-color")
    # c2 = create_button.value_of_css_property("background-color")
    # c3 = delete_button.value_of_css_property("background-color")
    # copy = driver.find_element(By.CSS_SELECTOR, "p[class='lead']").text
    # legend = driver.find_element(By.TAG_NAME, "legend")
    # username_label = driver.find_element(By.CSS_SELECTOR, "label[for='username']")
    # username_input = driver.find_element(By.NAME, "username")
    # password_label = driver.find_element(By.CSS_SELECTOR, "label[for='password']")
    # password_input = driver.find_element(By.NAME, "password")
    # form = driver.find_element(By.TAG_NAME, "form")
    # submit_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")
    # primary_btn = driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary[value='Login']")
    # success_btn = driver.find_element(By.CSS_SELECTOR, "input.btn.btn-success[value='Create']")
    # danger_btn = driver.find_element(By.CSS_SELECTOR, "input.btn.btn-danger[value='Delete']")
    # c_primary = primary_btn.value_of_css_property("background-color")
    # c_success = success_btn.value_of_css_property("background-color")
    # c_danger = danger_btn.value_of_css_property("background-color")

    # if h1_home_link:
    #     print("[PASSED] - Header home link exists."); passed += 1
    # else:
    #     print("[FAILED] - Header home link not found.")
    if login_button:
        print("[PASSED] - Login Button Exists."); passed += 1
    else:
        print("[FAILED] - Login button not found.")
    if create_button:
        print("[PASSED] - Create Button Exists."); passed += 1
    else:
        print("[FAILED] - Create button not found.")
    # if delete_button:
    #     print("[PASSED] - Delete Button Exists."); passed += 1
    # else:
    #     print("[FAILED] - Delete button not found.")
    # if legend and legend.text.strip() == "Login":
    #     print("[PASSED] - Legend text is exactly 'Login'."); passed += 1
    # else:
    #     print("[FAILED] - Legend text mismatch.")
    # if username_label.text.strip().lower() == "username" and username_input.get_attribute("type") == "text":
    #     print("[PASSED] - Username label and input type=text are correct."); passed += 1
    # else:
    #     print("[FAILED] - Username label/input mismatch.")
    # if password_label.text.strip().lower() == "password" and password_input.get_attribute("type") == "password":
    #     print("[PASSED] - Password label and input type=password are correct."); passed += 1
    # else:
    #     print("[FAILED] - Password label/input mismatch.")
    # if (form.get_attribute("method") or "").lower() == "post":
    #     print("[PASSED] - Form method is POST."); passed += 1
    # else:
    #     print("[FAILED] - Form method is not POST.")
    # values = {b.get_attribute("value") for b in submit_buttons}
    # if len({c_primary,c_success,c_danger}) == 3:
    #     print(f"[PASSED] - Button colors are correct: {c_primary}, {c_success}, {c_danger}"); passed += 1
    # else:
    #     print(f"[FAILED] - Button colors not correct: {c_primary}, {c_success}, {c_danger}")
    # if copy == "A billion dollars and it's yours!":
    #     print("[FAILED] - Tag descrikption is correct.")
    # else:
    #     print("[PASSED] - Tag descrption is not correct."); passed += 1

    print(f"--= Total Passed Tests: {passed} =--")

except Exception as e:
    print("Error:", e)
finally:
    print("--= Ending Tests =--")
    driver.quit()