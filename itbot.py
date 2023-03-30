import itchat
import requests
from bs4 import BeautifulSoup
import time

# 登录微信
itchat.auto_login(hotReload=True)

def reply_vote(msg):
    # 获取投票选项和链接
    vote_options, vote_link = get_vote_info(msg.text)
    # 获取已经投票的选项
    voted_options = get_voted_options(vote_link)
    # 过滤已经投过票的选项
    vote_options = list(set(vote_options) - set(voted_options))
    # 如果有未投票的选项，则进行投票
    if vote_options:
        vote_success = vote(vote_options[0], vote_link)
        if vote_success:
            reply_text = '成功为“{}”进行投票'.format(vote_options[0])
        else:
            reply_text = '投票失败，请稍后再试'
    else:
        reply_text = '所有选项都已经投过票了'
    # 回复投票结果
    itchat.send(reply_text, msg['FromUserName'])


def get_vote_info(text):
    # 解析消息文本，获取投票选项和链接
    soup = BeautifulSoup(text, 'html.parser')
    vote_options = []
    vote_link = ''
    for p in soup.find_all('p'):
        if '选项' in p.text:
            for li in p.find_next_sibling('ul').find_all('li'):
                vote_options.append(li.text)
        elif '链接' in p.text:
            vote_link = p.find('a')['href']
    return vote_options, vote_link


def get_voted_options(vote_link):
    # 获取已经投票的选项
    r = requests.get(vote_link)
    soup = BeautifulSoup(r.text, 'html.parser')
    voted_options = []
    for li in soup.find_all('li', {'class': 'vote__item'}):
        voted_options.append(li.find('p', {'class': 'vote__text'}).text)
    return voted_options


def vote(vote_option, vote_link):
    # 发送投票请求
    data = {'option': vote_option}
    headers = {'content-type': 'application/json'}
    r = requests.post(vote_link, json=data, headers=headers)
    # 等待一段时间，防止投票过于频繁
    time.sleep(5)
    # 判断投票是否成功
    if r.status_code == 200:
        return True
    else:
        return False


itchat.auto_login(hotReload=True)

@itchat.msg_register(itchat.content.TEXT)
def reply_vote(msg):
    reply_vote(msg)

itchat.run()
