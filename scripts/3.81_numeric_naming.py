#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sqlite3


def sqlite3_init():
    conn = sqlite3.connect('naming_korean.db')
    c = conn.cursor()
    # level: 격, luck: 운
    c.execute('''
    CREATE TABLE IF NOT EXISTS naming_81 (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "strokes" integer NULL,
    "reference" char(16) NULL,
    "level" char(16) NULL,
    "luck" char(16) NULL,
    "luck_type" char(1) NULL,
    UNIQUE(strokes, reference))
    ''')
    conn.commit()
    return conn


def insert_numeric_info(strokes, ref, level, luck, l_type, conn):
    insert_c = conn.cursor()
    if level is None or \
       luck is None or \
       l_type is None or \
       strokes is None or \
       ref is None:
        print('[pass] ', level, luck, l_type)
        return
    query = '''
    INSERT INTO naming_81
    VALUES (NULL, %s, "%s", "%s", "%s", "%s")''' % (
            strokes, ref, level, luck, l_type)
    try:
        insert_c.execute(query)
    except:
        print('already exist: ', strokes, level, luck, l_type)
    conn.commit()


def insert_yxeta(conn):  # http://yxeta.tistory.com/29
    with open('81_a') as f:
        for idx, line in enumerate(f):
            if idx % 8 == 0:
                strokes = line.rstrip()
            elif idx % 8 == 2:
                level = line.rstrip()
            elif idx % 8 == 4:
                luck = line.rstrip()
            elif idx % 8 == 6:
                l_type = line.rstrip()
                insert_numeric_info(strokes, 'yxeta',
                                    level, luck, l_type, conn)
                strokes, level, luck, l_type = None, None, None, None
    f.closed


def insert_ancapone(conn):  # http://m.blog.daum.net/ancapone/280
    with open('81_b') as f:
        for idx, line in enumerate(f):
            if idx % 2 == 0:
                info = line.rstrip().replace(',', '').replace('<', '').replace('>', '').split()
                if len(info) == 0:
                    continue
                strokes = re.split(r"(\d+)수:", info[0])[1]
                l_type = re.split(r"[\(\s+\)]", info[1])[1]
                level = info[2]
                luck = '%s, %s' % (info[3], info[4])
                insert_numeric_info(strokes, 'ancapone',
                                    level, luck, l_type, conn)
                strokes, level, luck, l_type = None, None, None, None
    f.closed


def insert_busan(conn):  # busan jakmyungso
# http://blog.naver.com/PostView.nhn?blogId=nuriname&logNo=220786794655&categoryNo=51&parentCategoryNo=-1&viewDate=&currentPage=&postListTopCurrentPage=&isAfterWrite=true
    with open('81_c') as f:
        for idx, line in enumerate(f):
            if idx % 2 == 0:
                info = re.split(r"(\d+)수 ", line.rstrip())
                strokes = info[1]
                l_type = info[2]
            else:
                temp = line.split()
                level = '%s(%s)' % (temp[0], temp[2])
                luck = '%s(%s)' % (temp[1], temp[3])
                insert_numeric_info(strokes, 'busan',
                                    level, luck, l_type, conn)
                strokes, level, luck, l_type = None, None, None, None
    f.closed


def main():
    conn = sqlite3_init()

    insert_yxeta(conn)
    insert_ancapone(conn)
    insert_busan(conn)

    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
