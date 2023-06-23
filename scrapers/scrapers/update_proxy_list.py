import requests
import json


def update_proxy_list():
    """Fetches updated proxy info and writes the urls to the proxy_list.txt file"""
    res = requests.get(
        "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&filterUpTime=60&anonymityLevel=elite")

    proxies = json.loads(res.text)["data"]
    print(proxies)

    with open('proxy_list.txt', 'w') as file:

        for proxy in proxies:
            proxy_url = "http://" + proxy["ip"] + ":" + proxy["port"]
            file.write(proxy_url + "\n")


if __name__ == "__main__":
    update_proxy_list()
