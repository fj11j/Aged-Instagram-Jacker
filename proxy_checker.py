import requests
import threading
class proxyChecker:
    def __init__(self):
        print('ok')

    def start(self, proxy):
        try:
            result = requests.get('https://www.instagram.com', proxies={'http':str(proxy), 'https': str(proxy)}, timeout=4)
       
            if result.status_code == 200:
                print('Good ' + proxy)
                with open('good.txt', 'a+') as f:
                    f.write(proxy + '\n')
            else:
                return
        except:
            return
    def _thread(self):
        with open('proxies.txt', 'r') as f:
            for proxy in f:
                proxy = proxy.replace('\n', '')
                attempting = True
                while attempting == True:
                    if threading.active_count() <= 300:
                        threading.Thread(target=self.start, args=(proxy,)).start()
                        attempting = False


if __name__ == '__main__':
    check = proxyChecker()
    check._thread()
