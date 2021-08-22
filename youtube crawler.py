from selenium import webdriver
import time

driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://www.youtube.com/watch?v=sJNC99aCHkQ")
driver.implicitly_wait(3)


prev_height = driver.execute_script("return document.body.scrolHeight")

for i in range(0, 10000):
    driver.execute_script("window.scrollBy(0, 10000)")
    print(i)

text = driver.find_element_by_css_selector("#content").text

print(text)

print("완료")
