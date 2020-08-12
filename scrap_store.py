from dbs import Planet
from bs4 import BeautifulSoup
from mongoengine import *
import requests
import time
import pprint
import re
import csv
import os
headers_all = []
#数据库这部分也还没用到
name=['Mass','Volume','Equatorial','radius','Polar radius',
      'Volumetric mean radius','Ellipticity','Mean density',
      'Surface gravity','Surface acceleration','Escape velocity','GM','Bond albed',
      'Geometric albed','V-band magnitude V','Solar irradiance','Black-body temperature',
      'Topographic range','Moment of inertia','J2','Number of natural satellite','Planetary ring syste',
      'Semimajor axis','Sidereal orbit period','Tropical orbit period','Perihelion','Aphelion','Synodic period',
      'Mean orbital velocity','Max. orbital velocity','Min. orbital velocity','Orbit inclination','Orbit eccentricit',
      'Sidereal rotation period','Length of day','Obliquity to orbit','Inclination of equator','planet_name'
     ]

def from_dict_to_planet(the_planet_dict):
    # 存进数据库对应字段
    return Planet(mass=the_planet_dict['Mass'],
                  volume=the_planet_dict['Volume'],
                  e_radius=the_planet_dict['Equatorial radius'],
                  p_radius =the_planet_dict['Polar radius'],
                  v_mean_radius=the_planet_dict['Volumetric mean radius'],
                  ellipticity=the_planet_dict['Ellipticity'],
                  m_density=the_planet_dict['Mean density'],
                  s_gravity=the_planet_dict['Surface gravity'],
                  s_acceleration=the_planet_dict['Surface acceleration'],
                  e_velocity=the_planet_dict['Escape velocity'],
                  GM=the_planet_dict['GM'],
                  b_albedo=the_planet_dict['Bond albed'],
                  g_albedo=the_planet_dict['Geometric albed'],
                  v_band=the_planet_dict['V-band magnitude V'],
                  s_irradiance=the_planet_dict['Solar irradiance'],
                  black_body=the_planet_dict['Black-body temperature'],
                  t_range=the_planet_dict['Topographic range'],
                  m_inertia=the_planet_dict['Moment of inertia'],
                  J2=the_planet_dict['J2'],
                  s_axis=the_planet_dict['Semimajor axis'],
                  s_o_period=the_planet_dict['Sidereal orbit period'],
                  t_period=the_planet_dict['Tropical orbit period'],
                  Perihelion=the_planet_dict['Perihelion'],
                  Aphelion=the_planet_dict['Aphelion'],
                  Sy_period=the_planet_dict['Synodic period'],
                  Mean_velocity=the_planet_dict['Mean orbital velocity'],
                  Max_velocity=the_planet_dict['Max. orbital velocity'],
                  Min_velocity=the_planet_dict['Min. orbital velocity'],
                  o_inclination=the_planet_dict['Orbit inclination'],
                  o_eccentricity=the_planet_dict['Orbit eccentricit'],
                  s_r_period=the_planet_dict['Sidereal rotation period'],
                  l_o_day=the_planet_dict['Length of day'],
                  o_t_o=the_planet_dict['Obliquity to orbit'],
                  i_o_e=the_planet_dict['Inclination of equator'],
                  )



def try_request(url):
    page_response = requests.request('GET', url)
    wait_time = 2
    while page_response.status_code == 429:
        print(f"Got 429, sleeping for {wait_time} seconds.. ")
        # time.sleep(int(page_response.headers["Retry-After"]))
        page_response = requests.request('GET', url)
        time.sleep(wait_time)
        wait_time = wait_time * 2
    print(page_response, page_response.content)
    return page_response

# 从第一个网页找接下来的html网址
def get_page_link(base_url):
    print(f"page_url = {base_url}")
    page_response = try_request(f"{base_url}")
    page_soup = BeautifulSoup(page_response.content, 'html.parser')
    # 只有一个table
    html_table = page_soup.find('table')
    url_list = html_table.find_all('a')
    # pprint.pprint(url_list)
    url_next = []
    # 清除不必要的html
    for url in url_list:
        abandon = f" {url['href']}"
        #print(f" {url['href']}")
        ret = re.findall('#', abandon)
        if not bool(len(ret)) and abandon.strip() not in url_next:
            url_next.append(abandon.strip())
    # for url in url_next:
    #     get_planet_data(base_url, url)
            # print(1)
    pprint.pprint(url_next)
    for url in url_next:
        if url != 'earthfact.html':
            get_planet_data(base_url, url)

    pprint.pprint(url_next)

