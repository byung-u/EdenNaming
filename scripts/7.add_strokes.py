#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3


"""
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
"hanja" char(1) NULL,
"strokes" integer NULL,
"add_strokes" integer NULL,
"is_naming_hanja" char(1) NULL,
"meaning" text NULL,
"reading" char(1) NULL,
"reading_strokes" integer NULL,
"radical" char(1) NULL,
"radical_info" varchar(128) NULL,
"five_type" char(1) NULL)''')


last_name (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "hanja" char(1) NULL,
    "strokes" integer NULL,
        '月': 2,
    "add_strokes" integer NULL,
    "reading" char(1) NULL,
    "reading_strokes" integer NULL,
    "meaning" text NULL,
    "radical" char(1) NULL,
    "radical_info" varchar(128) NULL,
    UNIQUE(reading, hanja));
"""

add_radical = {
        '扌': 1,
        '忄': 1,
        '氵': 1,
        '犭': 1,
        '礻': 1,
        '王': 1,
        '艹': 2,
        '衤': 1,
        '月': 2,
        '罒': 1,
        '辶': 3,
        '耂': 2,
        }
# 우부방, 좌부변은 따로 예외처리함


def update_add_strokes(table, add_strokes, hanja, conn):
    print(hanja, add_strokes)
    update_flag = conn.cursor()
    query = 'UPDATE %s SET add_strokes=%s WHERE hanja="%s"' % (table, add_strokes, hanja)
    update_flag.execute(query)
    conn.commit()


def naming_hanja_add_strokes(conn):
    s = conn.cursor()
    query = 'SELECT hanja,reading,radical,radical_info FROM naming_hanja'
    for row in s.execute(query):
        try:
            add_strokes = add_radical[row[2]]
            update_add_strokes('naming_hanja', add_strokes, row[0], conn)
        except:
            if row[3] == '우부방':
                update_add_strokes('naming_hanja', 4, row[0], conn)
            elif row[3] == '좌부변':
                update_add_strokes('naming_hanja', 5, row[0], conn)
            else:
                continue


def get_add_strokes(radical, radical_info):
    if len(radical) > 1:  # '荒木', '황목', '艹,木', '초두머리,나무목'
        rad = radical.split(',')
        add_strokes = 0
        for i in range(len(rad)):
            try:
                ret = add_radical[rad[i]]
                add_strokes += ret
            except:
                if radical_info == '우부방':
                    add_strokes += 4
                elif radical_info == '좌부변':
                    add_strokes += 5
                else:
                    continue
        return add_strokes
    else:
        try:
            return add_radical[radical]
        except:
            if radical_info == '우부방':
                return 4
            elif radical_info == '좌부변':
                return 5
            else:
                return 0


def last_name_add_strokes(conn):
    s = conn.cursor()
    query = 'SELECT hanja,reading,radical,radical_info FROM last_name'
    for row in s.execute(query):
        add_strokes = get_add_strokes(row[2], row[3])
        if add_strokes == 0:
            continue
        update_add_strokes('last_name', add_strokes, row[0], conn)


def main():

    conn = sqlite3.connect('naming_korean.db')

    naming_hanja_add_strokes(conn)
    last_name_add_strokes(conn)

    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
