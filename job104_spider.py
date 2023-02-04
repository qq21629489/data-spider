import time
import random
import requests
import pandas as pd
from tqdm import tqdm

# 詳細實作參考下面網址，這邊基本上是直接複製過來的：） 只做少部分資料需求的更改，沒有改邏輯
# https://blog.jiatool.com/posts/job104_spider/

class Job104Spider():
    def search(self, keyword, max_mun=10, filter_params=None, sort_type='符合度', is_sort_asc=False):
        """搜尋職缺"""
        jobs = []
        total_count = 0

        url = 'https://www.104.com.tw/jobs/search/list'
        query = f'ro=0&kwop=7&keyword={keyword}&expansionType=area,spec,com,job,wf,wktm&mode=s&jobsource=2018indexpoc'
        # https://www.104.com.tw/jobs/search/?keyword=%E9%9B%BB%E5%AD%90%E5%95%86%E5%8B%99&area=6001001000&jobsource=2018indexpoc&ro=0
        if filter_params:
            # 加上篩選參數，要先轉換為 URL 參數字串格式
            query += ''.join([f'&{key}={value}' for key,
                             value, in filter_params.items()])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Referer': 'https://www.104.com.tw/jobs/search/',
        }

        # 加上排序條件
        sort_dict = {
            '符合度': '1',
            '日期': '2',
            '經歷': '3',
            '學歷': '4',
            '應徵人數': '7',
            '待遇': '13',
        }
        sort_params = f"&order={sort_dict.get(sort_type, '1')}"
        sort_params += '&asc=1' if is_sort_asc else '&asc=0'
        query += sort_params

        page = 1
        while len(jobs) < max_mun:
            print('processing....', len(jobs))
            params = f'{query}&page={page}'
            r = requests.get(url, params=params, headers=headers)
            if r.status_code != requests.codes.ok:
                print('請求失敗', r.status_code)
                data = r.json()
                print(data['status'], data['statusMsg'], data['errorMsg'])
                break

            data = r.json()
            total_count = data['data']['totalCount']
            jobs.extend(data['data']['list'])

            if (page == data['data']['totalPage']) or (data['data']['totalPage'] == 0):
                break
            page += 1
            time.sleep(random.uniform(3, 5))

        return total_count, jobs[:max_mun]

    def get_job(self, job_id):
        """取得職缺詳細資料"""
        url = f'https://www.104.com.tw/job/ajax/content/{job_id}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Referer': f'https://www.104.com.tw/job/{job_id}'
        }

        r = requests.get(url, headers=headers)
        if r.status_code != requests.codes.ok:
            print('請求失敗', r.status_code)
            return

        data = r.json()
        return data['data']

    def search_job_transform(self, job_data):
        """將職缺資料轉換格式、補齊資料"""
        # appear_date = job_data['appearDate']
        # apply_num = int(job_data['applyCnt'])
        # company_addr = f"{job_data['jobAddrNoDesc']} {job_data['jobAddress']}"

        job_url = f"https:{job_data['link']['job']}"
        # job_company_url = f"https:{job_data['link']['cust']}"
        # job_analyze_url = f"https:{job_data['link']['applyAnalyze']}"

        job_id = job_url.split('/job/')[-1]
        if '?' in job_id:
            job_id = job_id.split('?')[0]

        # salary_high = int(job_data['salaryLow'])
        # salary_low = int(job_data['salaryHigh'])

        # job = {
        #     # 'job_id': job_id,
        #     # 'type': job_data['jobType'],
        #     # 'name': job_data['jobName'],  # 職缺名稱
        #     # # 'desc': job_data['descSnippet'],  # 描述
        #     # 'appear_date': appear_date,  # 更新日期
        #     # 'apply_num': apply_num,
        #     # 'apply_text': job_data['applyDesc'],  # 應徵人數描述
        #     # 'company_name': job_data['custName'],  # 公司名稱
        #     # 'company_addr': company_addr,  # 工作地址
        #     # 'job_url': job_url,  # 職缺網頁
        #     # 'job_analyze_url': job_analyze_url,  # 應徵分析網頁
        #     # 'job_company_url': job_company_url,  # 公司介紹網頁
        #     # 'lon': job_data['lon'],  # 經度
        #     # 'lat': job_data['lat'],  # 緯度
        #     # 'education': job_data['optionEdu'],  # 學歷
        #     # 'period': job_data['periodDesc'],  # 經驗年份
        #     # 'salary': job_data['salaryDesc'],  # 薪資描述
        #     # 'salary_high': salary_high,  # 薪資最高
        #     # 'salary_low': salary_low,  # 薪資最低
        #     # 'tags': job_data['tags'],  # 標籤
        # }
        return job_id

    def job_detail_transform(self, data):
        # job_name = data['header']['jobName']
        # cust_name = data['header']['custName']
        # job_detail = data['jobDetail']['jobDescription']
        # address_area = data['jobDetail']['addressArea']
        # salary_min = data['jobDetail']['salaryMin']
        # salary_max = data['jobDetail']['salaryMax']
        # work_exp = data['condition']['workExp']
        # major = ' '.join(data['condition']['major'])
        # edu = data['condition']['edu']
        # language = ', '.join([x['language'] + ':' + x['ability']
        #                      for x in data['condition']['language']])
        # localLanguage = ', '.join(
        #     [x['language'] + ':' + x['ability'] for x in data['condition']['localLanguage']])
        # specialty = ', '.join(x['description']
        #                       for x in data['condition']['specialty'])
        # skill = ', '.join(x['description'] for x in data['condition']['skill'])
        # other = data['condition']['other']
        
        x = {
            'job_name' : data['header']['jobName'],
            'cust_name' : data['header']['custName'],
            'appear_date' : data['header']['appearDate'],
            'job_detail' : data['jobDetail']['jobDescription'],
            'address_area' : data['jobDetail']['addressArea'],
            'salary_min' : data['jobDetail']['salaryMin'],
            'salary_max' : data['jobDetail']['salaryMax'],
            'work_exp' : data['condition']['workExp'],
            'major' : ' '.join(data['condition']['major']),
            'edu' : data['condition']['edu'],
            'language' : ', '.join([x['language'] + ':' + x['ability']
                                for x in data['condition']['language']]),
            'localLanguage' : ', '.join(
                [x['language'] + ':' + x['ability'] for x in data['condition']['localLanguage']]),
            'specialty' : ', '.join(x['description']
                                for x in data['condition']['specialty']),
            'skill' : ', '.join(x['description'] for x in data['condition']['skill']),
            'other' : data['condition']['other'],
        }
        

        # print(job_name)
        # print(cust_name)
        # print(job_detail)
        # print(address_area)
        # print(salary_min)
        # print(salary_max)
        # print(work_exp)
        # print(major)
        # print(edu)
        # print(language)
        # print(localLanguage)
        # print(specialty)
        # print(skill)
        # print(other)

        res = pd.DataFrame(x, index=[0])
        return res


