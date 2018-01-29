import requests
import re
from lxml import etree
import logging


logging.basicConfig(
     filename='music163.log',
     level=logging.INFO,
     format='%(levelname)s:%(asctime)s:%(message)s')
logger = logging.getLogger("music163")
myheader = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    'Referer': 'https://music.163.com/',
    'Host': 'music.163.com',
    }

def get_music_list_from_collect(collect_id):
    # logger.info('creating )
    
    url = 'https://music.163.com/playlist?id=' + collect_id
    music_list = []
    collect_info = {}
    #try download list
    try:
        r= requests.get(url, headers = myheader)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except Exception as e:
        logger.warn(e)
        raise e

    text = r.text

    # with open('l.html', 'w') as f:
        # f.write(r.text)
    
    # collect info 
    collect_info['title'] = re.findall(r'(?<="title": ").*(?=")', text)[0]
    # collect_info['tags'] = re.findall(r'(?<=;cc)')

    html = etree.HTML(text)   
    m_list = html.xpath('//*[@id="song-list-pre-cache"]/ul/li')

    for li in m_list:
        # print(li.xpath('a')[0].text)
        res = get_music_info_by_id(re.findall(r"(?<=id=)\d*", li.xpath('a/@href')[0])[0])
        music_list.append(res)

    return [collect_info, music_list]

def get_music_info_by_id(music_id):
    # print(music_id)
    url = 'https://music.163.com/song?id=' + music_id 
    res = {}
    try:
        r = requests.get(url, headers = myheader)
        r.raise_for_status()
        r.encoding = r.apparent_encoding 
    except Exception as e:
        logger.warn(e)
        raise e
    
    res['artist'] = re.findall('(?<=description": "歌手：).*(?=。所)', r.text)[0].strip()
    res['title'] = re.findall(r'(?<=em class="f-ff2">).*(?=</em>)', r.text)[0].strip()
    # res['title'] = re.findall(r'(?<="title": ").*(?=")', r.text)[0]
    res['title'] = delete_par(res['title'])

    print(res) 
    return res

def get_collect_list():
    url = "https://music.163.com/weapi/user/playlist"

    payload = "params=rBm1q9CgTwsbso1R1L39ZY59K7jaQudB%2BraPC2AU%2FFsu2HyKL9%2Fm%2BzfR4i2lonArmaSQFzx7uc6rl56Z9eEg69khjLrWFYsaAkLpFLC42gqYcCS3rOZ9%2B2hpzKejIzZNSEf4GR3mvLCFOQze8pD96TLgd%2F7dm%2B7kq6S2ERcu64ioIuYAgi3qKKsrtfGriegY&encSecKey=634f3a16838ab2f9ab99c7564b67e9185db28d6cd1fd2f8501e935bb5caf864b3cab544f787a67559e9acb2698c5f8d81cb1bf62c2b3fa9acb4f54ebd58795846e24be49b2da91b387018850e53403a49c9947c82ccfbd02374c34391f7a00c07d1e8c9dd2a4dd25a743fd0ec21fa3fcbceb0e786677e9492944cc9556501b82"
    headers = {
        'cache-control': "no-cache",
        'postman-token': "58686916-6ad2-3bb1-090b-11723aa5be48",
        'content-type': "application/x-www-form-urlencoded"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    text = response.text 
    collectid_list = re.findall(r'(?<="id":)\d*', text)
    
    return collectid_list

def delete_par(title):
    l = len(title)

    while title[-1] == ')':
        cnt = 1
        for i in range(1,l+1):
            if title[-1-i] == '(':
                if cnt == 1:
                    title = title[0:-1-i]
                    title = title.strip()
                    break
                else:
                    ++cnt

            elif title[-1-i] == ')':
                ++cnt
   
    return title

if __name__ == '__main__':
    # print(get_music_list_from_collect('933087088'))
   # print(get_music_info_by_id('579954')) 
   print(get_collect_list())
