#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

from bs4 import BeautifulSoup
from requests import get


def update_pronunciations(conn, pronunciations, hanja):
    c = conn.cursor()
    query = 'UPDATE naming_hanja SET pronunciations="%s" WHERE hanja="%s"' % (pronunciations, hanja)
    c.execute(query)
    print(pronunciations, hanja)
    conn.commit()


def main():
    conn = sqlite3.connect('naming_korean.db')
    base_url = 'http://hanja.naver.com/search?query='
    query = 'SELECT hanja,is_naming_hanja,reading FROM naming_hanja'
    detail_select = conn.cursor()
    for row in detail_select.execute(query):
        if row[1] == 0:  # Can not use Korean name
            continue
        url = '%s%s' % (base_url, row[0])
        r = get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        cnt = 0
        for span in soup.find_all('span'):
            cnt += 1
            if cnt == 49:
                update_pronunciations(conn, span.text, row[0])

    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