if __name__ == "__main__":
    job104_spider = Job104Spider()

    class_dict = {
        2004000000: '行銷企劃專案管理類',
        2007000000: '資訊軟體系統類'
    }
    
    code = 2007000000
    
    filter_params = {
        'jobcat': code, # 2004000000 行銷企劃專案管理類, 2007000000 資訊軟體系統類
        # 'area': '6001001000,6001016000',  # (地區) 台北市,高雄市
        # 's9': '1,2,4,8',  # (上班時段) 日班,夜班,大夜班,假日班
        # 's5': '0',  # 0:不需輪班 256:輪班
        # 'wktm': '1',  # (休假制度) 週休二日
        # 'isnew': '0',  # (更新日期) 0:本日最新 3:三日內 7:一週內 14:兩週內 30:一個月內
        # 'jobexp': '1,3,5,10,99',  # (經歷要求) 1年以下,1-3年,3-5年,5-10年,10年以上
        # 'newZone': '1,2,3,4,5',  # (科技園區) 竹科,中科,南科,內湖,南港
        # 'zone': '16',  # (公司類型) 16:上市上櫃 5:外商一般 4:外商資訊
        # 'wf': '1,2,3,4,5,6,7,8,9,10',  # (福利制度) 年終獎金,三節獎金,員工旅遊,分紅配股,設施福利,休假福利,津貼/補助,彈性上下班,健康檢查,團體保險
        # 'edu': '1,2,3,4,5,6',  # (學歷要求) 高中職以下,高中職,專科,大學,碩士,博士
        # 'remoteWork': '1',  # (上班型態) 1:完全遠端 2:部分遠端
        # 'excludeJobKeyword': '科技',  # 排除關鍵字
        # 'kwop': '1',  # 只搜尋職務名稱
    }
    total_count, jobs = job104_spider.search('', max_mun=5000, filter_params=filter_params)

    # print('搜尋結果職缺總數：', total_count)
    # # print(len(jobs))
    jobs = [job104_spider.search_job_transform(job) for job in jobs]
    # print(jobs)

    out = pd.DataFrame(columns=['job_name','cust_name', 'appear_date','job_detail', 'address_area', 'salary_min', 'salary_max',
                       'work_exp', 'major', 'edu', 'language', 'localLanguage', 'specialty', 'skill', 'other'])

    for j in tqdm(jobs):
        job_info = job104_spider.get_job(j)
        res = job104_spider.job_detail_transform(job_info)
        out = pd.concat([out, res])
    out.to_csv(f'104_{class_dict[code]}_data.csv', encoding="utf_8_sig", index=False)
    