#爬具体的数据
def get_planet_data(base_url, next_url):
    # 很多print的地方都是调试看结果
    print(f"page_url = {base_url}{next_url}")
    # 尝试获取html 只有一个请求 服务器暂时不会拒绝
    page_response = try_request(f"{base_url}{next_url}")
    # headers
    global headers_all

    # 先爬取整个html
    page_soup = BeautifulSoup(page_response.content, 'html.parser')
    # print(page_soup)
    html_table = page_soup.find('table')
    #print(html_table)
    next_table = html_table.find_next('table')

    # print(next_table)

    # 下面的部分就是取具体的字段和对应的数据
    planet_dictionary = {}
    rows = html_table.findChildren('tr')
    rows_another = next_table.findChildren('tr')
    rows_sum = rows + rows_another
    # print(rows_sum)
    abandon_words = {'Mercury', 'Earth', 'Ratio'}  # 这里的具体星球名要取出来再去掉
    # print(rows)
    planet_name = {}

    for row in rows_sum:
        cells = row.findChildren('th')
        data = row.find_all('td')
        for cell in cells:
            true_text = cell.text[:cell.text.find('(')].strip()  # 可以试试如果去掉这一步，然后下面true_text都用cell.text会怎样
            # if true_text not in abandon_words:

            # 存储星球的名字
            if cell['align'] == "center" and not bool(planet_name):
                planet_name["planet_name"] = cell.text.strip()
                print(cell.text.strip())
            if cell['align'] != "center" and true_text not in planet_dictionary and true_text not in abandon_words:
                planet_dictionary[true_text] = data[0].text
    print(planet_name)
    # 合并字典（有更简单的方法）
    for m, n in planet_name.items():
        planet_dictionary[m] = n
    pprint.pprint(planet_dictionary)
    for m in name:
        if m not in planet_dictionary.keys():
            planet_dictionary[m] = 'null'
    from_dict_to_planet(planet_dictionary).save()
    # path = r'C:\Users\79221\Desktop\project\mentor_session_1\test.txt'
    # f = open(path, 'a', encoding='utf-8')  # 以'w'方式打开文件
    # for k, v in planet_dictionary.items():  # 遍历字典中的键值
    #     s2 = str(v)  # 把字典的值转换成字符型
    #     f.write(k + '\n')  # 键和值分行放，键在单数行，值在双数行
    #     f.write(s2 + '\n')
    # f.close()
    # if not bool(len(headers_all)):
    #     headers_all = planet_dictionary.keys()
    # headers = list(headers_all)
    # if not os.path.exists('test.csv'):
    #     with open('test.csv', "w", newline='', encoding='utf-8') as csvfile:  # newline='' 去除空白行
    #         writer = csv.DictWriter(csvfile, fieldnames=headers)  # 写字典的方法
    #         writer.writeheader()
    # with open('test.csv', "a", newline='', encoding='utf-8') as csvfile:  # newline='' 一定要写，否则写入数据有空白行
    #     writer = csv.DictWriter(csvfile, fieldnames=headers)
    #     writer.writerow(planet_dictionary)  # 按行写入数据
    #     print("^_^ write success")


    # if not bool(len(headers_all)):
    #     headers_all = planet_dictionary.keys()
    # headers = list(headers_all)
    # print(headers)
    # # print(list(headers_all))
    # rows = []


    # with open('test.csv', 'a', newline='', encoding='utf-8') as f:
    #     writer = csv.writer(f)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
    #     writer.writerow(headers_all)  # 写入列名
    #     writer.writerows(rows)  # 写入数据
    # return planet_dictionary


if __name__ == "__main__":
    # Connect to the database
    connect('planets')

    # Crawl the webpage
    base_url = 'https://nssdc.gsfc.nasa.gov/planetary/factsheet/'
    #sub_url_to_crawl = ''
    # Crawl the page:
    #while sub_url_to_crawl is not None:
        #sub_url_to_crawl = parse_page(sub_url_to_crawl, base_url)
    url_to_crawl = get_page_link(base_url)
