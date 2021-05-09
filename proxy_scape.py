import requests

proxies = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all")

with open('proxies.txt', 'a+') as f:
    f.write(proxies.text.replace('\n', ''))

