#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import re
import sqlite3
from bs4 import BeautifulSoup


def sqlite3_init():
    conn = sqlite3.connect('naming_korean.db')
    c = conn.cursor()
    # sol : 태양력
    # lun : 태음력
    # 각 년에 배정되는 간지를 세차
    # 각 월에 부여되는 간지를 월건
    # 각 일에 배정되는 간지를 일진
    c.execute('''
    CREATE TABLE IF NOT EXISTS gregorian_calendar (
    "sol_year" integer NOT NULL,
    "sol_month" integer NOT NULL,
    "sol_day" integer NOT NULL,
    "lun_year" integer NOT NULL,
    "lun_month" integer NOT NULL,
    "lun_day" integer NOT NULL,
    "lun_secha" char(4) NOT NULL,
    "lun_wolgeon" char(4) NOT NULL,
    "lun_iljin" char(4) NOT NULL,
    UNIQUE(sol_year, sol_month, sol_day))
    ''')
    conn.commit()
    return conn


# OPEN API limit 10,000 per day.
# 1900~1919 [o]
# 1920~1939 [0]
# 1940~1959 [O]
# 1960~1979 [o]
# 1980~1999 [x]
# 2000~2019 [x]
# 2020~2039 [x]
def main():
    conn = sqlite3_init()
    february = 0
    for year in range(1983, 2000):
        if year % 4 == 0:
            if year % 400 == 0:
                february = 29
            elif year % 100 == 0:
                february = 28
            else:
                february = 29
        else:
            february = 28

        for month in range(1, 13):
            if (month == 1 or month == 3 or month == 5 or
                    month == 7 or month == 8 or month == 10 or month == 12):
                max_day = 31
            elif month == 4 or month == 6 or month == 9 or month == 11:
                max_day = 30
            elif month == 2:
                max_day = february
            else:
                print('error: ', month)
                continue
            for day in range(1, max_day + 1):
                insert_lunar_info(year, month, day, conn)


def insert_lunar_info(year, month, day, conn):
    # No more use this key, blocked
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
    print(soup)
    if soup.resultcode.text != '00' or soup.resultcode is None:
        print('BeautifulSoup failed, data: ', data)
        return

    r = re.compile(r'[()]')
    c = conn.cursor()
    if soup.lunleapmonth.text == '윤':
        # 월건이 없음
        query = '''
        INSERT INTO gregorian_calendar
        VALUES (%s, %s, %s, %s, %s, %s, "%s", "%s", "%s")''' % (
                soup.solyear.text, soup.solmonth.text, soup.solday.text,
                soup.lunyear.text, soup.lunmonth.text, soup.lunday.text,
                r.split(soup.lunsecha.text)[1],
                '-',
                r.split(soup.luniljin.text)[1])
    else:
        query = '''
        INSERT INTO gregorian_calendar
        VALUES (%s, %s, %s, %s, %s, %s, "%s", "%s", "%s")''' % (
                soup.solyear.text, soup.solmonth.text, soup.solday.text,
                soup.lunyear.text, soup.lunmonth.text, soup.lunday.text,
                r.split(soup.lunsecha.text)[1],
                r.split(soup.lunwolgeon.text)[1],
                r.split(soup.luniljin.text)[1])
    try:
        c.execute(query)
        print(
            soup.solyear.text, soup.solmonth.text, soup.solday.text,
            soup.lunyear.text, soup.lunmonth.text, soup.lunday.text,
            soup.lunsecha.text, soup.lunwolgeon.text, soup.luniljin.text)
    except:
        print('already exist: ',
              soup.solyear.text, soup.solmonth.text, soup.solday.text)

    conn.commit()


if __name__ == '__main__':
    main()
