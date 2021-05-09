#import modules
import requests
from time import sleep
from time import time
import json
import re
import random

class igScrape:
    def __init__(self):
        self.starter = input('> Base Username: ')
        self.first = self.starter
        self.lastchecked = self.starter
        self.username = input('> Username: ')
        self.password = input('> Password: ')
        self.grabid(self.starter)
        print('Ready.')
    
    def check_for_strong(self, string):
        comp1 = re.compile('[!@#$%^&+*"=(),?":{}|<>]')
        if comp1.search(string) == None:
            comp2 = re.compile("[!@#$%;~^&+*=(),?:{}|<>']")
            if comp2.search(string) == None:
                if '-' not in string:
                    if '.' not in string:
                        if '_' not in string:
                            if string[len(string) - 1].isdigit():
                                return True

    def grabid(self, username):
        getid = requests.get('https://www.instagram.com/web/search/topsearch/?query=' + str(username) + '/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.287'})
        try:
            self.userid = None
            idjson = getid.json()
            for user in idjson['users']:
                if user['user']['username'] == username:
                    self.userid = user['user']['pk']
                    self.userpfp = user['user']['profile_pic_url']
                    print(username + ' found! | UserID: ' + self.userid)
                    print('User Info [Handled]')
        except Exception as e:
            print('Error: ' + str(e))
            return
        else:
            if self.userid == None:
                return
                quit()


    def get_followers(self, session):
        cookie = session.get('https://www.instagram.com/')
        csrf0 = cookie.cookies.get_dict()['csrftoken']
        follower_grab = {
                "id": str(self.userid),
                "include_reel": True,
                "fetch_mutual": True,
                "first": '100'
            }
        grab_headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'referer': f'https://www.instagram.com/{self.starter}/followers/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.287',
            'x-csrftoken': csrf0,
            'x-requested-with': 'XMLHttpRequest'
        }
        followercount = 1
        try:
            grab_followers = session.get('https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=' + json.dumps(follower_grab), headers=grab_headers)
            try:
                if grab_followers.json()['data']['user']['edge_followed_by']['edges'] == '' or  grab_followers.json()['data']['user']['edge_followed_by']['edges'] == None or len(grab_followers.json()['data']['user']['edge_followed_by']['edges']) == 0 or grab_followers.json()['data']['user']['edge_followed_by']['count'] == '0' or grab_followers.json()['data']['user']['edge_followed_by']['count'] == 0:
                    print('Invalid user ' + self.starter)
                    if self.starter == self.lastchecked:
                        self.starter = self.first
                    else:
                        self.starter = self.lastchecked
                    self.grabid(self.starter)
                    self.get_followers(session)
                    return
            except:
                print('Invalid user ' + self.starter)
                self.starter = self.first
                self.get_followers(session)
                return
            else:
                for person in grab_followers.json()['data']['user']['edge_followed_by']['edges']:
                    if self.check_for_strong(person.get('node').get('username')) == True:
                        followercount += 1
                        with open('results.txt', 'a+') as f:
                            f.write(person.get('node').get('username') + '\n')
                try:
                    self.starter = grab_followers.json()['data']['user']['edge_followed_by']['edges'][random.randint(0, followercount - 1)].get('node').get('username')
                except:
                    self.get_followers(session)
                else:
                    print('New base user ' + self.starter)
                    self.lastchecked = self.starter
                    self.grabid(self.starter)
                    self.get_followers(session)
                    
        except:
            self.starter = self.first
            self.get_followers(session)

    
    def start(self):
        username = self.username
        password = self.password
        session = requests.session()


        melena = {
            'accept': '/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com/',
            'cookie': 'ig_cb=1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        
        cookie = session.get('https://www.instagram.com/accounts/login/', headers = melena)
        #time.sleep(1)
        csrf0 = cookie.cookies.get_dict()['csrftoken']
        print(csrf0)

        
        #print(session.cookies.get_dict())
        #csrf0 = cookie.cookies.get_dict()['csrftoken']
        unixtime = str(time())
        loginurl = 'https://www.instagram.com/accounts/login/ajax/'
        data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{unixtime}:{password}',
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
        
        loginresponse = session.post(loginurl, data=data, headers=login_headers)
        if loginresponse.json().get('authenticated') == True:
            print(username + ' || Logged in!')
            self.get_followers(session)
        elif 'Please wait a few minutes before you try again.' in loginresponse.text:
            print('You are being rate limited!')

            

            
        
        
if __name__ == '__main__':
    scrape = igScrape()
    scrape.start()
