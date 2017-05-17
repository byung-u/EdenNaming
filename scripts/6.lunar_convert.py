#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import re
from bs4 import BeautifulSoup


def get_siju(hour, day):
    # siju[0][0] ... arr[4][11]
    siju = [
        ["甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥"],
        ["丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥"],
        ["戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥"],
        ["庚子", "辛丑", "壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥"],
        ["壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"],
    ]

    if day == '갑' or day == '기':
        x = 0
    elif day == '을' or day == '경':
        x = 1
    elif day == '병' or day == '신':
        x = 2
    elif day == '정' or day == '임':
        x = 3
    elif day == '무' or day == '계':
        x = 4
    else:
        print('[ERR] invalid day: ', day)
        return None

    if 23 <= hour or hour < 1:
        y = 0
    elif 1 <= hour < 3:
        y = 1
    elif 3 <= hour < 5:
        y = 2
    elif 5 <= hour < 7:
        y = 3
    elif 7 <= hour < 9:
        y = 4
    elif 9 <= hour < 11:
        y = 5
    elif 11 <= hour < 13:
        y = 6
    elif 13 <= hour < 15:
        y = 7
    elif 15 <= hour < 17:
        y = 8
    elif 17 <= hour < 19:
        y = 9
    elif 19 <= hour < 21:
        y = 10
    elif 21 <= hour < 23:
        y = 11
    else:
        print('[ERR] invalid hour: ', hour)
        return None
    return (siju[x][y])


def main():
    year = 2017
    month = 4
    day = 26
    hour = 8
    key = 'IhZSwJv61jxbgIPl2A2B489tudqg3YSP9ojnEqJznLZOWK%2B%2BVQBSrrmQT%2F6ckP63nZAd%2FV%2B%2B2d9PdjNrnvWyuw%3D%3D'
    url = 'http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService/getLunCalInfo?solYear=%4d&solMonth=%02d&solDay=%02d&ServiceKey=%s' % (year, month, day, key)

    req = urllib.request.Request(url)
    try:
        res = urllib.request.urlopen(req)
    except UnicodeEncodeError:
        print('UnicodeEncodeError, url: ', url)
        return

    data = res.read().decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    if soup.resultcode.text != '00':
        print('BeautifulSoup failed, data: ', data)
        return
    siju = get_siju(hour, soup.luniljin.text[0])
    print('시  일  월  년')

    r = re.compile(r'[()]')
    print(siju, r.split(soup.luniljin.text)[1],
            r.split(soup.lunwolgeon.text)[1],
            r.split(soup.lunsecha.text)[1])
    #print(soup.lunyear.text, soup.lunmonth.text, soup.lunday.text)
    #print(soup.solyear.text, soup.solmonth.text, soup.solday.text)
    #print('-----')
    #print(soup.lunsecha.text, '년', soup.lunwolgeon.text, '월', soup.luniljin.text, '일', siju, '시')


if __name__ == '__main__':
    main()
