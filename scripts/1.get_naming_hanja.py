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
# meaning: 뜻, reading: 음, radical: 부수, strokes: 획
# five_type: 오행 -> 금(金), 수(水), 목(木), 화(火), 토(土)
    c.execute('''
    CREATE TABLE IF NOT EXISTS naming_korean (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "hanja" char(1) NULL,
    "strokes" integer NULL, 
    "is_naming_hanja" boolean,
    "meaning" text NULL,
    "reading" char(1) NULL,
    "reading_strokes" integer NULL, 
    "radical" char(1) NULL,
    "radical_info" varchar(128) NULL, 
    "five_type" char(1) NULL)''')
    conn.commit()
    return c, conn


def insert_hanja_query(cursor, conn,
                           reading, naming_char, naming_char_len):
    if len(reading) != 1:
        print([reading], 'pass')
        return

    if naming_char_len == 1 and naming_char[0] == '–':
        print([reading], 'pass')
        return

    for i in range(naming_char_len):
        if naming_char[i] == '𡅕':
            print(reading, '\t', naming_char[i])
            continue
        query = '''
        INSERT INTO naming_korean (id, hanja, reading) 
        VALUES (NULL, "%s", "%s")''' % (naming_char[i], reading)
        cursor.execute(query)
        conn.commit()


def main():

    cursor, conn = sqlite3_init()

    url = 'https://namu.wiki/w/%ED%95%9C%EC%9E%90/%EC%9D%B8%EB%AA%85%EC%9A%A9%20%ED%95%9C%EC%9E%90%ED%91%9C'
    r = get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for wt in soup.find_all(match_soup_class(['wiki-table'])):
        for tr in wt.find_all('tr'):
            idx = 1
            # print('\n\n')
            for td in tr.find_all('td'):
                if idx == 1:
                    # print('----------------- ', td.text, ' ---------------')
                    reading = td.text
                elif idx == 3:
                    naming_char = td.text.split()
                    naming_char_len = len(td.text.split())
                    insert_hanja_query(cursor, conn,
                                       reading, naming_char, naming_char_len)

                idx += 1
        break  # need 1 loop
    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
