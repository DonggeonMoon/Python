from selenium import webdriver
import time

driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://www.youtube.com/watch?v=sJNC99aCHkQ")
driver.implicitly_wait(3)


prev_height = driver.execute_script("return document.body.scrolHeight")

while True:

    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    driver.execute_script("window.scrollBy(0, 10000)")
"""
    curr_height = driver.execute_script("return document.body.scrollHeight")

    if(curr_height== prev_height):
        break
    else:
        prev_height = driver.execute_script("return document.body.scrollHeight")

    print(prev_height)
    print(curr_height)
    print("checked")
"""

print("완료")
