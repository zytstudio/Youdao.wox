import http.client
import json
import urllib
import webbrowser
import time
import hashlib
import uuid
from configparser import ConfigParser

from wox import Wox, WoxAPI


class Main(Wox):
    __HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    __EMPTY_RESULT = [{
        'Title': 'Start to translate between Chinese and English',
        'SubTitle': 'Powered by youdao api, Python3.x only.',
        'IcoPath': 'img\\youdao.ico'
    }]
    __SERVER_DOWN = [{
        'Title': '网易在线翻译服务暂不可用',
        'SubTitle': '请待服务恢复后再试',
        'IcoPath': 'img\\youdao.ico'
    }]
    __NETWORK_ERROR = [{
        'Title': '网络请求失败',
        'SubTitle': '请检查网络连接是否正常',
        'IcoPath': 'img\\youdao.ico'
    }]
    __NO_KEY = [{
        'Title': '未填写Key',
        'SubTitle': '请在key.ini中的key中填写app_key与app_secret',
        'IcoPath': 'img\\youdao.ico'
    }]

    def __init__(self):
        self.__hash_object = hashlib.sha256()
        self.__error_codes: dict = {}
        self.__load_error_codes()
        self.__app_key = ""
        self.__app_secret = ""
        self.__load_key()
        Wox.__init__(self)

    def __load_error_codes(self):
        try:
            with open('error_codes.json', 'r', encoding='utf-8') as file:
                self.__error_codes = json.load(file)
        except:
            self.__error_codes = {}

    def __load_key():
        try:
            conf = ConfigParser()
            conf.read("key.ini")
            self.__app_key = conf.get("key", "app_key")
            self.__app_secret = conf.get("key", "app_secret")
        except:
            self.__app_key = ""
            self.__app_secret = ""
    
    def query(self, param: str) -> list:
        q = param.strip()
        if not q:
            return self.__EMPTY_RESULT

        if not (self.__app_key and self.__app_secret):
            return self.__NO_KEY
        
        response = self.__translate_api(q)
        if not response:
            return self.__NETWORK_ERROR

        error_code = response.get('errorCode', None)
        if not error_code:
            return self.__SERVER_DOWN
        
        if error_code != "0":
            return [{
                "Title": self.__error_codes.get(error_code, "未知错误"),
                "SubTitle": "errorCode=%s" % error_code,
                "IcoPath": "img\\youdao.ico"
            }]
        
        translations = response.get('translation', [])
        speak_url = response.get('tSpeakUrl', '')
        web_dict = response.get('webdict', '')
        
        result: list = []
        if translations:
            for translation in translations:
                result.append({
                    'Title': translation,
                    'SubTitle': '有道翻译',
                    'IcoPath': 'img\\youdao.ico',
                    'JsonRPCAction': {
                        'method': 'open_url',
                        'parameters': [web_dict.get('url', '')]
                    }
                })
        
        if speak_url:
            result.append({
                'Title': '获取发音',
                'SubTitle': '点击可跳转 - 有道翻译',
                'IcoPath': 'img\\youdao.ico',
                'JsonRPCAction': {
                    'method': 'open_url',
                    'parameters': [speak_url]
                }
            })
        return result

    def open_url(self, url: str) -> str:
        if url:
            webbrowser.open(url)

    def __get_sign(self, q: str, salt: str, cur_time: str) -> str:
        input_str = ""
        if len(q) <= 20:
            input_str = q
        else:
            input_str = q[:10] + str(len(q)) + q[-10:]
        self.__hash_object.update((self.__app_key + input_str + salt + cur_time + self.__app_secret).encode('utf-8'))
        return str(self.__hash_object.hexdigest())
        
    def __translate_api(self, q: str):
        cur_time = str(int(time.time()))
        salt = str(uuid.uuid1())
        sign = self.__get_sign(q, salt, cur_time)
        data = {
            "q": q,
            "from": "auto",
            "to": "zh-CHS",
            "appKey": self.__app_key,
            "salt": salt,
            "sign": sign,
            "signType": "v3",
            "curtime": cur_time
        }
        payload = urllib.parse.urlencode(data).encode('utf-8')

        try:
            conn = http.client.HTTPSConnection("openapi.youdao.com")
            conn.request("POST", "/api", body=payload, headers=self.__HEADERS)
            response = conn.getresponse()
            if response.code == 200:
                return json.loads(response.read().decode("utf-8"))
            return None
        except:
            return None
        finally:
            if conn:
                conn.close()
                
    def __get_proxies(self):
        proxies = {}
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies["http"] = "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))
            proxies["https"] = "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))
        return proxies


if __name__ == '__main__':
    Main()
