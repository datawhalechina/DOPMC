""" 
Datawhale开源项目鲸币奖励计算
使用说明请看下方__main__模块的注释
"""
import os
import datetime
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


def get_commits(repo, username=''):
    """ 读取commit记录 """
    url = 'https://api.github.com/repos/datawhalechina/'+ repo + '/commits'
    if username:
        url += '?author=' + username + '&per_page=100'
    else:
        url += '?per_page=100'

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


def get_pr(repo, commit_sha):
    """ 读取pull request记录 """
    url = 'https://api.github.com/repos/datawhalechina/' + repo + '/commits/'+ commit_sha + '/pulls'
    url += '?per_page=100'
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise ValueError(res.text)
    res = res.json()
    return res


def get_stars(repo):
    """ 读取仓库的star数 """
    url = 'https://api.github.com/repos/datawhalechina/' + repo + ''
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise ValueError(res.text)
    res = res.json()
    return res['stargazers_count']


def compute_coins(cmts, prs):
    """ 计算参与贡献的项目奖励的鲸币数量 """
    # 计算通过commit获得的鲸币
    date_cmt = {}
    cmts_coins = 0
    for cmt in cmts:
        date = cmt.date.split('T')[0]
        if date not in date_cmt:
            date_cmt[date] = []
        date_cmt[date].append(cmt)
    
    if date_cmt:
        print('根据Commit记录计算您参与贡献的项目的的奖励明细如下：\n日期\t明细\t鲸币数量')
        out_list = []
        for date in date_cmt:
            total_coins = len(set([x.repo for x in date_cmt[date]]))
            cmts_coins += total_coins
            
            details = []
            for item in date_cmt[date]:
                details.append('{}您在{}提交了Commit：{}（{}）'.format(item.date, item.repo, item.title, item.url))

            out_list.append((date, ','.join(details), str(total_coins)))

        out_list_sorted = sorted(out_list, key=lambda x: x[0], reverse=True)
        for out in out_list_sorted:
            print('\t'.join(out))

    # 计算通过pull request获得的鲸币
    date_pr = {}
    prs_coins = 0
    for pr in prs:
        date = pr.date.split('T')[0]
        if date not in date_pr:
            date_pr[date] = []
        date_pr[date].append(pr)

    if date_pr:
        print('根据Pull Request记录计算您参与贡献的项目的奖励明细如下：\n日期\t明细\t鲸币数量')
        out_list = []
        for date in date_pr:
            cnt = Counter([x.label for x in date_pr[date]])
            enhancement_coins = cnt['enhancement'] * 3
            bug_coins = cnt['bug'] * 1
            total_coins = enhancement_coins + bug_coins
            prs_coins += total_coins

            details = []
            for item in date_pr[date]:
                details.append('{}您在{}提交了类型为{}的Pull Request：{}（{}）'.format(item.date, item.repo, item.label, item.title, item.url))

            out_list.append((date, ','.join(details), str(total_coins)))

        out_list_sorted = sorted(out_list, key=lambda x: x[0], reverse=True)
        for out in out_list_sorted:
            print('\t'.join(out))
        

    return cmts_coins, prs_coins
    
    
def compute_owner_coins(cmts, stars):
    """ 计算所负责的项目所奖励的鲸币数量 """
    # 计算通过commit获得的鲸币
    date_cmt = {}
    for cmt in cmts:
        repo = cmt['html_url'].split('/')[-3]
        date = cmt['commit']['author']['date'].split('T')[0]
        if date not in date_cmt:
            date_cmt[date] = set()
        date_cmt[date].add(repo)
    
    cmts_coins = 0
    if date_cmt:
        print('根据Commit记录计算您所负责的项目的奖励明细如下：\n日期\t明细\t鲸币数量')
        out_list = []
        for date in date_cmt:
            total_coins = len(date_cmt[date])
            cmts_coins += total_coins
            details = '{}有Commit记录的项目共有{}个：{}'.format(date, len(date_cmt[date]), '、'.join(date_cmt[date]))
            out_list.append((date, details, str(total_coins)))

        out_list_sorted = sorted(out_list, key=lambda x: x[0], reverse=True)
        for out in out_list_sorted:
            print('\t'.join(out))
    
    # 计算通过star获得的鲸币
    stars_coins = 0
    print('根据Star数计算您所参与和负责的项目的奖励明细如下：\n日期\t明细\t鲸币数量')
    stages = {1000, 10000}
    for star in stars:
        repo, style, star_num = star
        if star_num < min(stages):
            details = '{}的star数为{}尚未达到奖励标准'.format(repo, star_num)
            print('\t'.join([datetime.datetime.today().strftime('%Y-%m-%d'), details, '0']))
            continue

        for stage in stages:
            if star_num >= stage:
                if style == 'contributor':
                    stars_coins += 5
                    details = '{}的Star数超过{}，作为贡献者奖励5鲸币'.format(repo, stage)
                    print('\t'.join([datetime.datetime.today().strftime('%Y-%m-%d'), details, '5']))
                
                if style == 'owner':
                    stars_coins += 100
                    details = '{}的Star数超过{}，作为项目负责人奖励100鲸币'.format(repo, stage)
                    print('\t'.join([datetime.datetime.today().strftime('%Y-%m-%d'), details, '100']))
    
    return cmts_coins, stars_coins


