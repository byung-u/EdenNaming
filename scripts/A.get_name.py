#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

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
    return row


# 목 -> 화 -> 토 -> 금 -> 수 -> 목 (생)
# 토 -> 목 -> 금 -> 화 -> 수 -> 토 (흉)
def check_five_type(name_type):
    # TODO : 현재는 같거나 생인 경우에만 통과 시킴
    #        다른 케이스가 있는지 추가 확인 필요
    # http://sajuplus.tistory.com/235
    if name_type == '木木水':  # 木
        return True
    elif name_type == '木木火':
        return True
    elif name_type == '木水木':
        return True
    elif name_type == '木水水':
        return True
    elif name_type == '木火木':
        return True
    elif name_type == '木火火':
        return True
    elif name_type == '木火土':
        return True
    elif name_type == '木水金':
        return True
    elif name_type == '火木木':  # 火
        return True
    elif name_type == '火木水':
        return True
    elif name_type == '火木火':
        return True
    elif name_type == '火火木':
        return True
    elif name_type == '火火土':
        return True
    elif name_type == '火土金':
        return True
    elif name_type == '火土火':
        return True
    elif name_type == '火土土':
        return True
    elif name_type == '土金金':  # 土
        return True
    elif name_type == '土金土':
        return True
    elif name_type == '土金水':
        return True
    elif name_type == '土火木':
        return True
    elif name_type == '土火火':
        return True
    elif name_type == '土火土':
        return True
    elif name_type == '土土金':
        return True
    elif name_type == '土土火':
        return True
    elif name_type == '金金水':  # 金
        return True
    elif name_type == '金金土':
        return True
    elif name_type == '金水金':
        return True
    elif name_type == '金水木':
        return True
    elif name_type == '金水水':
        return True
    elif name_type == '金土金':
        return True
    elif name_type == '金土火':
        return True
    elif name_type == '金土土':
        return True
    elif name_type == '水金金':  # 水
        return True
    elif name_type == '水金水':
        return True
    elif name_type == '水金土':
        return True
    elif name_type == '水木木':
        return True
    elif name_type == '水木水':
        return True
    elif name_type == '水木火':
        return True
    elif name_type == '水水金':
        return True
    elif name_type == '水水木':
        return True
    else:  # not in  水火土金木 rule
        return False


def check_81_suri(conn, total_strokes):
    s = conn.cursor()
    query = 'SELECT luck_type FROM naming_81 WHERE strokes=%s' % total_strokes
    for row in s.execute(query):
        if row[0].endswith('吉') is False:  # not 吉
            return False
    return True


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


def get_energy_saju(siju_type, iljin_type, wolgeon_type, secha_type):
    energy = {
            '木': 0,
            '火': 0,
            '土': 0,
            '金': 0,
            '水': 0,
    }
    energy[siju_type[0]] += 1
    energy[siju_type[1]] += 1
    energy[iljin_type[0]] += 1
    energy[iljin_type[1]] += 1
    energy[wolgeon_type[0]] += 1
    energy[wolgeon_type[1]] += 1
    energy[secha_type[0]] += 1
    energy[secha_type[1]] += 1
    return min(energy, key=energy.get), max(energy, key=energy.get)


def get_saju(conn, birth):
    year = birth[0:4]
    month = birth[4:6]
    day = birth[6:8]
    hour = birth[8:10]
    # print('[DBG1]', year, month, day, hour)
    secha, wolgeon, iljin = get_secha_wolgeon_iljin(conn, year, month, day)
    siju = get_siju(iljin[0], int(hour))  # siju : hour
    # print('[DBG2] hour, day, month, year')
    print('[DBG2]', siju[0], iljin[0], wolgeon[0], secha[0])
    print('[DBG3]', siju[1], iljin[1], wolgeon[1], secha[1])

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
    # saju = {
    #         'siju': siju, 'siju_type': siju_type,
    #         'iljin': iljin, 'iljin_type': iljin_type,
    #         'wolgeon': wolgeon, 'wolgeon_type': wolgeon_type,
    #         'secha': secha, 'secha_type': secha_type,
    # }

    week, strong = get_energy_saju(siju_type, iljin_type, wolgeon_type, secha_type)

    return week, strong


