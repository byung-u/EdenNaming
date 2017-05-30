#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sqlite3
from konlpy.tag import *

list_tag = [u'NNG', u'VV', u'VA', u'VXV', u'UN']


def check_is_possible(pos, list_positive, list_negative, list_neutral, ALL):
    meaning_res = []
    for i in pos:
        if i[1] == u'SW':
            if i[0] in [u'♡', u'♥']:
                meaning_res.append(i[0])
        if i[1] in list_tag:
            meaning_res.append(i[0])

    # naive bayes 값 계산
    result_pos = naive_bayes_classifier(meaning_res, list_positive, ALL)
    result_neg = naive_bayes_classifier(meaning_res, list_negative, ALL)
    result_neu = naive_bayes_classifier(meaning_res, list_neutral, ALL)

    if (result_pos > result_neg and result_pos > result_neu):
        #print(u'긍정', '+:', result_pos, '-:', result_neg, name)
        return True
    else:  # 부정, 중립
        return False


def getting_list(filename, listname, kkma):
    while 1:
        line = filename.readline()
        string = str(line)
        line_parse = kkma.pos(string)
        for i in line_parse:
            if i[1] == u'SW':
                if i[0] in [u'♡', u'♥']:
                    listname.append(i[0])
            if i[1] in list_tag:
                listname.append(i[0])
        if not line:
            break
    return listname


#naive bayes classifier + smoothing
def naive_bayes_classifier(test, train, all_count):
    counter = 0
    list_count = []
    for i in test:
        for j in range(len(train)):
            if i == train[j]:
                counter = counter + 1
        list_count.append(counter)
        counter = 0
    list_naive = []
    for i in range(len(list_count)):
        list_naive.append((list_count[i]+1)/float(len(train)+all_count))
    result = 1
    for i in range(len(list_naive)):
        result *= float(round(list_naive[i], 6))
    return float(result)*float(1.0/3.0)



def update_naming_flag(conn, hanja):
    update_flag = conn.cursor()
    query = 'UPDATE naming_hanja SET is_naming_hanja=0 WHERE hanja="%s"' % (hanja)
    update_flag.execute(query)
    conn.commit()


def main():
    conn = sqlite3.connect('naming_korean.db')
    kkma = Kkma()

    # getting_list함수를 통해 필요한 tag를 추출하여 list 생성
    f_pos = open('positive-words-ko-v2.txt', 'r')
    f_neg = open('negative-words-ko-v2.txt', 'r')
    f_neu = open('neutral-words-ko-v2.txt', 'r')

    list_positive = []
    list_negative = []
    list_neutral = []

    list_positive = getting_list(f_pos, list_positive, kkma)
    list_negative = getting_list(f_neg, list_negative, kkma)
    list_neutral = getting_list(f_neu, list_neutral, kkma)
    ALL = len(set(list_positive)) + len(set(list_negative)) + len(set(list_neutral))

    s = conn.cursor()
    query = 'SELECT hanja,reading,meaning FROM naming_hanja WHERE is_naming_hanja=1;'
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    for row in s.execute(query):
        meaning = hangul.sub('', row[2])
        pos = kkma.pos(meaning)
        is_possible = check_is_possible(pos, list_positive, list_negative, list_neutral, ALL)
        if is_possible is False:
            update_naming_flag(conn, row[0])
            #print(row[0], is_possible)
            #print('\t\t', meaning)
        #print(filtered_list, len(filtered_list))

#    f_pos.close()
#    f_neg.close()
#    f_neu.close()
    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
