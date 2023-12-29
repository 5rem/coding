import socket
from urllib.parse import urlparse
import re


def match_ip(ip):
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(pattern, ip))


def dns_resolve(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    domain2 = match_ip(domain)
    if domain2 is True:
        return domain
    else:
        try:
            return socket.gethostbyname(domain)
        except Exception as e:
            print(f"Error resolving {domain}: {e}")
            return None


def remove_duplicates(urls):
    unique_urls = set()
    for url in urls:
        dns_ip = dns_resolve(url)
        if dns_ip is not None:
            unique_urls.add((url, dns_ip))  # 将 URL 和 IP 地址作为元组添加到集合中
    return unique_urls


# 从文件中读取URL列表
with open(r"D:\scan\httpx\keyishiyong.txt", "r", encoding="utf-8") as file:
    urls = file.readlines()

unique_urls = remove_duplicates(urls)

# 将结果写入另一个文件
with open(r"D:\scan\httpx\quchongfu.txt", "w", encoding="utf-8") as file:
    for url, ip in unique_urls:
        file.write(f"{url}\n")
        print(f"{url} -> {ip}")  # 在终端中输出去重后的 URL 和 IP 地址
