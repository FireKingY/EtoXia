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
    
    res['artist'] = re.findall('(?<="description": ").*(?=。所)', r.text)[0]
    res['title'] = re.findall(r'(?<="title": ").*(?=")', r.text)[0]
    print(res) 
    return res

if __name__ == '__main__':
    print(get_music_list_from_collect('933087088'))
   # print(get_music_info_by_id('33916691')) 
