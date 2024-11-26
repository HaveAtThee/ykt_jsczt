import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_option = Options()

chrome_option.set_capability("goog:loggingPrefs", {"performance": "ALL"})


service = Service("./chromedriver-win64/chromedriver.exe")

driver = webdriver.Chrome(service=service, options=chrome_option)


driver.get("http://ykt.jsczt.cn/#/policy")

performance_log = driver.get_log("performance")

for packet in performance_log:
    message = json.loads(packet.get("message")).get("message")
    packet_method = message.get("method")
    if "Network" in packet_method:
        request_id = message.get("params").get("requestId")
        try:
            resp = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
            body = resp.get("params")
            # body = resp.get("body")

            # print(request_id)
            print(body)

        except:
            pass

