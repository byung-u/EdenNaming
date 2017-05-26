#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sqlite3

from bs4 import BeautifulSoup
from hangul_utils import split_syllable_char
from requests import get


"""
naming_hanja
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


TABLE naming_81
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "strokes" integer NULL,
    "reference" char(16) NULL,
    "level" char(16) NULL,
    "luck" char(16) NULL,
    "luck_type" char(1) NULL,

"""

def get_last_name_info(conn, hanja):
    s = conn.cursor()
    query = 'SELECT hanja,reading,strokes,add_strokes,five_type FROM naming_hanja where hanja="%s"' % hanja
    s.execute(query)
    row = s.fetchone()
    print(row)

    result = []
    result.append(row[0])  # ('菊', '국', 12, 2, '木')
    result.append(row[1])
    if row[3] is None:
        strokes = int(row[2])
    else:
        strokes = int(row[2]) + int(row[3])
    result.append(strokes)
    if strokes % 2 == 0:  # 짝수:-, 홀수:+
        result.append('-')
    else:
        result.append('+')

    result.append(row[4])  # 5 type
    return result

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
"""

# 목 -> 화 -> 토 -> 금 -> 수 -> 목 (생)
# 토 -> 목 -> 금 -> 화 -> 수 -> 토 (흉)
def check_five_type(last_name, middle_name):
    # TODO : 현재는 같거나 생인 경우에만 통과 시킴 
    #        다른 케이스가 있는지 추가 확인 필요
    if last_name == '木' and middle_name == '木':
        return True
    elif last_name == '木' and middle_name == '火':
        return True
    elif last_name == '火' and middle_name == '火':
        return True
    elif last_name == '火' and middle_name == '土':
        return True
    elif last_name == '土' and middle_name == '土':
        return True
    elif last_name == '土' and middle_name == '金':
        return True
    elif last_name == '金' and middle_name == '金':
        return True
    elif last_name == '金' and middle_name == '水':
        return True
    elif last_name == '水' and middle_name == '水':
        return True
    elif last_name == '水' and middle_name == '木':
        return True
    else:
        return False


def check_81_suri(conn, total_strokes):
    s = conn.cursor()
    query = 'SELECT luck_type FROM naming_81 WHERE strokes=%s' % total_strokes
    for row in s.execute(query): 
        if (row[0].endswith('吉') == False):  # not 吉
            return False
    return True

def get_middle_name2(conn, last_name_info, middle_name1, m1_strokes):
    middle_name2_list = []
    s = conn.cursor()
    query = 'SELECT hanja,strokes,add_strokes,five_type FROM naming_hanja'
    for row in s.execute(query):  # ('架', 9, None, '木')
        if middle_name1 == row[0]:
            continue
        if (check_five_type(last_name_info[4], row[3]) == False):
            continue

        if row[2] is None:
            strokes = int(row[1])
        else:
            strokes = int(row[1]) + int(row[2])
        total_strokes = last_name_info[2] + strokes
        if (check_81_suri(conn, total_strokes) == False):  # (홍+길) 동
            continue
        if (check_81_suri(conn, m1_strokes + strokes) == False):  # 홍 (길+동)
            continue
        if (check_81_suri(conn, last_name_info[2] + m1_strokes + strokes) == False):  # 홍+길+동
            continue
        if (last_name_info[2] % 2 == 0 and m1_strokes % 2 == 0 and strokes % 2 == 0): # 전부 획수가 음(짝수)
            continue
        if (last_name_info[2] % 2 == 1 and m1_strokes % 2 == 1 and strokes % 2 == 1): # 전부 획수가 양(홀수)
            continue
        middle_name2_list.append(row[0])
    return middle_name2_list


def get_middle_and_last_name(conn, last_name_info):
    s = conn.cursor()
    query = 'SELECT hanja,strokes,add_strokes,five_type FROM naming_hanja'
    last_name = last_name_info[0]
    for row in s.execute(query):  # ('架', 9, None, '木')
        middle_name1 = ''
        if (check_five_type(last_name_info[4], row[3]) == False):
            continue

        if row[2] is None:
            strokes = int(row[1])
        else:
            strokes = int(row[1]) + int(row[2])
        total_strokes = last_name_info[2] + strokes
        if (check_81_suri(conn, total_strokes) == False):
            continue
        middle_name1 = row[0]
        middle_name2_list = get_middle_name2(conn, last_name_info, middle_name1, strokes)
        print(middle_name2_list)
        print(len(middle_name2_list))
        # FIXME : 81 수리까지 체크 완료, 조건을 더 추가해서 줄여야함
# 1. 성에서 받침이 있는지 없는지 확인해서 줄임
# 2. 사주를 먼저 확인해서 보태줄 수 있는 5행 극성을 찾아내서 조건을 더 줄임
        break  # TODO: for dev MUST delete


def get_namelist_with_wh2j(conn, last_name_info):

    get_middle_and_last_name(conn, last_name_info)
    # print(last_name_info)  # ['菊', '국', 14, '-', '木']

    #check_jung_kyuk(conn, last_name_info)  # 성,이름 전부 체크

def get_siju(iljin, hour):
    siju = [
        ["甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥"],
        ["丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥"],
        ["戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥"],
        ["庚子", "辛丑", "壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥"],
        ["壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"],
    ]

    if iljin == '甲' or iljin == '己':
        x = 0
    elif iljin == '乙' or iljin == '庚':
        x = 1
    elif iljin == '丙' or iljin == '辛':
        x = 2
    elif iljin == '丁' or iljin == '壬':
        x = 3
    elif iljin == '戊' or iljin == '癸':
        x = 4
    else:
        print('[ERR] invalid iljin: ', iljin)
        return None

    if 23 <= hour or hour < 1:
        y = 0
    elif 1 <= hour < 3:
        y = 1
    elif 3 <= hour < 5:
        y = 2
    elif 5 <= hour < 7:
        y = 3
    elif 7 <= hour < 9:
        y = 4
    elif 9 <= hour < 11:
        y = 5
    elif 11 <= hour < 13:
        y = 6
    elif 13 <= hour < 15:
        y = 7
    elif 15 <= hour < 17:
        y = 8
    elif 17 <= hour < 19:
        y = 9
    elif 19 <= hour < 21:
        y = 10
    elif 21 <= hour < 23:
        y = 11
    else:
        print('[ERR] invalid hour: ', hour)
        return None
    return (siju[x][y])


def get_secha_wolgeon_iljin(conn, year, month, day):
    s = conn.cursor()
    query = '''
    SELECT lun_secha, lun_wolgeon, lun_iljin 
    FROM gregorian_calendar 
    WHERE sol_year=%s and sol_month=%s and sol_day=%s
    ''' % (year, month, day)
    s.execute(query)
    row = s.fetchone()
    return row[0], row[1], row[2]


def get_h10gan_5types(h10gan):
    if h10gan == '甲' or h10gan == '乙':
        return '木'
    elif h10gan == '丙' or h10gan == '丁':
        return '火'
    elif h10gan == '戊' or h10gan == '己':
        return '土'
    elif h10gan == '庚' or h10gan == '辛':
        return '金'
    elif h10gan == '壬' or h10gan == '癸':
        return '水'
    else:
        return None


#    if h10gan == '甲' or h10gan == '己':
#        return '木'
#    elif h10gan == '乙' or h10gan == '庚':
#        return '火'
#    elif h10gan == '丙' or h10gan == '辛':
#        return '土'
#    elif h10gan == '丁' or h10gan == '壬':
#        return '金'
#    elif h10gan == '戊' or h10gan == '癸':
#        return '水'
#    else:
#        return None


def get_h12ji_5types(h12ji):
    if h12ji == '子' or h12ji == '亥':
        print('h12ji: ', h12ji,  '水')
        return '水'
    elif h12ji == '寅' or h12ji == '卯':
        return '木'
    elif h12ji == '巳' or h12ji == '午':
        return '火'
    elif h12ji == '辰' or h12ji == '戌' or h12ji == '丑' or h12ji == '未':
        return '土'
    elif h12ji == '申' or h12ji == '酉':
        return '金'
    else:
        return None


def get_5types(h10gan, h12ji):
    res_h10gan = get_h10gan_5types(h10gan)
    if res_h10gan is None:
        return None
    res_h12ji = get_h12ji_5types(h12ji)
    if res_h12ji is None:
        return None

    return '%s%s' % (res_h10gan, res_h12ji)

 
def get_saju(conn, birth):
    year = birth[0:4]
    month = birth[4:6]
    day = birth[6:8]
    hour = birth[8:10]
    #print('[DBG1]', year, month, day, hour)
    secha, wolgeon, iljin = get_secha_wolgeon_iljin(conn, year, month, day)
    siju = get_siju(iljin[0], int(hour))  # siju : hour
    #print('[DBG2] hour, day, month, year')
    #print('[DBG2]', siju[0], iljin[0], wolgeon[0], secha[0])
    #print('[DBG3]', siju[1], iljin[1], wolgeon[1], secha[1])

    siju_type = get_5types(siju[0], siju[1])
    if siju_type is None:
        return None
    iljin_type = get_5types(iljin[0], iljin[1])
    if iljin_type is None:
        return None
    wolgeon_type = get_5types(wolgeon[0], wolgeon[1])
    if wolgeon_type is None:
        return None
    secha_type = get_5types(secha[0], secha[1])
    if secha_type is None:
        return None
    print('[DBG4]', siju_type[0], iljin_type[0], wolgeon_type[0], secha_type[0])
    print('[DBG4]', siju_type[1], iljin_type[1], wolgeon_type[1], secha_type[1])

# TODO: get 5 type
    #print('[DBG2]', secha, wolgeon, iljin, siju)

def main():

    conn = sqlite3.connect('naming_korean.db')

    last_name_info = []
    birth='200203011201'
    hanja = "菊"
    # STEP 1: 성씨 정보 확인
    last_name_info = get_last_name_info(conn, hanja)

    # STEP 2: 사주
    saju = get_saju(conn, birth)
    return

    # STEP 3: 원형이정
    possible_name_list = get_namelist_with_wh2j(conn, last_name_info)
    # STEP 1: get 'Supreme Court of Korea' naming hanja list
    #get_sc_naming_hanja(conn)

    # STEP 2: filterling possible naming hanja list
    #check_possible_naming(conn)

    # STEP 3: set detail hanja information
    # set_detail_info(conn)

    # STEP 4: select one of 5 types (木 火 水 土 金)
    #set_five_type(conn)

    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
