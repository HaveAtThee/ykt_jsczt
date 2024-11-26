from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

def get_siganture():
    # 设置 ChromeDriver 路径


    # 配置选项
    options = Options()
    options.add_argument("--headless")  # 可选，无头模式
    options.add_argument("--disable-gpu")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})



    # 启动浏览器
    driver = webdriver.Chrome( options=options)

    # 启用 Network 捕获
    driver.execute_cdp_cmd("Network.enable", {})

    # 打开目标页面
    driver.get("http://ykt.jsczt.cn/#/policy")
    driver.implicitly_wait(10)
    # 获取性能日志并提取所有请求的 URL
    performance_log = driver.get_log("performance")

    print("All request URLs:")
    for packet in performance_log:
        try:
            # 解析日志中的 JSON 数据
            message = json.loads(packet.get("message")).get("message")
            packet_method = message.get("method")

            # 监听请求发送事件
            if packet_method == "Network.requestWillBeSent":
                request_details = message.get("params")
                initiator_type = request_details.get("initiator", {}).get("type")
                url = request_details.get("request", {}).get("url")  # 获取 URL


                header = request_details.get("request", {}).get("headers")  # 获取 URL
                if initiator_type in ["script"]:
                    if url.endswith(".css") or url.endswith(".js"):
                        pass
                    else:
                        print(url)
                        print(header["signature"])
                        print(header["timestamp"])
        except Exception as e:
            # 忽略解析或其他异常
            pass

    # 关闭浏览器
    driver.quit()
if __name__ =="__main__":
    get_siganture()
