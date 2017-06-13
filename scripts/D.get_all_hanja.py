#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

from bs4 import BeautifulSoup
from requests import get
from hangul_utils import check_syllable, split_syllable_char


BLOCK_LIST1 = {
    u'ㄲ' : 1,
    u'ㄸ' : 1,
    u'ㅃ' : 1,
    u'ㅆ' : 1,
    u'ㅉ' : 1,
}

BLOCK_LIST3 = {
    u'ㄲ' : 1,
    u'ㄳ' : 1,
    u'ㄵ' : 1,
    u'ㄶ' : 1,
    u'ㄺ' : 1,
    u'ㄻ' : 1,
    u'ㄼ' : 1,
    u'ㄽ' : 1,
    u'ㄾ' : 1,
    u'ㄿ' : 1,
    u'ㅀ' : 1,
    u'ㅄ' : 1,
    u'ㄷ' : 1,
    u'ㅆ' : 1,
    u'ㅊ' : 1,
    u'ㅋ' : 1,
    u'ㅌ' : 1,
    u'ㅍ' : 1,
    u'ㅎ' : 1,
}


def match_soup_class(target, mode='class'):
    def do_match(tag):
        classes = tag.get(mode, [])
        return all(c in classes for c in target)
    return do_match


def create_hanja_table():
    conn = sqlite3.connect('naming_korean.db')

    create_c = conn.cursor()
    create_c.execute('''
    CREATE TABLE IF NOT EXISTS hanja (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "hanja" char(1) NULL,
    "reading" char(1) NULL,
    "pronunciations" varchar(32) NULL)
    ''')
    conn.commit()

    return conn


def insert_hanja(conn, hi):
    c = conn.cursor()
    for hanja, pronunciations in hi.items():
        query = '''
        INSERT INTO hanja (id, hanja, pronunciations) VALUES (NULL, "%s", "%s")''' % (hanja, pronunciations)
        c.execute(query)
    conn.commit()


def get_hanja_info(soup):
    hanja = []
    pronounce = []
    hanja_info = {}
    for sub in soup.find_all(match_soup_class(['result_chn_chr'])):
        for dt in sub.find_all('dt'):
            hanja.append(dt.text)
        for dd in sub.find_all('dd'):
            pronounce.append(dd.a.text)
    # print(hanja, len(hanja))
    # print(pronounce, len(pronounce))
    hanja_info = dict(zip(hanja, pronounce))
    return hanja_info


def get_hanja(conn, hanguls):
    hi = {}
    # s = conn.cursor()
    for hangul in hanguls:
        total = 0
        init_url = 'http://hanja.naver.com/search/keyword?query=%s&searchOption=sortrank&ordr=dsc&pageNo=1&strokeCnt=0&idiomType=1' % hangul
    # query = 'SELECT hanja,reading FROM naming_hanja'
        r = get(init_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for res in soup.find_all(match_soup_class(['result_chn_chr'])):
            cnt = 0
            for sp in res.find_all('span'):
                cnt += 1
                if cnt == 3:  # TODO: need to fix more reliable
                    result_cnt = sp.text.replace(')', '').replace('(', '').replace('건', '')
                    total = int(result_cnt)
                    break
                else:
                    continue
                break
            else:
                continue
            break
        if total == 0:
            continue
        print(total)
        hi = get_hanja_info(soup)
        print(init_url, hi)
        insert_hanja(conn, hi)

        if total <= 10:
            continue
        total_page = (total // 20) + 1  # 나눗셈 // 버림 연산
        for i in range(2, total_page + 1):  # start from 2
            url = 'http://hanja.naver.com/search/keyword?query=%s&searchOption=sortrank&ordr=dsc&pageNo=%d&strokeCnt=0&idiomType=1' % (hangul, i)
            r = get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            hi = get_hanja_info(soup)
            print(url, hi)
            insert_hanja(conn, hi)
    return 


def get_hangul_list():
    hanguls = []
    with open('unicode_hangul') as f:
        for line in f:
            hangul = line.split()
            for h in hangul:
                if check_syllable(h) is False:
                    continue
                split_h = split_syllable_char(h)
                try:
                    if BLOCK_LIST1[split_h[0]] == 1:
                        continue
                except:
                    try:
                        if BLOCK_LIST3[split_h[2]] == 1:
                            continue
                    except:
                        pass
                hanguls.append(h)
    return hanguls


def main():
    conn = create_hanja_table()

    hanguls = get_hangul_list()
    # print(hanguls)
    # print(len(hanguls))
    get_hanja(conn, hanguls)

    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
