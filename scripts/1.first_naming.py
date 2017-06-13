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


def create_naming_hanja_table():
    conn = sqlite3.connect('naming_korean.db')
    create_c = conn.cursor()
# meaning: 뜻, reading: 음, radical: 부수, strokes: 획
# add_strokes: 원획과 필획의 획수가 다른 한자가 있어서 추가할 획수 저장
# five_type: 오행 -> 금(金), 수(水), 목(木), 화(火), 토(土)
    create_c.execute('''
    CREATE TABLE IF NOT EXISTS naming_hanja (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "hanja" char(1) NULL,
    "strokes" integer NULL,
    "add_strokes" integer NULL,
    "is_naming_hanja" char(1) NULL,
    "meaning" text NULL,
    "reading" char(1) NULL,
    "pronunciations" varchar(32) NULL,
    "reading_strokes" integer NULL,
    "radical" char(1) NULL,
    "radical_info" varchar(128) NULL,
    "five_type" char(1) NULL,
    "rsc_type" char(1) NULL,
    "pronunciations" varchar(32) NULL)
    ''')
    conn.commit()

    return conn


def insert_query_naming_hanja(hanja, reading, conn):
    insert_sc = conn.cursor()
    query = '''
    INSERT INTO naming_hanja (id, hanja, reading)
    VALUES (NULL, "%s", "%s")''' % (hanja, reading)
    insert_sc.execute(query)
    conn.commit()


# Supreme Court
def insert_sc_nameing_hanja(conn, reading, naming_char, naming_char_len):
    if len(reading) != 1:
        # print('[Insert Naming Hanja] ', [reading], 'pass')
        return

    if naming_char_len == 1 and naming_char[0] == '–':
        # print('[Insert Naming Hanja] ', [reading], '– pass')
        return

    for i in range(naming_char_len):
        if len(naming_char[i]) > 1:
            exception_char = naming_char[i].replace('(', ' ').replace(')', '').split()
            for j in range(len(exception_char)):
                insert_query_naming_hanja(exception_char[j], reading, conn)
        else:
            insert_query_naming_hanja(naming_char[i], reading, conn)


def get_sc_naming_hanja(conn):
    url = 'https://namu.wiki/w/%ED%95%9C%EC%9E%90/%EC%9D%B8%EB%AA%85%EC%9A%A9%20%ED%95%9C%EC%9E%90%ED%91%9C'
    r = get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for wt in soup.find_all(match_soup_class(['wiki-table'])):
        for tr in wt.find_all('tr'):
            idx = 1
            for td in tr.find_all('td'):
                if idx == 1:
                    reading = td.text
                else:
                    naming_char = td.text.split()
                    naming_char_len = len(td.text.split())
                    insert_sc_nameing_hanja(conn, reading,
                                            naming_char, naming_char_len)
                idx += 1
        break  # need 1 loop


def update_naming_flag(flag, hanja, conn):
    update_flag = conn.cursor()
    query = 'UPDATE naming_hanja SET is_naming_hanja=%s WHERE hanja="%s"' % (
            flag, hanja)
    update_flag.execute(query)
    conn.commit()


def check_possible_naming(conn):
    possible_select = conn.cursor()
    base_url = 'http://hanja.naver.com/hanja?q='
    query = 'SELECT hanja,reading FROM naming_hanja'
    # query = 'select chinese_char from naming_baby where id=5624'
    for row in possible_select.execute(query):
        url = '%s%s' % (base_url, row[0])
        r = get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for top_box in soup.find_all(match_soup_class(['entrytop_box'])):
            if top_box.text.find('인명용') == -1:
                update_naming_flag('0', row[0], conn)  # False
                print('[IsPossible - Nope]: ', row[0], row[1])
            else:
                update_naming_flag('1', row[0], conn)  # True
                print('[IsPossible - Good]: ', row[0], row[1])


def update_detail_info(radical_info, strokes, meaning, hanja, conn):
    update_detail = conn.cursor()
    query = '''
    UPDATE naming_hanja
    SET radical="%s", radical_info="%s", strokes=%s, meaning="%s"
    WHERE hanja="%s"
    ''' % (radical_info[0], radical_info[1], strokes, meaning, hanja)
    update_detail.execute(query)
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


def set_detail_info(conn):
    base_url = 'http://hanja.naver.com/search?query='
    query = 'SELECT hanja,is_naming_hanja,reading FROM naming_hanja'
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
        print('[Detail Insert] ', row[0], row[2])


def update_hangul_strokes(f_type, hanja, conn):
    update_c = conn.cursor()
    query = 'UPDATE naming_hanja SET five_type="%s" WHERE hanja="%s"' % (
            f_type, hanja)
    update_c.execute(query)
    conn.commit()


def get_five_type(cs):
    if cs == 'ㄱ' or cs == 'ㄲ' or cs == 'ㅋ':
        f_type = '木'
    elif cs == 'ㄴ' or cs == 'ㄷ' or cs == 'ㄸ' or cs == 'ㄹ' or cs == 'ㅌ':
        f_type = '火'
    elif cs == 'ㅁ' or cs == 'ㅂ' or cs == 'ㅃ' or cs == 'ㅍ':
        f_type = '水'
    elif cs == 'ㅇ' or cs == 'ㅎ':
        f_type = '土'
    elif cs == 'ㅅ' or cs == 'ㅆ' or cs == 'ㅈ' or cs == 'ㅉ' or cs == 'ㅊ':
        f_type = '金'
    else:
        print('error, check it chosung: ', cs)
        return -1
    return f_type


def set_five_type(conn):
    query = 'SELECT hanja,is_naming_hanja,reading FROM naming_hanja'
    ftype_select = conn.cursor()
    for row in ftype_select.execute(query):
        if row[1] == 0:  # Can not use Korean name
            continue
        cs = split_syllable_char(row[2])  # 초성
        # hlen = hangul_len(row[2])
        f_type = get_five_type(cs[0])  # 음양'오행'
        if f_type == -1:
            continue
        print(f_type, row[0])
        update_hangul_strokes(f_type, row[0], conn)


def main():

    conn = create_naming_hanja_table()

    # STEP 1: get 'Supreme Court of Korea' naming hanja list
    get_sc_naming_hanja(conn)

    # STEP 2: filterling possible naming hanja list
    check_possible_naming(conn)

    # STEP 3: set detail hanja information
    set_detail_info(conn)

    # STEP 4: select one of 5 types (木 火 水 土 金)
    set_five_type(conn)

    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
