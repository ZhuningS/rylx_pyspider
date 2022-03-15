from bs4 import BeautifulSoup
import socket
import urllib
from urllib import request
import re
import zlib
import json
from urllib.parse import urlparse
from bs4 import NavigableString
from bs4 import Tag

     #获取页面
def getPageSource(url, timeout=100, coding=None):
     try:
          socket.setdefaulttimeout(timeout)
          req = urllib.request.Request(url)
          req.add_header('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
          response = urllib.request.urlopen(req)
          page = ''
          if response.headers.get('Content-Encoding') == 'gzip':
               page = zlib.decompress(page, 16 + zlib.MAX_WBITS)
          if coding is None:
               coding = response.headers.get("charset")
          if coding is None:
               page = response.read()
          else:
               page = response.read()
               page = page.decode(coding).encode('utf-8')
          return page
     except Exception as e:
          m = str(e)
          print(m)
          return m

def affect(points, keep_ratio, ratio, power):
    keep = points * keep_ratio
    if ratio >= 1.: return points
    return keep + (points - keep) * pow(ratio, power)

def calc_link_points(host, ul):
    # simplified host 不要子域名部分！
    link_density = linktext_count = totaltext_count = 0.001
    container_count = innerlink_count = 0.001
    for a in ul.find_all('a'):
        href = a.get('href', '')
        # 内部链接
        if not href or not href.lower().startswith('http') or host in href:
            innerlink_count += 1
            continue
        # 层次太深
        if urlparse(href)[2].strip('/').count('/') >= 1 or '?' in href:
            continue
        link_density += 1
        linktext_count += len(a.text)
        if '_blank' == a.get('target'):
            link_density += 1
    # 统计容器字数
    for t in ul.recursiveChildGenerator():
        if type(t) is NavigableString:
            totaltext_count += len(t)
        else:
            container_count += 1
    points = (link_density - innerlink_count) * 1000
    if points < 0: return 0

    points = affect(points, 0.1, linktext_count / totaltext_count, 2.)
    points = affect(points, 0.1, link_density / container_count, 1.)

    if points < 1000: points = 0
    return points

     #获取友情连接


def getHyperLinks(url):
    data = getPageSource(url)
    data=str(data)
    pats='(https?://[^\s)";]+\.(\w|/)*)'
    link=re.compile(pats).findall(data)
    links=json.dumps(link)
    return links


def getLuple(url):
    data=getPageSource(url)
    soup=BeautifulSoup(data,"lxml")
    for tag in('ul','div'):
        div1=soup.find_all(tag)
    return div1


url="https://51.ruyo.net"
html=getHyperLinks(url)
ulk=getLuple(url)
candidate=[]
for ul in ulk:
    s=calc_link_points(html, ul)
    candidate.append((ul,s))
print(max(candidate))
#print(s)
#print(ul)
#print(html)
