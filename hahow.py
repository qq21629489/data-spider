import requests
import pandas as pd
from tqdm import tqdm
from collections import Counter
def search_keyword(keyword='電子商務', page=0):
    # 設定課程資料欄位
    x = {
            'courseId': [],                     # course id(self-defining)
            'id' : [],                          # course id(website)
            'title' : [],                       # course name
            'titleDescription' : [],            # course description
            'owner' : [],                       # course owner
            'ownerDescription' : [],            # course owner description
            'videoLength' : [],                 # course video length(second)
            'students' : [],                     # course stuents
        }
    
    # 自定義id流水號
    count = 1
    
    # 此API上限一次可以回覆100筆(limit)相關課程，使用page可以控制回饋的頁碼，一直撈到撈不到資料為止
    # ex: keyword: ABC 共有 250 筆資料，page0~3可以撈完，page4停止
    while True:
        # API 網址
        url = f'https://api.hahow.in/api/products/search?category=COURSE&limit=100&page={page}&query={keyword}&sort=RELEVANCE'
        
        # request header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Referer': 'https://hahow.in/',
        }

        # 打API出去
        r = requests.get(url, headers=headers)
        
        # 有error(連線失敗、網址失效...)直接停止
        if r.status_code != requests.codes.ok:
            print('請求失敗', r.status_code)
            data = r.json()
            break
        
        # 課程資料儲存在 data > courseData > products中
        data = r.json()['data']['courseData']['products']

        # 若課程為0表示沒有課程資料了 停止搜尋
        if len(data) == 0:
            break
        # print(data)

        # 依序將要的資料取出來
        for d in data:
            # hahow的課程有三種狀態 PUBLISHED SUCCESS INCUBATING，只撈PUBLISHED，其他略過
            if d['status'] != 'PUBLISHED':
                continue
            # print(count)
            
            x['courseId'].append(f'A{count}')
            x['id'].append(d['_id'])
            x['title'].append(d['title'])
            x['titleDescription'].append(d['metaDescription'])
            x['owner'].append(d['owner']['name'])
            x['ownerDescription'].append(search_owner_detail(d['_id'])) # owner的詳細資料要在課程主頁面(main)才有，另外撈
            x['videoLength'].append(d['totalVideoLengthInSeconds'])
            x['students'].append(d['numSoldTickets'])
            
            count += 1
        page += 1

    res = pd.DataFrame(x)

    return res

def search_owner_detail(id='61e7f78a6d9e6f00067549ab'):
    url = f'https://api.hahow.in/api/courses/{id}?requestBackup=false'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
        'Referer': 'https://hahow.in/',
    }

    r = requests.get(url, headers=headers)
    if r.status_code != requests.codes.ok:
        print('請求失敗', r.status_code, id)
        data = r.json()
        return '' # owner description missing...
    
    data = r.json()
    detail = data['owner'].get('metaDescription', '') # 有些owner沒有像細資料欄為，用dict的get方法設預設值('')避免key error
    return detail # 回傳string

# page使用概念跟關鍵詞搜尋一樣
# courseId單純比較方便建立資料，也可以在外測做
def search_feedbacks(id_='61e7f78a6d9e6f00067549ab', page=0, courseId=''):
    x = {
        'courseId' : [],
        'rating' : [],
        'feedbackTopic' : [],
        'feedback' : []
    }
    
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
        if len(data) == 0:
            break
        
        # 實際跑的時候有出現撈不到值的狀況，這邊全部都採預設值，避免key error
        for d in data:
            x['courseId'].append(courseId)
            x['rating'].append(d.get('rating', -1))
            x['feedbackTopic'].append(d.get('title', ''))
            x['feedback'].append(d.get('description', ''))

        page += 1

    res = pd.DataFrame(x)
    return res

if __name__ == '__main__':
    # 設定搜尋關建詞
    keyword = '資料分析'   # 電子商務 資料分析
    
    # 撈取關鍵詞相關"課程資料"
    course_data = search_keyword(keyword=keyword)
    # print(course_data)
    
    # 輸出課程資料
    course_data.to_csv(f'hahow_{keyword}_course_data.csv', encoding="utf_8_sig", index=False)

    # 設定課程回饋欄位
    out = pd.DataFrame(columns=[
        'courseId',
        'rating',
        'feedbackTopic',
        'feedback'
    ])
    
    # 使用課程id依序撈取回饋資料
    for index, row in tqdm(course_data.iterrows()):
        id_ = row['id']
        courseId = row['courseId']
        
        # 撈取課程回饋資料
        feedbacks = search_feedbacks(id_=id_, courseId=courseId)
        
        # 合併不同課程回饋資料
        out = pd.concat([out, feedbacks])
    
    # 輸出課程回饋資料
    out.to_csv(f'hahow_{keyword}_feedback_data.csv', encoding='utf_8_sig', index=False)
    # print(out)






# 課程id, , 價格, 老師,  人數, 評論, 星等
# A          1    100  5     zxczxc 
# A          1    100  5
# A          1    100  5