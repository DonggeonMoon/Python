from selenium import webdriver
import time

driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://www.youtube.com/watch?v=sJNC99aCHkQ")
driver.implicitly_wait(3)


prev_height = driver.execute_script("return document.body.scrolHeight")

while True:
    driver.execute_script("window.scrollBy(0, 10000)")


print("완료")
