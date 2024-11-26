from selenium import webdriver
from selenium.webdriver.common.by import By


# 启动 Chrome 浏览器
driver = webdriver.Chrome()
driver.get("http://ykt.jsczt.cn/#/policy")
driver.implicitly_wait(10)


driver.quit()