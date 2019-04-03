from urllib import request
from bs4 import  BeautifulSoup
import time


title_dict = dict()

def send_email(title_dict):
    email_title = '[仙珍园]' + str(len(title_dict)) + '条新帖子'
    email_content = ''
    for key, value in title_dict.items():
        cur_line = value['date'] + '\t' + value['title_text'] + '\t' + \
                         value['comment_num'] + '/' + value['view_num'] + '\t' + value['href'] +'\n'
        print(cur_line)
        email_content += cur_line
    # Shini just use email_title and email_content, Fighting!


def refresh():
    print('refresh')
    global title_dict
    new_title = dict()
    paratext= 'mod=forumdisplay&fid=24&page=1&filter=typeid&typeid=21'
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
    url='http://www.xianzhenyuan.cn/forum.php'
    req = request.Request(url='%s%s%s' % (url,'?',paratext),headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    # print(res)
    soup = BeautifulSoup(res, 'html.parser')
    title_list = soup.find_all('a', 's xst')
    for title in title_list:
        post = dict()
        post['date'] = str(title.parent.parent.find_all('span')[-1]).split('>')[1].split('<')[0]
        num_element = title.parent.parent.find('td', 'num')
        for child in num_element:
            if child.name == 'a':
                post['comment_num'] = child.contents[0]
            if child.name == 'em':
                post['view_num'] = child.contents[0]
        title = str(title)
        href = title.split('href="')[1].split('"')[0]
        if 'amp;' in href:
            href = href.replace('amp;', '')
        post['href'] = href
        post['title_text'] = title.split('>')[1].split('<')[0]
        tid = href.split('tid=')[1].split('&')[0]
        if tid in title_dict:
            continue
        else:
            title_dict[tid] = post
            new_title[tid] = post
    if len(new_title) != 0:
        send_email(new_title)

if __name__ == '__main__':
    while True:
        refresh()
        time.sleep(60)