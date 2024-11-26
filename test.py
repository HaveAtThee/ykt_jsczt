import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

class ykt_bonus_info_fetcher:
    def __init__(self):
        pass
        
    def get_siganture(self):
        # 配置选项
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")  # 可选，无头模式
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
                            self.signature = header["signature"]
                            self.timestamp = header["timestamp"]
            except Exception as e:
                # 忽略解析或其他异常
                pass

        # 关闭浏览器
        driver.quit()
    def get_all_city(self):
        headers = {
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Length": "0",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "http://ykt.jsczt.cn",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://ykt.jsczt.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "signature": self.signature,
            "timestamp": self.timestamp
        }
        url = "http://ykt.jsczt.cn/yktffjk/qhList"  # 替换为目标 URL
        response = requests.post(url, headers=headers)
        # self.city_json = response.json()["data"]["data"]
        print(response.text)
    def get_js_region(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "http://ykt.jsczt.cn",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://ykt.jsczt.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "signature": self.signature,
            "timestamp": self.timestamp
        }
        url = "http://ykt.jsczt.cn/yktffjk/subqhList"
        data = {
            "admDivCode": "32"
        }
        response = requests.post(url, headers=headers, data=data)
        self.region_json = response.json()["data"]["data"]
        print(self.region_json)
    def get_policy_list(self,admDivCode):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "http://ykt.jsczt.cn",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://ykt.jsczt.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "signature": self.signature,
            "timestamp": self.timestamp
        }
        data = {
            "admDivCode": admDivCode
        }
        url = "http://ykt.jsczt.cn/yktffjk/zcxxList"
        response = requests.post(url, headers=headers, data=data)
        self.policy_list = response.json()["data"]["data"]
        print(self.policy_list)
    def get_policy_content(self,uuid):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "http://ykt.jsczt.cn",
            "Proxy-Connection": "keep-alive",
            "Referer": "http://ykt.jsczt.cn/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "signature": self.signature,
            "timestamp": self.timestamp
        }
        data = {
            "uuid": uuid
        }
        url = "http://ykt.jsczt.cn/yktffjk/zcxxContent"
        response = requests.post(url, headers=headers, data=data)
        self.policy_list = response.json()["data"]["data"]
        print(response.text)

if __name__ =="__main__":
    fetcher = ykt_bonus_info_fetcher()
    fetcher.get_siganture()
    fetcher.get_js_region()
    fetcher.get_policy_list(320000)
    fetcher.get_policy_content("1CE00A51BD7E3B94E0635D1A1223645C")