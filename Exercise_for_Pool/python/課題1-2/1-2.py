from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import sys
import csv
import re
import ssl

# ユーザエージェントの設定
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}

# SSL認証の無視
ssl._create_default_https_context = ssl._create_unverified_context

# driverの設定
options = webdriver.ChromeOptions()
#options.add_argument('--headless') # ヘッドレスモード
options.add_argument('--user-agent=' + header["User-Agent"])
driver = webdriver.Chrome('./chromedriver', options=options)

# Now Loading
def printNowLoading(p):
    s = "Now Loading: " + str(p) + "%"
    sys.stdout.write("\033[2K\033[G%s" % s) # 1行削除して、同じ場所に出力
    sys.stdout.flush()

def get_urls(n=50):
    sleep(3)
    driver.get("https://r.gnavi.co.jp/area/tokyo/rs/?p=2")
    urls = []

    for i in range(10):
        elem_bt = driver.find_element(By.XPATH, "//div/nav/ul/li[12]/a")
        elem_bt.click()
        for elem_a in driver.find_elements_by_xpath('//div/div/div/article/div/a'):
            urls.append(elem_a.get_attribute('href'))
        printNowLoading((i + 1) * 10)
    print()

    urls.sort(key=len) 
    urls = urls[:n]

    return urls

def get_server_certificate(hostname):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
                der_cert = sslsock.getpeercert(True)
                return True
    except:
        return False

# 各々のURLについて、店舗情報をスクレイピング
def get_info(url):
    # 3秒待ち
    sleep(3)

    # ウェブページの取得
    driver.get(url)
    
    # 要素の取得
    elm = driver.find_elements_by_xpath("//section/div/div/div/table/tbody/tr/td")

    # 店舗
    name_elm = elm[0].find_elements_by_xpath("./p[1]")[0]
    name = name_elm.text

    # 電話番号
    phone_elm = elm[1].find_elements_by_xpath("./ul/li/span[1]")[0]
    phone = phone_elm.text

    # メールアドレス
    addr_elm = driver.find_elements_by_xpath("//section/div/div/div/table/tbody/tr/td/ul/li/a")
    addr_dic = {e.text: e.get_attribute('href') for e in addr_elm}
    if "お店に直接メールする" in addr_dic:
        addr = addr_dic["お店に直接メールする"]
    else:
        addr = None
    
    # 都道府県・市区町村・番地・建物名
    adr_elms = elm[2].find_elements_by_xpath("./p/span")
    adr_list = [e.text for e in adr_elms]
    left = re.findall('[^0-9-]+', adr_list[0])[0] # 番地より左
    prfc, city = re.findall("[^都]+[都]?", left)
    street = re.findall("[0-9-]+", adr_list[0])[0]
    if len(adr_list) >= 2:
        building = adr_list[1]
    else:
        building = None

    # URL
    URL = url

    # SSL
    SSL = get_server_certificate("r.gnavi.co.jp")
    
    return [name, phone, addr, prfc, city, street, building, URL, SSL]

def print_info(i, csv_list):
    name, phone, addr, prfc, city, street, building, URL, SSL = csv_list

    print("【店舗No." + str(i + 1) + "】")
    print("店舗名:        ", name)
    print("電話番号:      ", phone)
    print("メールアドレス:", addr)
    print("都道府県:      ", prfc)
    print("市区町村:      ", city)
    print("番地:          ", street)
    print("建物名:        ", building)
    print("URL:           ", URL)
    print("SSL:           ", SSL)

    print()

def main():
    print("URLの取得開始")
    printNowLoading(0)
    urls = get_urls()
    csv_file_name = '1-2.csv'

    with open(csv_file_name, 'w', newline='', errors='ignore') as f:
        writer = csv.writer(f)
        csv_header = [
            "店舗名",
            "電話番号",
            "メールアドレス",
            "都道府県",
            "市区町村",
            "番地",
            "建物名",
            "URL",
            "SSL"
        ]
        writer.writerow(csv_header)
        for i, url in enumerate(urls):
            csv_list = get_info(url)
            print_info(i, csv_list)
            writer.writerow(csv_list)
    
    driver.close()

if __name__ == "__main__":
    main()