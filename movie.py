import requests
import re
from dbs import Movie
from mongoengine import *
import json
from bson import binary
from mongoengine import *

def parse_html(url):
    # 反爬要加上header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}
    response = requests.get(url, headers=headers)
    text = response.text

    # print(text)

    # 正则匹配HTML爬取数据

    regix = '<div class="pic">.*?<em class="">(.*?)</em>.*?<img.*?src="(.*?)" class="">.*?div class="info.*?class="hd".*?class="title">(.*?)</span>.*?class="other">' \
            '(.*?)</span>.*?<div class="bd">.*?<p class="">.*?导演:(.*?)&nbsp.*?主演:(.*?)<br>(.*?)&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*?)</p>.*?class="star.*?<span class="(.*?)"></span>.*?' \
            'span class="rating_num".*?average">(.*?)</span>.*?<span>(.*?)</span>.*?class="quote">.*?class="inq">(.*?)</span>.*?</p>'

    results = re.findall(regix, text, re.S)
    for item in results:
        # down_image(item[1],headers=headers)
        yield {
            'name' : item[2] + ' ' + re.sub('&nbsp;','',item[3]),
            'author':re.sub('&nbsp;','',item[4].strip()),
            'actor': re.sub('&nbsp;', '', item[5].strip()),
            'score': item[10] ,
            'rank' : item[0],
            'people':re.sub('人评价','',item[11].strip()),
            'year':re.sub('\n','',item[6].strip()),
            'country':item[7],
            'type':re.sub('\n','',item[8].strip())
        }
        movie = {'name' : item[2] + ' ' + re.sub('&nbsp;','',item[3]),
                 'author':re.sub('&nbsp;','',item[4].strip()),
                 'actor': re.sub('&nbsp;', '', item[5].strip()),
                 'score': item[10] ,
                 'rank' : item[0],
                 'people':re.sub('人评价','',item[11].strip()),
                 'year':re.sub('\n','',item[6].strip()),
                 'country':item[7],
                 'type':re.sub('\n','',item[8].strip())}
        Movie(name = movie['name'],
              author=movie['author'],
              actor=movie['actor'],
              score=movie['score'],
              rank=movie['rank'],
              people=movie['people'],
              year=movie['year'],
              country=movie['country'],
              type=movie['type']).save()


    # print(yield)


def main():
    for offset in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start=' + str(offset) +'&filter='
        for item in parse_html(url):
            print(item)
            # write_movies_file(item)


# def down_image(url,headers):
#     r = requests.get(url,headers = headers)
#     filename = re.search('/public/(.*?)$',url,re.S).group(1)
#     with open(filename,'wb') as f:
#         f.write(r.content)


def star_transform(str):
    if str == 'rating5-t':
        return '5'
    elif str == 'rating45-t' :
        return '4.5'
    elif str == 'rating4-t':
        return '4'
    elif str == 'rating35-t' :
        return '3.5'
    elif str == 'rating3-t':
        return '3'
    elif str == 'rating25-t':
        return '2.5'
    elif str == 'rating2-t':
        return '2'
    elif str == 'rating15-t':
        return '1.5'
    elif str == 'rating1-t':
        return '1'
    else:
        return '0'


if __name__ == '__main__':
    connect('movies')
    main()






