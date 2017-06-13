#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sqlite3


def sqlite3_init():
    conn = sqlite3.connect('naming_korean.db')
    c = conn.cursor()
    # level: 격, luck: 운
    c.execute('''
    CREATE TABLE IF NOT EXISTS naming_81_explanation (
    "strokes" integer NULL,
    "explain" varchar(1024) NULL,
    UNIQUE(strokes))
    ''')
    conn.commit()
    return conn


def insert_numeric_info(strokes, explain, conn):
    insert_c = conn.cursor()
    if strokes is None or explain is None:
        print('[pass] ', strokes, explain)
        return
    query = 'INSERT INTO naming_81_explanation VALUES (%s, "%s")' % (
            strokes, explain)
    try:
        insert_c.execute(query)
    except:
        print('already exist: ', strokes, explain)
    conn.commit()


# 이외에 82수 이상의 數는 그數에 80을 뺀 數를 적용하면 되는데
# 86數인 경우 80을 뺀 6數에 해당하는
# 길흉(吉凶)으로 해석하면 틀림 없겠습니다.
def insert_explanation(conn):  # http://yxeta.tistory.com/29
    with open('81_explanation') as f:
        for idx, line in enumerate(f):
            if idx % 2 == 0:
                info = line.rstrip().replace(',', '').replace('<', '').replace('>', '').split()
                if len(info) == 0:
                    continue
                strokes = re.split(r"(\d+)", info[0])[1]
            else:
                explain = line.strip().split('.')
                insert_numeric_info(strokes, explain[0], conn)
                strokes, explain = None, None
    f.closed


def main():
    conn = sqlite3_init()

    insert_explanation(conn)

    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
