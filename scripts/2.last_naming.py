#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sqlite3

from bs4 import BeautifulSoup
from requests import get

MAX_LAST_NAME_1_COUNT = 282
MAX_LAST_NAME_2_COUNT = 13


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
    "rsc_type" char(1) NULL,
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


def update_detail_info2(radical, radical_info, strokes, meaning, hanja, conn):
    update_detail = conn.cursor()
    query = '''
    UPDATE last_name
    SET radical="%s", radical_info="%s", strokes=%s, meaning="%s"
    WHERE hanja="%s"
    ''' % (radical, radical_info, strokes, meaning, hanja)
    print(query)
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


def set_detail_info2(conn):
    base_url = 'http://hanja.naver.com/search/keyword?query='
    query = 'SELECT hanja,reading FROM last_name where LENGTH(hanja)=2'
    detail_select = conn.cursor()
    for row in detail_select.execute(query):
        if row[1] == 0:  # Can not use Korean name
            continue
        url = '%s%s' % (base_url, row[0])
        r = get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        sub_infos = []
        for sub_info in soup.find_all(match_soup_class(['sub_info'])):
            sub_infos.append(sub_info.text)
        cnt = 0
        means = []
        for mean in soup.find_all(match_soup_class(['meaning'])):
            means.append(mean.text)
            cnt += 1
            if cnt == 2:
                break  # MUST 2 looping

        r1 = re.compile(r'[\[\]\(\)]')  # [부수]馬(말마)
        r2 = re.compile(r'[\[\]총획]')  # [총획]13획

        a1 = []  # radical hanja
        a2 = []  # radical meaning
        a3 = 0  # radical strokes
        a4 = []  # radical meaning

        for i in range(2):
            each_info = sub_infos[i].split()
            each_mean = means[i].split()

            radical_info = r1.split(each_info[0])[2:4]
            a1.append(radical_info[0])
            a2.append(radical_info[1])
            strokes = r2.split(each_info[1])[4]
            a3 += int(strokes)
            meaning = get_hanja_meaning(each_mean)
            a4.append(meaning)
        res_means = '%s^%s' % ("".join(a4[0]), "".join(a4[1]))
        update_detail_info2(",".join(a1), ",".join(a2), a3, res_means, row[0], conn)


def insert_from_file(conn, file_name):
    with open(file_name) as f:
        for line in f:
            ln = line.split()
            insert_last_name(ln, conn)
    f.closed


def check_inserted_hanja(conn):
    select_l = conn.cursor()
    query = 'select COUNT(*) from last_name;'
    select_l.execute(query)
    if (select_l.fetchone()[0] == MAX_LAST_NAME_1_COUNT):
        print('[1]Already inserted')
        return 0

    print('[1]Need to insert')
    return -1


def check_inserted_hanja2(conn):
    select_l = conn.cursor()
    query = 'select COUNT(*) from last_name where LENGTH(hanja)=2;'
    select_l.execute(query)
    if (select_l.fetchone()[0] == MAX_LAST_NAME_2_COUNT):
        print('[2]Already inserted')
        return 0
    print('[2]Need to insert')
    return -1


def main():
    conn = sqlite3_init()
    ret = check_inserted_hanja(conn)
    if ret == -1:  # not inserted yet
        insert_from_file(conn, 'last_name_1')
    set_detail_info(conn)

    ret = check_inserted_hanja2(conn)
    if ret == -1:  # not inserted yet
        insert_from_file(conn, 'last_name_2')
    set_detail_info2(conn)

    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()


# Last name 자원 오행 타입 추가한 코드
"""
    query = 'select hanja from last_name'
    for row in s1.execute(query):
        nested_query = "select rsc_type from naming_hanja where hanja='%s'" % row[0]
        for nested_row in s2.execute(nested_query):
            if nested_row[0] is None:
                print(row, nested_row)
            else:
                uc = conn.cursor()
                u_query = "UPDATE last_name SET rsc_type='%s' WHERE hanja='%s'" % (nested_row[0], row[0])
                uc.execute(u_query)
                print(u_query)

    conn.commit()
UPDATE last_name SET rsc_type='火' WHERE hanja='鴌';
UPDATE last_name SET rsc_type='土' WHERE hanja='郝';
UPDATE last_name SET rsc_type='木' WHERE hanja='罗';
UPDATE last_name SET rsc_type='水' WHERE hanja='滕';
UPDATE last_name SET rsc_type='木' WHERE hanja='杨';
UPDATE last_name SET rsc_type='金' WHERE hanja='陈';
UPDATE last_name SET rsc_type='金' WHERE hanja='张';
"""
