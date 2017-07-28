import requests
import re
import xlwt
from bs4 import BeautifulSoup


def get_proxy_ip(page):
    init_url = "http://www.kuaidaili.com/free/inha/"
    ip_and_port = list()
    for page in range(page, page + 1):
        url = init_url + str(page) + "/"
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        html = str(soup.select("#list")[0]).replace("\n", "")
        pattern = re.compile(
            '''<td data-title="IP">(.*?)</td><td data-title="PORT">(.*?)</td><td data-title="匿名度">.*?</td><td data-title="类型">HTTP''')
        for i in re.findall(pattern, html):
            ip_and_port.append(i)
    print("Get {} proxies.".format(len(ip_and_port)))
    return ip_and_port


def select_valid_ip(ip_port):
    url_for_testing = "http://icanhazip.com/"
    valid_proxies = list()
    for ip, port in ip_port:
        proxies = {
            "http": "http://" + ip + ":" + port
        }
        try:
            if str(requests.get(url_for_testing, proxies=proxies, timeout=1).content)[2:-3] == ip:
                print(proxies["http"] + " succeed.")
                valid_proxies.append((ip, port))
        except:
            print(proxies["http"] + " failed.")
            continue
    print("Get {} valid proxies.".format(len(valid_proxies)))
    return valid_proxies


def save_to_excel(proxies):
    wb = xlwt.Workbook()
    sh = wb.add_sheet('Sheet1')
    current_row = 0
    for ip, port in proxies:
        sh.write(current_row, 0, ip)
        sh.write(current_row, 1, port)
        current_row += 1
    wb.save('output_proxies.xls')
    print("Already finished saving valid proxies to output_proxies.xls.")


if __name__ == "__main__":
    valid_proxies = []
    page = 1
    while True:
        print("Page:" + str(page))
        ip_port_list = get_proxy_ip(page)
        [valid_proxies.append(i) for i in select_valid_ip(ip_port_list)]
        save_to_excel(valid_proxies)
        print("Total usable IP number: ", len(valid_proxies))
        page += 1
