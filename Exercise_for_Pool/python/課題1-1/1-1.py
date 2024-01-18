import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import csv
import re
import ssl

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}

urls = [
    "https://r.gnavi.co.jp/p864034/",
    "https://r.gnavi.co.jp/dhpxwcry0000/",
    "https://r.gnavi.co.jp/p2cbxryf0000/",
    "https://r.gnavi.co.jp/gak5844/",
    "https://r.gnavi.co.jp/g112500/",
    "https://r.gnavi.co.jp/be2zhv140000/",
    "https://r.gnavi.co.jp/g853122/",
    "https://r.gnavi.co.jp/dxhskv1b0000/",
    "https://r.gnavi.co.jp/3dtsp2tp0000/",
    "https://r.gnavi.co.jp/a318806/",
    "https://r.gnavi.co.jp/a1vpgrs10000/",
    "https://r.gnavi.co.jp/7e5dk4ex0000/",
    "https://r.gnavi.co.jp/g620622/",
    "https://r.gnavi.co.jp/axu8y34k0000/",
    "https://r.gnavi.co.jp/g493516/",
    "https://r.gnavi.co.jp/5x2v9juj0000/",
    "https://r.gnavi.co.jp/5922s03v0000/",
    "https://r.gnavi.co.jp/etb1jg070000/",
    "https://r.gnavi.co.jp/e892400/",
    "https://r.gnavi.co.jp/1xs3n7yv0000/",
    "https://r.gnavi.co.jp/gckh603/",
    "https://r.gnavi.co.jp/s6wp3mku0000/",
    "https://r.gnavi.co.jp/g493533/",
    "https://r.gnavi.co.jp/b934300/",
    "https://r.gnavi.co.jp/jfex1hw00000/",
    "https://r.gnavi.co.jp/a634203/",
    "https://r.gnavi.co.jp/4uf21jes0000/",
    "https://r.gnavi.co.jp/b97rkcd90000/",
    "https://r.gnavi.co.jp/endwf8fh0000/",
    "https://r.gnavi.co.jp/kbnmxzw30000/",
    "https://r.gnavi.co.jp/e2gc74ua0000/",
    "https://r.gnavi.co.jp/cc0621e60000/",
    "https://r.gnavi.co.jp/stcar5tc0000/",
    "https://r.gnavi.co.jp/a538508/",
    "https://r.gnavi.co.jp/ad2jcfny0000/",
    "https://r.gnavi.co.jp/2auk9en00000/",
    "https://r.gnavi.co.jp/hezarf970000/",
    "https://r.gnavi.co.jp/bn8ypj8n0000/",
    "https://r.gnavi.co.jp/g414814/",
    "https://r.gnavi.co.jp/8c4aguwx0000/",
    "https://r.gnavi.co.jp/d0r9dw100000/",
    "https://r.gnavi.co.jp/f7gt3vxu0000/",
    "https://r.gnavi.co.jp/g493543/",
    "https://r.gnavi.co.jp/7n2j1tyc0000/",
    "https://r.gnavi.co.jp/g184900/",
    "https://r.gnavi.co.jp/g281800/",
    "https://r.gnavi.co.jp/bt9ry2u90000/",
    "https://r.gnavi.co.jp/p462003/",
    "https://r.gnavi.co.jp/peaem60s0000/",
    "https://r.gnavi.co.jp/b020100/"
]

def get_server_certificate(hostname):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
                der_cert = sslsock.getpeercert(True)
                return True
    except:
        return False

def get_info(url):
    # 3秒待ち
    #sleep(3)

    # ウェブページの取得
    response = requests.get(url, headers=header)

    # 取得したHTMLを解析
    soup = BeautifulSoup(response.content, "html.parser")

    # 店舗名
    store_name_element = soup.find("dt", class_="contact-term")
    store_name = store_name_element.text if store_name_element else None

    # 電話番号
    phone_number_element = soup.find("span", class_="number")
    phone_number = phone_number_element.text if phone_number_element else None

    # メールアドレス
    email_address_list = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", response.text)
    email_address = email_address_list[0] if email_address_list else None

    # 都道府県・市区町村・番地・建物名
    address_pref_element = soup.find(class_="region")
    address_suf_element = soup.find(class_="locality")
    left = re.findall('[^0-9-]+', address_pref_element.text)[0] # 番地より左
    prefecture, city = re.findall("[^都]+[都]?", left)
    street = re.findall("[0-9-]+", address_pref_element.text)[0]
    building_name = address_suf_element.text if address_suf_element else None

    # URL
    URL = url

    # SSL
    SSL = get_server_certificate("r.gnavi.co.jp")
    
    return [store_name, phone_number, email_address, prefecture, city, street, building_name, URL, SSL]

def print_info(i, csv_list):
    store_name, phone_number, email_address, prefecture, city, street, building_name, URL, SSL = csv_list

    print("店舗No." + str(i + 1))
    print("店舗名:", store_name)
    print("電話番号:", phone_number)
    print("メールアドレス:", email_address)
    print("都道府県:", prefecture)
    print("市区町村:", city)
    print("番地:", street)
    print("建物名:", building_name)
    print("URL:", URL)
    print("SSL:", SSL)

    print()

def main():
    print()
    csv_file_name ='1-1.csv'

    with open(csv_file_name, 'w', newline='', errors='ignore') as f:
        writer = csv.writer(f)
        csv_header = ["店舗名", "電話番号", "メールアドレス", "都道府県", "市区町村:", "番地:", "建物名:", "URL:", "SSL"]
        writer.writerow(csv_header)

        for i, url in enumerate(urls):
            csv_list = get_info(url)
            print_info(i, csv_list)
            writer.writerow(csv_list)

        f.close()

if __name__ == "__main__":
    main()