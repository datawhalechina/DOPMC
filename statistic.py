""" 
Datawhale仓库统计分析
使用说明请看下方__main__模块的注释
"""
import os
import datetime
import time
from collections import namedtuple, Counter
import requests
import json

GITHUB_KEY = os.getenv('GITHUB_KEY')


if GITHUB_KEY:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer {}".format(GITHUB_KEY),
        "X-GitHub-Api-Version": "2022-11-28"
    }
else:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }


def get_repos(org):
    """ 读取组织账户下的仓库列表 """
    url = 'https://api.github.com/orgs/'+ org + '/repos?per_page=100'

    remaining = True
    result = []
    while remaining:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            raise ValueError(res.text)
        header_link = res.headers.get('Link', '')
        res = res.json()
        result.extend(res)
        if 'rel="next"' in header_link:
            url = header_link.split('; rel="next"')[0][1:-1]
        else:
            remaining = False
    return result


def get_all_contributor_commit_activity(repo=''):
    """ 读取仓库下的所有成员的提交记录数 """
    url = 'https://api.github.com/repos/datawhalechina/' + repo + '/stats/contributors'
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise ValueError(res.text)
    res = res.json()
    return res




if __name__ == "__main__":
    # 统计起始时间点
    start_time = '2025-01-01 00:00:00'
    
    ### 华丽的分界线，分界线以下的代码不用关注 ###
    max_try_times = 3
    repos = get_repos('datawhalechina')
    repos = [x['name'] for x in repos]

    start_time_array = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    start_time_stamp = int(time.mktime(start_time_array))

    for repo in repos:
        res = []
        try_times = 0
        while True:
            if try_times > max_try_times:
                print('{}\t{}'.format(repo, 'get contributor commit fail'))
                break
            try:
                res = get_all_contributor_commit_activity(repo)
            except:
                time.sleep(1)
                try_times += 1
            else:
                break

        for item in res:
            author = item['author']
            weeks = item['weeks']
            total_a = 0
            total_d = 0
            total_c = 0
            for week in weeks:
                if week['w'] < start_time_stamp:
                    continue
                total_a += week['a']
                total_d += week['d']
                total_c += week['c']
            
            print('{}\t{}\t{}\t{}\t{}'.format(repo, author['login'], total_a, total_d, total_c))

