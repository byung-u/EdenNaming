#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sqlite3

from bs4 import BeautifulSoup
from requests import get

MAX_LAST_NAME_1_COUNT = 282


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
    CREATE TABLE IF NOT EXISTS last_name (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "hanja" char(1) NULL,
    "strokes" integer NULL,
    "add_strokes" integer NULL,
    "reading" char(1) NULL,
    "reading_strokes" integer NULL,
    "meaning" text NULL,
    "radical" char(1) NULL,
    "radical_info" varchar(128) NULL,
    UNIQUE(reading, hanja))''')
    conn.commit()
    return conn


def insert_last_name(last_name, conn):
    if len(last_name) == 0:
        print('[ERR] ', last_name)
        return

    query = '''
    INSERT INTO last_name (id, reading, hanja) VALUES (NULL, "%s", "%s")
    ''' % (last_name[0], last_name[1])

    insert_c = conn.cursor()
    try:
        insert_c.execute(query)
    except:
        print('already exist: ', last_name[0], last_name[1])
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
    UPDATE last_name
    SET radical="%s", radical_info="%s", strokes=%s, meaning="%s"
    WHERE hanja="%s"
    ''' % (radical_info[0], radical_info[1], strokes, meaning, hanja)
    update_detail.execute(query)
    conn.commit()


def set_detail_info(conn):
    base_url = 'http://hanja.naver.com/search?query='
    query = 'SELECT hanja,reading FROM last_name'
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


def insert_from_file(conn):
    with open('last_name_1') as f:
        for line in f:
            ln = line.split()
            insert_last_name(ln, conn)
    f.closed


def check_inserted_hanja(conn):
    select_l = conn.cursor()
    query = 'select COUNT(*) from last_name;'
    select_l.execute(query)
    if (select_l.fetchone()[0] == MAX_LAST_NAME_1_COUNT):
        print('Already inserted')
        return 0

    print('Need to insert')
    return -1


def main():
    conn = sqlite3_init()
    ret = check_inserted_hanja(conn)
    if ret == -1:  # not inserted yet
        insert_from_file(conn)
    set_detail_info(conn)
    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
