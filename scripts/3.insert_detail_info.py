#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sqlite3
from bs4 import BeautifulSoup
from requests import get


def match_soup_class(target, mode='class'):
    def do_match(tag):
        classes = tag.get(mode, [])
        return all(c in classes for c in target)
    return do_match


def sqlite3_init():
    conn = sqlite3.connect('naming_korean.db')
    c = conn.cursor()
    return c, conn


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
    update_c = conn.cursor()
    query = '''
    UPDATE naming_korean
    SET radical="%s", radical_info="%s", strokes=%s, meaning="%s"
    WHERE hanja="%s"
    ''' % (radical_info[0], radical_info[1], strokes, meaning, hanja)
    update_c.execute(query)
    conn.commit()


def main():

    cursor, conn = sqlite3_init()

    base_url = 'http://hanja.naver.com/search?query='
    query = 'SELECT hanja,is_naming_hanja,reading FROM naming_korean'
    for row in cursor.execute(query):
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
        print(row[0], row[2])


if __name__ == '__main__':
    main()