if __name__ == "__main__":
    # 使用说明：
    # 1. 将以下的【username、repos、owner_repos】改写为你的信息
    # 2. 执行【python3 whale-coin.py > res.txt】命令
    # 3. 将【res.txt】中的内容复制，然后打开一个空白excel文档，粘贴即可查看明细

    # GitHub用户名
    username = 'Sm1les'

    # 参与贡献的项目
    repos = set(['joyful-pandas', 'easy-rl'])

    # 所负责的项目
    owner_repos = set(['pumpkin-book'])

    ######## 这里是华丽的分界线，分界线以下的代码请勿改动 ########

    # 参与贡献的项目和所负责的项目不可重复
    if not repos.isdisjoint(owner_repos):
        raise ValueError('参与贡献的项目和所负责的项目请分开填写，不能有交集~')

    # 读取参与贡献的项目提交记录
    Commit = namedtuple('Commit', 'repo title url date')
    Pullrequest = namedtuple('Pullrequest', 'repo label title url date')

    cmts = set()
    prs = set()

    real_repos = set()

    for repo in repos:
        commits = get_commits(repo, username)
        for cmt in commits:
            sha = cmt['sha']
            real_repos.add(cmt['html_url'].split('/')[-3])
            pr = get_pr(repo, sha)

            if not pr:
                # 无对应PR的commit
                cmts.add(Commit(repo, cmt['commit']['message'], cmt['html_url'], cmt['commit']['author']['date']))
            else:
                # 有对应PR的commit
                for item in pr:
                    labels = set([x['name'] for x in item['labels']])

                    if not labels or 'enhancement' in labels:
                        prs.add(Pullrequest(repo, 'enhancement', item['title'], item['html_url'], item['merged_at']))
                    
                    if 'bug' in labels:
                        prs.add(Pullrequest(repo, 'bug', item['title'], item['html_url'], item['merged_at']))
    
    # 修正参与贡献的项目
    repos = real_repos

    # 计算参与贡献的项目所奖励的鲸币数量
    cmts_coins, prs_coins = compute_coins(cmts, prs)
    
    # 读取所负责的项目提交记录
    cmts = []
    stars = []
    for repo in owner_repos:
        commits = get_commits(repo)
        cmts.extend(commits)

    # 读取参与贡献的项目的star数
    for repo in repos:
        stars.append((repo, 'contributor', get_stars(repo)))

    # 读取所负责的项目的star数
    for repo in owner_repos:
        stars.append((repo, 'owner', get_stars(repo)))

    # 计算所负责的项目所奖励的鲸币数量
    owner_cmts_coins, stars_coins = compute_owner_coins(cmts, stars)

    # 输出最终计算结果
    print('您通过参与项目贡献提交Commit获得{}鲸币奖励~'.format(cmts_coins))
    print('您通过参与项目贡献提交Pull Request获得{}鲸币奖励~'.format(prs_coins))
    print('您所负责的项目在您的贡献下持续更新迭代获得{}鲸币奖励~'.format(owner_cmts_coins))
    print('您所参与和负责的项目在您的贡献下收获大量star获得{}鲸币奖励~'.format(stars_coins))
    print('您总共获得{}鲸币奖励~'.format(cmts_coins + prs_coins + owner_cmts_coins + stars_coins))