def get_name_list(conn, last_name, m1):
    name_list = []
    s = conn.cursor()
    query = 'SELECT hanja,reading,strokes,add_strokes,five_type FROM naming_hanja'
    for m2 in s.execute(query):  # ('架', 9, None, '木')
        if m1[0] == m2[0]:
            continue
        name_type = '%s%s%s' % (last_name[4], m1[4], m2[4])
        if check_five_type(name_type) is False:
            continue

        #check_total_stroke
        t1 = get_total_strokes(last_name, m2, None)
        if check_81_suri(conn, t1) is False:  # (홍+길) 동
            continue

        t2 = get_total_strokes(m1, m2, None)
        if check_81_suri(conn, t2) is False:  # 홍 (길+동)
            continue

        t3 = get_total_strokes(last_name, m1, m2)
        if check_81_suri(conn, t3) is False:  # 홍+길+동
            continue
        #print(t1, t2, t3)
        #print('\t\t', last_name[2], last_name[3], m1[2], m1[3], m2[2], m2[3])
        temp_name = '%s%s%s' % (last_name[1], m1[1], m2[1])
        print('\t\t', temp_name)
 
        #print('last: ', last_name)
        #print('m1  : ', middle_name)
        #print('m2  : ', row)
        #if (last_name_info[2] % 2 == 0 and m1_strokes % 2 == 0 and strokes % 2 == 0):  # 전부 획수가 음(짝수)
        #    continue
        #if (last_name_info[2] % 2 == 1 and m1_strokes % 2 == 1 and strokes % 2 == 1):  # 전부 획수가 양(홀수)
        #    continue
        #middle_name2_list.append(row[0])
        #print(last_name_info[4], mid_5type, row[3])
        #print(last_name_info[0], middle_name1, row[0])
    #return middle_name2_list
    return None


"""
1: 선천명과의 합국 조화 관계 (생년월일시를 기준으로 사주팔자법)
2: 수리영동 조직관계
3: 음양 배열 관계
4: 오행의 배치 관계
5: 자의 정신 관계
6: 음령 오행의 역상 관계
7: 수리 역상의 관계
8: 어휘 어감의 조정 관계
"""

def get_total_strokes(n1, n2, n3=None):
    if n1[3] is None:
        n1_strk = int(n1[2])
    else:
        n1_strk = int(n1[2]) + int(n1[3])

    if n2[3] is None:
        n2_strk = int(n2[2])
    else:
        n2_strk = int(n2[2]) + int(n2[3])

    if n3 is None:
        total_strokes = n1_strk + n2_strk
        # print(n1[2], n1[3], n2[2], n2[3], '---> ', total_strokes)
    else:
        if n3[3] is None:
            n3_strk = int(n3[2])
        else:
            n3_strk = int(n3[2]) + int(n3[3])
        total_strokes = n1_strk + n2_strk + n3_strk
        print(n1[2], n1[3], n2[2], n2[3], n3[2], n3[3],'---> ', total_strokes)
    return total_strokes


def main():

    conn = sqlite3.connect('naming_korean.db')

    birth = '200203011201'
    hanja = "菊"
    # STEP 1: 성씨 정보 확인
    last_name = get_last_name_info(conn, hanja)

    # STEP 2: 사주
    week, strong = get_saju(conn, birth)
    print(week, strong)

    # STEP 3: 원형이정
    s = conn.cursor()
    query = 'SELECT hanja,reading,strokes,add_strokes,five_type FROM naming_hanja'
    # last_name = last_name[0]
    for row in s.execute(query):  # ('架', 9, None, '木')
        # row : middle_name
        name_list = get_name_list(conn, last_name, row)
        break
 
    # possible_name_list = get_namelist_with_wh2j(conn, last_name)
    #print(possible_name_list)
    # STEP 4: 음양 배열 확인 (get_middle_name2 함수에서 처리함)
    # STEP 5: 발음 오행 법 (get_middle_name2 함수에서 처리함)

    # TODO: 부족한 기운까지 가져옴, 자원오행으로 이를 보충해주기 위한 
    # 조건을 추가하여 이름이 될 수 있는 범위를 더 좁혀야함.
    return
    # STEP 1: get 'Supreme Court of Korea' naming hanja list
    # get_sc_naming_hanja(conn)

    # STEP 2: filterling possible naming hanja list
    # check_possible_naming(conn)

    # STEP 3: set detail hanja information
    # set_detail_info(conn)

    # STEP 4: select one of 5 types (木 火 水 土 金)
    # set_five_type(conn)

    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
