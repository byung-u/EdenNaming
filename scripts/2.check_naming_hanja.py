#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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


def update_naming_flag(flag, hanja, conn):
    update_c = conn.cursor()
    query = 'UPDATE naming_korean SET is_naming_hanja=%s WHERE hanja="%s"' % (
            flag, hanja)
    update_c.execute(query)
    conn.commit()


def main():

    cursor, conn = sqlite3_init()

    base_url = 'http://hanja.naver.com/hanja?q='
    query = 'SELECT hanja,reading FROM naming_korean'
    # query = 'select chinese_char from naming_baby where id=5624'
    for row in cursor.execute(query):
        url = '%s%s' % (base_url, row[0])
        r = get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for top_box in soup.find_all(match_soup_class(['entrytop_box'])):
            if top_box.text.find('인명용') == -1:
                update_naming_flag(0, row[0], conn)  # False
                print('[Not for Korean]: ', row[0], row[1])
            else:
                update_naming_flag(1, row[0], conn)  # True
                print('[Got it]: ', row[0], row[1])

    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
