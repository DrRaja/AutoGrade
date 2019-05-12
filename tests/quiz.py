from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys


driver=webdriver.Chrome("C:\\Users\\rabia\\OneDrive\\Documents\\GitHub\\AutoGrader\\tests\\chromedriver.exe")    #the browser on which we are testing it and its driver path
driver.set_page_load_timeout(10)               #the timeout time to load for this page/site
driver.get("http://localhost:5000/quiz")                #the URL whihc we are going to test
driver.find_element_by_name("answer").send_keys("stack is a kind of Data Structure")

driver.find_element_by_name("button").send_keys(Keys.ENTER)
time.sleep(4)
driver.quit()
