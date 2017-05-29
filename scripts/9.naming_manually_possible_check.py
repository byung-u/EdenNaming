#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sqlite3
from konlpy.tag import *

PROHIBIT_WORD = [
        '격', '견', '굉', '긍', 
        '념', 
        '륵', '랍', '륭', '뢰',
        '멱', '밀',
        '방', '봉', '번', '벽', '변', '불',
        '악', '울', '앙',
        '족', '질', 
        '촌', '촉', '취',
        '팽', 
        '타', '탐', '특',
        '휴', '핵', '협', '횡', '흑', '훼', '훤', '혹',
        ]


def update_naming_flag(conn, hanja):
    update_flag = conn.cursor()


def main():
    conn = sqlite3.connect('naming_korean.db')

    s = conn.cursor()
    for i in range(len(PROHIBIT_WORD)):
        query = 'UPDATE naming_hanja SET is_naming_hanja=-1 WHERE reading="%s" AND is_naming_hanja=1' % (PROHIBIT_WORD[i])
        print(PROHIBIT_WORD[i])
        s.execute(query)
    conn.commit()
    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
