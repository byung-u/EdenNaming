#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sqlite3
from konlpy.tag import *

PROHIBIT_WORD = [
        '격', '견', '굉', '긍', '감', '간', '궤', '귀', '결', '괴', '개', '갱',
        '념', 
        '단', '답', '독',
        '륵', '랍', '륭', '뢰', '릉', '력', '른', '론',
        '멱', '밀', '맹', '막', '만', '망', 
        '방', '봉', '번', '벽', '변', '불', '벌', '빙', '비', '박', '분',
        '숭', '살', '속', '술', '숙',
        '악', '울', '앙', '알', '욕', '압', '역', '암', '업',
        '족', '즐', '질', '적', '증', '징',
        '촌', '촉', '취', '총', '축', '층', '차',
        '쾌',
        '팽', '파', '판', '포', '피', '평',
        '타', '탕', '탐', '특', '탄', '투', '통',
        '휴', '핵', '협', '횡', '흑', '훼', '훤', '혹', '흉', '확', '흔',
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
