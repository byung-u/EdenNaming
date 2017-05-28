#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3


def sqlite3_init():
    conn = sqlite3.connect('naming_korean.db')
    c = conn.cursor()
    # level: 격, luck: 운
    c.execute('''
    CREATE TABLE IF NOT EXISTS naming_60_gapja (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "gapja" char(4) NULL,
    "gapja_hangul" char(4) NULL,
    UNIQUE(gapja, gapja_hangul))
    ''')
    conn.commit()
    return conn


def insert_gapja_query(info, conn):
    insert_g = conn.cursor()
    if len(info) == 0:
        print('[pass] ', info)
        return
    query = 'INSERT INTO naming_60_gapja VALUES (NULL, "%s", "%s")' % (
            info[0], info[1])
    try:
        insert_g.execute(query)
    except Exception as e:
        print('query error: ', e, [info])
    conn.commit()


def insert_gapja(conn):
    with open('60_gap') as f:
        for idx, line in enumerate(f):
            info = line.split()
            if len(info) == 0:
                continue
            insert_gapja_query(info, conn)
    f.closed


def main():
    conn = sqlite3_init()
    insert_gapja(conn)
    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
