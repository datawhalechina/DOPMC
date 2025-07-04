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
import sys
from whale_coin import get_commits

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

if __name__ == "__main__":
    # 统计起始时间点
    start_time = '2025-04-01T00:00:00Z'
    end_time = '2025-07-01T00:00:00Z'
    
    ### 华丽的分界线，分界线以下的代码不用关注 ###
    ok_repo = set()
    with open('github_statistic_out.tsv') as f:
        for line in f:
            repo = line.split('\t')[0].strip()
            ok_repo.add(repo)
    repos = get_repos('datawhalechina')
    print('{}\t{}'.format('total repos:', len(repos)), file=sys.stderr)
    repos = [x['name'] for x in repos if not x['private']]
    print('{}\t{}'.format('public repos:', len(repos)), file=sys.stderr)
    print('{}\t{}'.format('already repos:', len(ok_repo)), file=sys.stderr)
    
    

    max_try_times = 3
    for repo in repos:
        if repo in ok_repo:
            continue
        
        author_cnt = {}
        commits = []
        try_times = 0
        while True:
            if try_times > max_try_times:
                print('{}\t{}'.format(repo, 'get contributor commit fail'), file=sys.stderr)
                break
            try:
                commits = get_commits(repo=repo, since=start_time, until=end_time)
            except:
                time.sleep(1)
                try_times += 1
            else:
                break
        
        outputs = []
        for cmt in commits:
            sha = cmt['sha']
            if cmt['author']:
                author_name = cmt['author']['login']
            else: # 贡献者修改了用户名导致author字段为空则用历史的用户名
                author_name = cmt['commit']['author']['name']

            if author_name not in author_cnt:
                author_cnt[author_name] = {
                    'commits': []
                }

            author_cnt[author_name]['commits'].append({'repo': repo, 'url': cmt['html_url']})
        
        for author_name in author_cnt:
            print(f'{repo}\t{author_name}\t{len(author_cnt[author_name]['commits'])}', flush=True)
