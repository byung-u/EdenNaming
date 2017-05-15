#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sqlite3
from hangul_utils import split_syllable_char


def match_soup_class(target, mode='class'):
    def do_match(tag):
        classes = tag.get(mode, [])
        return all(c in classes for c in target)
    return do_match


def sqlite3_init():
    conn = sqlite3.connect('naming_korean.db')
    c = conn.cursor()
    return c, conn


def get_hanja_meaning(means):
    result = []
    temp = []
    meanings = ""
    r3 = re.compile(r'[\d+a-zA-Z]\.')  # ['1.', '아름답다', '2.', '기리다'...]
    for i in range(len(means)):
        if r3.match(means[i]):
            meanings = " ".join(temp)
            if len(meanings) > 0:
                result.append(" ".join(temp))

            del temp[:]
            temp.append(means[i])
        else:
            temp.append(means[i])

    result.append(" ".join(temp))
    return result


def update_hangul_strokes(f_type, hanja, conn):
    update_c = conn.cursor()
    query = 'UPDATE naming_korean SET five_type="%s" WHERE hanja="%s"' % (
            f_type, hanja)
    update_c.execute(query)
    conn.commit()


def get_five_type(cs):
    if cs == 'ㄱ' or cs == 'ㄲ' or cs == 'ㅋ':
        f_type = '木'
    elif cs == 'ㄴ' or cs == 'ㄷ' or cs == 'ㄸ' or cs == 'ㄹ' or cs == 'ㅌ':
        f_type = '火'
    elif cs == 'ㅁ' or cs == 'ㅂ' or cs == 'ㅃ' or cs == 'ㅍ':
        f_type = '水'
    elif cs == 'ㅇ' or cs == 'ㅎ':
        f_type = '土'
    elif cs == 'ㅅ' or cs == 'ㅆ' or cs == 'ㅈ' or cs == 'ㅉ' or cs == 'ㅊ':
        f_type = '金'
    else:
        print('error, check it chosung: ', cs)
        return -1
    return f_type


def main():

    cursor, conn = sqlite3_init()

    query = 'SELECT hanja,is_naming_hanja,reading FROM naming_korean'
    for row in cursor.execute(query):
        if row[1] == 0:  # Can not use Korean name
            continue
        cs = split_syllable_char(row[2])  # 초성
        # hlen = hangul_len(row[2])
        f_type = get_five_type(cs[0])  # 음양'오행'
        if f_type == -1:
            continue
        update_hangul_strokes(f_type, row[0], conn)


if __name__ == '__main__':
    main()
