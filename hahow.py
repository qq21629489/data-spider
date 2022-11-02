import requests
import pandas as pd
import time
import random
# https://api.hahow.in/api/products/search?category=COURSE&limit=24&page=0&query=%E9%9B%BB%E5%AD%90%E5%95%86%E5%8B%99&sort=RELEVANCE
# 
def search_keyword(keyword='電子商務', page=0):
    while True:
        x = {
            'id' : [],
            'title' : [],
            'metaDescription' : [],
            'owner' : [],
            'totalVideoLengthInSeconds' : [],
            'numSoldTickets' : [],
        }


        url = f'https://api.hahow.in/api/products/search?category=COURSE&limit=100&page={page}&query={keyword}&sort=RELEVANCE'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Referer': 'https://hahow.in/',
        }

        r = requests.get(url, headers=headers)
        if r.status_code != requests.codes.ok:
            print('請求失敗', r.status_code)
            data = r.json()
            return
        data = r.json()['data']['courseData']['products']

        if len(data) == 0:
            break
        print(data[0])

        for d in data:
            x['id'].append(d['_id'])
            x['title'].append(d['title'])
            x['metaDescription'].append(d['metaDescription'])
            x['owner'].append(d['owner']['name'])
            x['totalVideoLengthInSeconds'].append(d['totalVideoLengthInSeconds'])
            x['numSoldTickets'].append(d['numSoldTickets'])

        page += 1

    res = pd.DataFrame(x)

    return res

def search_feedbacks(id_='61e7f78a6d9e6f00067549ab', page=0):
    x = {
        'rating' : [],
        'feedBackTopic' : [],
        'feedback' : []
    }
    total_count = 0
    while True:
        url = f'https://api.hahow.in/api/courses/{id_}/feedbacks?limit=20&page={page}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Referer': 'https://hahow.in/',
        }

        r = requests.get(url, headers=headers)
        if r.status_code != requests.codes.ok:
            print('請求失敗', r.status_code)
            data = r.json()
            break

        data = r.json()
        # print(len(data))

        total_count += len(data)
        if len(data) == 0:
            break

        for d in data:
            x['rating'].append(d['rating'])
            x['feedBackTopic'].append(d['title'])
            x['feedback'].append(d['description'])

        page += 1

    print(total_count)
    res = pd.DataFrame(x)
    print(res)
    return res



if __name__ == '__main__':    
    # ids = search_keyword()
    # # print(len(ids))
    # c = 0
    # print(ids[0])
    
    search_feedbacks(id_='597df7e2acc137070007013c')
    # for i in ids:
    #     total_count = search_feedbacks(id_=i)
    #     c += total_count
    # print(c)


# 課程id, , 價格, 老師,  人數, 評論, 星等
# A          1    100  5     zxczxc 
# A          1    100  5
# A          1    100  5