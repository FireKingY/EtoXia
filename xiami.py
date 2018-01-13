import re
import time
import os
import requests
import json
import logging

logger = logging.getLogger("xiamiLoger")
myheader = {
        'host' : 'www.xiami.com',
        'User-Agent' : r'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Refer' : 'http://www.xiami.com'
        }

def login(session=requests.session()):
    gen_qr_url = 'https://login.xiami.com/member/generate-qrcodelogin?from=xiami&size=150&t='
    check_url_head = 'https://login.xiami.com/member/qrcodelogin?lgToken='
    check_url_tail = '&defaulturl=http%3A%2F%2Fwww.xiami.com%2F&t='
    t = str(int(time.time()*1000))
    gen_qr_url = gen_qr_url + t 

    #get qr_data
    try:
        r = session.get(gen_qr_url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except Exception as e:
        logger.error(e)
        raise e
        return

    qr_data = json.loads(r.text) 
    qr_url = 'https:' + qr_data['data']['url']
    lg_token = qr_data['data']['lgToken']

    #download qr_code
    try:
        r = session.get(qr_url)
        r.raise_for_status()
    except Exception as e:
        logger.error(e)
        raise e

    with open('qr_code.png','wb') as f:
        f.write(r.content)    
    
    #check login status
    while True:
        t = str(int(time.time()*1000))
        check_url = check_url_head + lg_token + check_url_tail + t
            
        try:
            r = session.get(check_url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
        except Exception as e:
            logger.warning(e)
            raise e 

        status_data = json.loads(r.text)   
        code = status_data['data']['code'] 
        if code == 10000:
            print('waiting for scan')
        elif code == 10004:
            print('QRcode expired')
            return
        elif code == 10001: 
            print(status_data['data']['message'] + ', please check it in your phone')
            # break
        else:
            print(status_data['data']['message'])
            break
        time.sleep(1.2)

    return session

def create_collect(session, collect_name):
    c_url = 'http://www.xiami.com/collect/createstep1'
    header = {
        'Host': 'www.xiami.com',
        'User-Agent':' Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Referer': 'http://www.xiami.com/collect/createstep1s',
        }

    #get data
    try:
        r = session.get(c_url, headers = myheader)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except Exception as e:
        logger.warning(e)
        raise e

    text = r.text
    token = re.findall(r'(?<=name="token" value=").*(?=">)', text)[0]
    _xiamitoken =re.findall(r'(?<=value=").*(?=" name="_xiamitoken")', text)[0]

    mydata = {            
        'name': collect_name,
        'type':'0',
        'public':'1',
        'des':'',
        'tags':'',
        'submit4':'保存',
        '_xiamitoken': _xiamitoken,
        'imgx':'0',
        'imgy':'0',
        'imgw':'300',
        'imgh':'300',
        'imgsrc':'',
        'updateimg':'0',
        'nosubject':'0',
        'token': token,
        '_xiamitoken': _xiamitoken,
        'searchkey':'',
        }

    #try create list
    try:
        r = session.post(c_url, headers = header, data = mydata)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except Exception as e:
        logger.warning(e)
        raise e

    collectid = re.findall(r"(?<=var cid = ').*(?=';)", r.text)
    return collectid
    

def add_music_to_collect(session, musicid, collectid):
    url = 'http://www.xiami.com/song/collect'
    collect_url = 'http://www.xiami.com/collect/' + collectid
    music_url = 'http://www.xiami.com/song/' + musicid
    header = {
        'Host': 'www.xiami.com',
        'User-Agent':' Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Referer': music_url,
        }

    #get data
    try:
        r = session.get(music_url,headers = myheader)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except Exception as e:
        logger.warn(e)
        raise e

    _xiamitoken =re.findall(r"(?<=_xiamitoken = ').*(?=';)", r.text)[0]
    mydata = {
        '_xiamitoken' : _xiamitoken,
        'id' : musicid,
        'list_id' : collectid,
        'tag_name' : '',
        'description' : '',
        'submit' : '保存',
        }

    #try add
    try:
        r = session.post(url, headers = header, data = mydata)
        r.raise_for_status()
    except Exception as e:
        logger.warn(e)
        raise e
    return r

if __name__ == "__main__":
    login()
