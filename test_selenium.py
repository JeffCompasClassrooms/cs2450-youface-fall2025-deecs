from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://isitchristmas.com")

#Find the element with id="answer"
answer = driver.find_element(By.ID, "answer")

print("Page title:", driver.title)
print("Answer text:", answer.text)

driver.quit()
