#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sqlite3

from bs4 import BeautifulSoup
from hangul_utils import split_syllable_char
from requests import get


def match_soup_class(target, mode='class'):
    def do_match(tag):
        classes = tag.get(mode, [])
        return all(c in classes for c in target)
    return do_match


def sqlite3_init():
    conn = sqlite3.connect('naming_korean.db')
    c = conn.cursor()
    # level: 격, luck: 운
    c.execute('''
    CREATE TABLE IF NOT EXISTS last_name_hanja (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "hanja" char(1) NULL,
    "strokes" integer NULL,
    "reading" char(1) NULL,
    "reading_strokes" integer NULL,
    "meaning" text NULL,
    "radical" char(1) NULL,
    "radical_info" varchar(128) NULL)''')
    conn.commit()
    return conn


def insert_last_name(last_name, hanja, conn):
    insert_c = conn.cursor()
    if len(hanja) == 0 or len(last_name) == 0:
        print('[ERR] ', last_name, hanja)
        return

    for i in range(len(last_name)):
        for j in range(len(hanja)):
            query = '''
            INSERT INTO last_name_hanja (id, reading, hanja)
            VALUES (NULL, "%s", "%s")''' % (last_name[i], hanja[j])
            try:
                insert_c.execute(query)
            except:
                print('already exist: ', last_name[i], hanja[j])
    conn.commit()


def get_hanja_meaning(means):
    result = []
    temp = []
    meanings = ""
    r3 = re.compile(r'[\d+a-zA-Z]\.')  # ['1.', '아름답다', '2.', '기리다'...]
    for i in range(len(means)):
        if r3.match(means[i]):
            meanings = " ".join(temp)
            if len(meanings) > 0:
                result.append(" ".join(temp))

            del temp[:]
            temp.append(means[i])
        else:
            temp.append(means[i])

    result.append(" ".join(temp))
    return result


def update_detail_info(radical_info, strokes, meaning, hanja, conn):
    update_detail = conn.cursor()
    query = '''
    UPDATE last_name_hanja
    SET radical="%s", radical_info="%s", strokes=%s, meaning="%s"
    WHERE hanja="%s"
    ''' % (radical_info[0], radical_info[1], strokes, meaning, hanja)
    update_detail.execute(query)
    conn.commit()


def set_detail_info(conn):
    base_url = 'http://hanja.naver.com/search?query='
    query = 'SELECT hanja,reading FROM last_name_hanja'
    detail_select = conn.cursor()
    for row in detail_select.execute(query):
        if row[1] == 0:  # Can not use Korean name
            continue
        url = '%s%s' % (base_url, row[0])
        r = get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for sub_info in soup.find_all(match_soup_class(['sub_info'])):
            sub_infos = sub_info.text.split()
        for mean in soup.find_all(match_soup_class(['meaning'])):
            means = mean.text.split()
            break  # MUST 1 looping

        r1 = re.compile(r'[\[\]\(\)]')  # [부수]馬(말마)
        radical_info = r1.split(sub_infos[0])[2:4]

        r2 = re.compile(r'[\[\]총획]')  # [총획]13획
        strokes = r2.split(sub_infos[1])[4]

        meaning = get_hanja_meaning(means)
        update_detail_info(radical_info, strokes, meaning, row[0], conn)
        print('[Detail Insert] ', row[0], row[1])



def main():
    conn = sqlite3_init()
    set_detail_info(conn)

#    with open('last_name_hanja') as f:
#        for idx, line in enumerate(f):
#            if idx % 2 == 0:  # hangul
#                if line.find('/') != -1:
#                    fn = line.rstrip().split('/')
#                else:
#                    fn = line.rstrip()
#            else:  # hanja
#                h = line.split()
#                insert_last_name(fn, h, conn)
#
#    f.closed
#    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
