import os
import pandas as pd
# print(len(os.listdir('104data/url/')))
def get_job_id(url):
    job_id = url.split('/job/')[-1]
    if '?' in job_id:
        job_id = job_id.split('?')[0]
    return job_id

dir_list = os.listdir('104data/url/')
print(dir_list)
for d in dir_list:
    df = pd.read_csv(f'104data/url/{d}')
    df['id'] = df['url'].apply(get_job_id)
print(df)