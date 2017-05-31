#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

sixty_gapja = {
    u'甲子': '갑자',
    u'乙丑': '을축',
    u'丙寅': '병인',
    u'丁卯': '정묘',
    u'戊辰': '무진',
    u'己巳': '기사',
    u'庚午': '경오',
    u'辛未': '신미',
    u'壬申': '임신',
    u'癸酉': '계유',
    u'甲戌': '갑술',
    u'乙亥': '을해',
    u'丙子': '병자',
    u'丁丑': '정축',
    u'戊寅': '무인',
    u'己卯': '기묘',
    u'庚辰': '경진',
    u'辛巳': '신사',
    u'壬午': '임오',
    u'癸未': '계미',
    u'甲申': '갑신',
    u'乙酉': '을유',
    u'丙戌': '병술',
    u'丁亥': '정해',
    u'戊子': '무자',
    u'己丑': '기축',
    u'庚寅': '경인',
    u'辛卯': '신묘',
    u'壬辰': '임진',
    u'癸巳': '계사',
    u'甲午': '갑오',
    u'乙未': '을미',
    u'丙申': '병신',
    u'丁酉': '정유',
    u'戊戌': '무술',
    u'己亥': '기해',
    u'庚子': '경자',
    u'辛丑': '신축',
    u'壬寅': '임인',
    u'癸卯': '계묘',
    u'甲辰': '갑진',
    u'乙巳': '을사',
    u'丙午': '병오',
    u'丁未': '정미',
    u'戊申': '무신',
    u'己酉': '기유',
    u'庚戌': '경술',
    u'辛亥': '신해',
    u'壬子': '임자',
    u'癸丑': '계축',
    u'甲寅': '갑인',
    u'乙卯': '을묘',
    u'丙辰': '병진',
    u'丁巳': '정사',
    u'戊午': '무오',
    u'己未': '기미',
    u'庚申': '경신',
    u'辛酉': '신유',
    u'壬戌': '임술',
    u'癸亥': '계해',
}


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


def insert_gapja_query(conn, hanja, hangul):
    insert_g = conn.cursor()
    query = 'INSERT INTO naming_60_gapja VALUES (NULL, "%s", "%s")' % (
            hanja, hangul)
    try:
        insert_g.execute(query)
    except Exception as e:
        print('query error: ', e, hanja, hangul)
    conn.commit()


def insert_gapja(conn):
    for hanja, hangul in sixty_gapja.items():
        insert_gapja_query(conn, hanja, hangul)


def main():
    conn = sqlite3_init()
    insert_gapja(conn)
    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
