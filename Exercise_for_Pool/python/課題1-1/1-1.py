import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import csv
import re
import ssl
import sys

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}

# Now Loading
def printNowLoading(p):
    s = "Now Loading: " + str(p) + "%"
    sys.stdout.write("\033[2K\033[G%s" % s) # 1行削除して、同じ場所に出力
    sys.stdout.flush()

def get_urls(n=50):
    print("URL取得開始")
    printNowLoading(0)
    main_url = "https://r.gnavi.co.jp/area/jp/rs/?date=20240119&fw=%E3%81%8A%E3%81%A7%E3%82%93" # ここに検索したページのURLを入力
    urls = []

    for p in range(1, 4):
        sleep(3)
        res = requests.get(main_url + "&p=" + str(p), headers=header)
        soup = BeautifulSoup(res.text, 'html.parser')
        elm_a = soup.find_all('a', class_='style_titleLink__oiHVJ')
        for e in elm_a:
            urls.append(e.attrs["href"])
        printNowLoading(33 * p + 1)

    urls.sort(key=len) 
    urls = urls[:n]
    print()
    print()

    return urls

def get_info(url):
    # ウェブページの取得
    #sleep(3)
    res = requests.get(url, headers=header)

    # 取得したHTMLを解析
    soup = BeautifulSoup(res.content, "html.parser")

    # 店舗名
    store_name_element = soup.find("dt", class_="contact-term")
    name = store_name_element.text if store_name_element else None

    # 電話番号
    phone_number_element = soup.find("span", class_="number")
    phone = phone_number_element.text if phone_number_element else None

    # メールアドレス
    email_address_list = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", res.text)
    addr = email_address_list[0] if email_address_list else None

    # 都道府県・市区町村・番地・建物名
    pattern = "(...??[都道府県])([^0-9-]+)(.+)"
    addr_pref_elm = soup.find(class_="region")
    result = re.match(pattern, addr_pref_elm.text)
    prfc = result.group(1)
    city = result.group(2)
    street = result.group(3)
    addr_suf_elm = soup.find(class_="locality")
    building = addr_suf_elm.text if addr_suf_elm else None

    # URL
    URL = None # 課題1-1 に関しては「URL」に入れる値は空でよい.

    # SSL
    SSL = False
    
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
    csv_file_name ='1-1.csv'

    with open(csv_file_name, 'w', newline='', errors='ignore') as f:
        writer = csv.writer(f)
        csv_header = ["店舗名", "電話番号", "メールアドレス", "都道府県", "市区町村:", "番地:", "建物名:", "URL:", "SSL"]
        writer.writerow(csv_header)

        urls = get_urls()
        for i, url in enumerate(urls):
            csv_list = get_info(url)
            print_info(i, csv_list)
            writer.writerow(csv_list)

        f.close()

if __name__ == "__main__":
    main()