import requests, pickle
import json
import base64
import os
from urllib.parse import urlparse
from releases1c import parsing
import sys
from clint.textui import progress
import time
from releases1c.progress import printProgressBar

class Request1C:
    
    session = None
    loginURL = "https://login.1c.ru"
    login = ""
    password = ""
    __saved_cookies_file = "__cookies.bin"
    
    def __init__(self, login:str, password:str, flush_cookie:bool):
        self.session = requests.Session()
        # load cookies
        if os.path.isfile(self.__saved_cookies_file) and not flush_cookie:
            #print('load cookies from file',self.__saved_cookies_file)
            with open(self.__saved_cookies_file, 'rb') as f:
                self.session.cookies.update(pickle.load(f))
        self.login = login
        self.password = password

    def get_url_params(self,url:str):
        url_parts = urlparse(url)
        url_query_params = list(map(lambda x: x.split('=')[0],url_parts.query.split('&')))
        url_path = url_parts.path.split('/')[1]
        can_be_file = False
        
        if (url_path == 'total'):
            parse_op = parsing.parse_releases_main_page
        elif (url_path == 'project'):
            parse_op = parsing.parse_project_page
        elif (url_path == 'version_files'):
            if (set(['nick','ver']) == set(url_query_params)):
                parse_op = parsing.parse_version_files
            else:
                print('>> UNSUPPORTED >>',url_path,url_query_params)
        elif (url_path == 'version_file'):
            if (set(['nick','ver','path']) == set(url_query_params)):
                parse_op = parsing.parse_sources
                # OR
                can_be_file = True
            else:
                print('>> UNSUPPORTED >>',url_path,url_query_params)

        else:
            print('>> UNSUPPORTED >>',url_path,url_query_params)
        
        return {'parse_op':parse_op,'can_be_file':can_be_file}
    
    def get_head(self, url):
        resph = self.session.head(url,allow_redirects=True)
        return resph
    
    def get_stream(self, url):
        return self.session.get(url, stream=True)

    def get(self, url:str):
        config_url = self.get_url_params(url)
        
        if (config_url['can_be_file']):
            resph = self.session.head(url,allow_redirects=True)
            if resph.url.startswith(self.loginURL):
                resph = self.authenticate(url,only_headers=True)
            
            # The way, how we decide is this a file ot not
            if not (resph.headers.get('X-Application-Context')): # This is a file
                return [resph.url]

        resp = self.session.get(url)

        if resp.url.startswith(self.loginURL):
            resp = self.authenticate(url)

        return config_url['parse_op'](resp.content.decode())
    
    def is_dirname(self,path):
        if (path == '.' or path == '..' or os.path.isdir(path)):
            path = os.path.join(path,'')
        return path[-1] == os.sep

    def get_local_filename(self,url,path):
        if self.is_dirname(path):
            resph = self.session.head(url,allow_redirects=True)
            #print('resph.url',resph.url)
            #print('resph.headers',resph.headers)

            if (resph.headers.get('content-disposition')):
                filename = [x[1].replace('"','') for x in [k.strip().split('=') for k in resph.headers.get('content-disposition').split(';')] if x[0] == 'filename'][0]
            else:
                filename = resph.url.split('/')[-1]
            return os.path.join(path,filename)
        else:
            return path
    
    def download(self, url:str, dest:str):
        file_name = self.get_local_filename(url,dest)
        print('Downloading to:', file_name)
        r = self.session.get(url, stream=True)
        with open(file_name, "wb") as f:
            total_length = r.headers.get('content-length')
            if total_length is None: # no content length header
                f.write(r.content)
                print('Complete!')
            else:
                dl = 0
                total_length = int(total_length)
                for chunk in r.iter_content(chunk_size=int(total_length/5000)):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                    dl += len(chunk)
                    printProgressBar(dl, total_length, prefix = 'Progress:', suffix = f'Complete ({int(total_length/1024/1024)} Mb)', length = 50)

    def authenticate(self, url, only_headers=False):

        # obtain token
        auth_data = {"login":self.login,"password":self.password,"serviceNick": url}
        payload = json.dumps(auth_data)
        resp = self.session.post(f"{self.loginURL}/rest/public/ticket/get",data=payload, headers={'Content-Type':'application/json'})
        if resp.status_code != 200:
            print(resp.status_code,resp.headers,resp.url, resp.json())
            return resp

        # login
        if (only_headers):
            resp = self.session.head("{loginURL}/ticket/auth?token={ticket}".format(loginURL=self.loginURL,**(resp.json())),headers={'Authentication':'Basic {}'.format(base64.b64encode("{}:{}".format(self.login,self.password).encode()).decode())},allow_redirects=True)
        else:
            resp = self.session.get("{loginURL}/ticket/auth?token={ticket}".format(loginURL=self.loginURL,**(resp.json())),headers={'Authentication':'Basic {}'.format(base64.b64encode("{}:{}".format(self.login,self.password).encode()).decode())})
        
        if resp.status_code != 200:
            print(resp.status_code,resp.headers,resp.url)
            return resp
        
        # save cookies to file
        with open(self.__saved_cookies_file, 'wb') as f:
            pickle.dump(self.session.cookies, f)
        
        return resp
