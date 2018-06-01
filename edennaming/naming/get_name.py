#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
from random import randrange

# https://github.com/kaniblu/hangul-utils
from .hangul_utils import hangul_len, split_syllable_char
from .block_list import BLOCK_LIST
from .words_list import WORDS_LIST
from .use_name_list import (MALE_MIDDLE_DICT, FEMALE_MIDDLE_DICT,
                            MALE_LAST_DICT, FEMALE_LAST_DICT,
                            MALE_NAME_DICT, FEMALE_NAME_DICT,)

NORMAL = 0
IGNORE = 1

MALE = 1
FEMALE = 2

HANJA = 0
READING = 1
STROKES = 2
ADD_STROKES = 3
RSC_TYPE = 4
PRONUNCIATIONS = 5


def get_last_name_info(conn, hanja):
    s = conn.cursor()
    query = '''
    SELECT hanja,reading,strokes,add_strokes,rsc_type
    FROM last_name where hanja="%s"
    ''' % hanja
    s.execute(query)
    row = s.fetchone()
    if row is None:
        print('SELECT failed, hanja=', hanja)
        return None
    last_name = list(row)
    if last_name[1] == '리':
        last_name[1] = '이'
    elif last_name[1] == '로':
        last_name[1] = '노'
    elif last_name[1] == '금':
        last_name[1] = '김'
    elif last_name[1] == '림':
        last_name[1] = '임'

    return last_name


def check_81_suri(conn, total_strokes, mode):
    s = conn.cursor()
    query = 'SELECT luck_type FROM naming_81 WHERE strokes=%s' % total_strokes
    for row in s.execute(query):
        if mode == NORMAL:
            if row[0].endswith('吉') is False:  # 여러 케이스 전부 확인
                return False
        elif mode == IGNORE:
            if row[0].endswith('吉') is True:  # 결과가 없어서 무시해야함
                return True
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


def yundal_to_pyoungdal(conn, year, month, day):
    YUNDAL_DICT = {
        '190008': '乙酉',
        '190305': '戊午',
        '190604': '癸巳',
        '190902': '丁卯',
        '191106': '乙未',
        '191405': '庚午',
        '191702': '癸卯',
        '191907': '壬申',
        '192205': '丙午',
        '192504': '辛巳',
        '192802': '乙卯',
        '193006': '癸未',
        '193305': '戊午',
        '193603': '壬辰',
        '193807': '庚申',
        '194106': '乙未',
        '194404': '己巳',
        '194702': '癸卯',
        '194907': '壬申',
        '195205': '丙午',
        '195503': '庚辰',
        '195708': '己酉',
        '196006': '癸未',
        '196304': '丁巳',
        '196603': '壬辰',
        '196807': '庚申',
        '197105': '甲午',
        '197404': '己巳',
        '197608': '丁酉',
        '197906': '辛未',
        '198204': '乙巳',
        '198410': '乙亥',
        '198706': '丁未',
        '199005': '壬午',
        '199303': '丙辰',
        '199508': '乙酉',
        '199805': '戊午',
        '200104': '癸巳',
        '200402': '丁卯',
        '200607': '丙申',
        '200905': '庚午',
        '201203': '甲辰',
        '201409': '甲戌',
        '201705': '丙午',
        '202004': '辛巳',
        '202302': '乙卯',
        '202506': '癸未',
        '202805': '戊午',
        '203103': '壬辰',
        '203311': '癸丑',
        '203606': '乙未',
        '203905': '乙未',
    }
    s = conn.cursor()
    query = '''
    SELECT lun_year, lun_month, lun_day
    FROM gregorian_calendar
    WHERE sol_year=%s and sol_month=%s and sol_day=%s
    ''' % (year, month, day)
    s.execute(query)
    row = s.fetchone()
    yun_month = '%d%02d' % (row[0], row[1])
    return YUNDAL_DICT[yun_month]


def get_secha_wolgeon_iljin(conn, year, month, day):
    s = conn.cursor()
    query = '''
    SELECT lun_secha, lun_wolgeon, lun_iljin, lun_year, lun_month, lun_day
    FROM gregorian_calendar
    WHERE sol_year=%s and sol_month=%s and sol_day=%s
    ''' % (year, month, day)
    s.execute(query)
    row = s.fetchone()
    lun_date = []
    lun_date.append(row[3])
    lun_date.append(row[4])
    lun_date.append(row[5])
    if row[1] == '-':
        pyoungdal = yundal_to_pyoungdal(conn, year, month, day)
        return row[0], pyoungdal, row[2], lun_date
    else:
        return row[0], row[1], row[2], lun_date


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


# 사주에 ‘木’이 3개이상 있을때는 ‘火’ 또는 ‘金’에 해당하는 글자로 작명합니다.
# 사주에 ‘土’가 3개이상 있을때는 ‘金’ 또는 ‘木’에 해당하는 글자로 작명합니다.
# 사주에 ‘火’가 3개이상 있을때는 ‘土’ 또는 ‘水’에 해당하는 글자로 작명합니다.
# 사주에 ‘金’이 3개이상 있을때는 ‘水’ 또는 ‘火’에 해당하는 글자로 작명합니다.
# 사주에 ‘水’가 3개이상 있을때는 ‘木’ 또는 ‘土’에 해당하는 글자로 작명합니다.
# 木火土金水
def check_complementary(strong_energy):
    complementary = []
    if strong_energy == '木':
        complementary.append('火')
        complementary.append('金')
    elif strong_energy == '土':
        complementary.append('金')
        complementary.append('木')
    elif strong_energy == '火':
        complementary.append('土')
        complementary.append('水')
    elif strong_energy == '金':
        complementary.append('水')
        complementary.append('火')
    elif strong_energy == '水':
        complementary.append('木')
        complementary.append('土')
    else:
        return None

    return complementary


def get_complementary(energy):
    strong = max(energy, key=energy.get)
    max_val = energy[strong]
    for key, value in energy.items():
        if value == max_val:
            strong_cnt = key
            break
    c = check_complementary(strong_cnt)
    if c is None:
        return None
    return c, strong


def count_5heng(siju_type, iljin_type, wolgeon_type, secha_type):
    # 木火土金水
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
    return energy


def array_remove_duplicates(l):
    return list(set(l))


def get_saju(conn, birth):
    year = birth[0:4]
    month = birth[4:6]
    day = birth[6:8]
    hour = birth[8:10]
    secha, wolgeon, iljin, lun_date = get_secha_wolgeon_iljin(conn, year, month, day)
    siju = get_siju(iljin[0], int(hour))  # siju : hour

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

    energy = count_5heng(siju_type, iljin_type, wolgeon_type, secha_type)
    complementary_type, strong_energy = get_complementary(energy)

    saju = {
            'year': year, 'month': month.replace('0', ''),
            'day': day.replace('0', ''), 'hour': hour,
            'lun_year': lun_date[0], 'lun_month': lun_date[1], 'lun_day': lun_date[2],
            'c1':  complementary_type[0],
            'c2':  complementary_type[1],
            'strong':  strong_energy,
            'siju': siju, 'siju_type': siju_type,
            'iljin': iljin, 'iljin_type': iljin_type,
            'wolgeon': wolgeon, 'wolgeon_type': wolgeon_type,
            'secha': secha, 'secha_type': secha_type,
            }
    return saju


def check_total_stroke(conn, n1, n2, n3, mode):
    t1 = get_total_strokes(n1, n3, None)
    if t1 == 0:
        return False
    if check_81_suri(conn, t1, mode) is False:  # (홍) 길 (동)
        return False

    t2 = get_total_strokes(n2, n3, None)
    if t2 == 0:
        return False
    if check_81_suri(conn, t2, mode) is False:  # 홍 (길+동)
        return False

    t3 = get_total_strokes(n1, n2, n3)
    if t3 == 0:
        return False
    if check_81_suri(conn, t3, mode) is False:  # (홍+길+동)
        return False

    return True


def check_positive_negative(conn, n1, n2, n3):
    # Hangul
    s1 = hangul_len(n1[1])
    s2 = hangul_len(n2[1])
    s3 = hangul_len(n3[1])
    if s1 % 2 == 0 and s2 % 2 == 0 and s3 % 2 == 0:
        return False
    if s1 % 2 == 1 and s2 % 2 == 1 and s3 % 2 == 1:
        return False
    return True


def check_two_words_hard_pronounce(n1, n2):
    s1 = split_syllable_char(n1)
    s2 = split_syllable_char(n2)

    if len(s1) == 3 and len(s2) == 3:
        if s1[1] == 'ㅕ' and s1[2] == 'ㅇ' and s2[1] == 'ㅡ' and s2[2] == 'ㅇ':  # 경흥원
            return False
        elif s1[1] == 'ㅏ' and s1[2] == 'ㅇ' and s2[1] == 'ㅏ' and s2[2] == 'ㅇ':  # 강항준
            return False
        elif s1[1] == 'ㅏ' and s1[2] == 'ㅇ' and s2[1] == 'ㅑ' and s2[2] == 'ㅇ':  # 강향준
            return False
    return True


def check_all_name_hard_pronounce(s1, s2, s3):

    if (s1[0] == s2[0] == s3[0]):  # 김구관
        return False
    # elif s2[0] == s3[0]:  # 신류려

    # if (s2[1] == 'ㅐ'):  # 김해선 -> 김혜선  신애라
    if (s3[1] == 'ㅔ'):  # 김지에 -> 김지애
        return False

    if (s2[0] == s3[0]):  # 이름의 자음이 같은 경우에 모음 확인
        if (s2[1] == 'ㅜ' and s3[1] == 'ㅜ'):  # 최준주
            return False
        elif (s2[1] == 'ㅜ' and s3[1] == 'ㅠ'):  # 김주쥬
            return False
        elif (s2[1] == 'ㅗ' and s3[1] == 'ㅗ'):  # 박곤고
            return False
        elif (s2[1] == 'ㅗ' and s3[1] == 'ㅛ'):  # 박포표
            return False

    if (s2[1] == 'ㅖ' and s3[1] == 'ㅖ'):  # 이계혜
            return False
    elif (s2[1] == 'ㅖ' and s3[1] == 'ㅐ'):  # 이혜애
            return False
    elif (s2[1] == 'ㅖ' and s3[1] == 'ㅔ'):  # 이혜에
            return False

    # if len(s2) == 3 and len(s3) > 1:
        # if s2[2] == s3[0]:  # 김열루
            # return False
    if len(s2) == 3 and len(s3) == 3:
        if (s2[1] == 'ㅕ' and s2[2] == 'ㄴ' and s3[1] == 'ㅕ' and s3[2] == 'ㄴ'):  # 최현련
            return False
        elif (s2[1] == 'ㅕ' and s2[2] == 'ㅁ' and s3[1] == 'ㅕ' and s3[2] == 'ㅇ'):  # 최겸경
            return False
        elif (s2[1] == 'ㅕ' and s2[2] == 'ㅇ' and s3[1] == 'ㅕ' and s3[2] == 'ㅇ'):  # 최영경
            return False
        elif (s2[1] == 'ㅑ' and s2[2] == 'ㅇ' and s3[1] == 'ㅕ' and s3[2] == 'ㅁ'):  # 최양념
            return False
        elif (s2[1] == 'ㅑ' and s2[2] == 'ㅇ' and s3[1] == 'ㅑ' and s3[2] == 'ㅇ'):  # 최양량
            return False
        elif s2[1] == 'ㅜ' and s2[2] == 'ㅇ' and s3[1] == 'ㅡ' and s3[2] == 'ㅇ':  # 상중승
            return False
        elif s2[1] == 'ㅡ' and s2[2] == 'ㅇ' and s3[1] == 'ㅜ' and s3[2] == 'ㅇ':  # 상승중
            return False
        # elif (s2[2] == 'ㄱ' and s3[2] == 'ㄱ'):  # 이혁탁
            # return False
        # elif (s2[2] == 'ㄴ' and s3[2] == 'ㄴ'):  # 이완린
            # return False
    # elif len(s2) == 3 and len(s3) == 2:
        # if (s2[2] == 'ㄹ' and s3[1] == 'ㅖ'):  # 김설혜
            # return False
    return True


def is_good_pronounce(check_set, set_len):
    if set_len == 5:
        if check_set == 'ㄱㄴㅁㅅㅇ':
            return True

    if set_len == 4:
        if check_set == 'ㄱㄴㅁㅇ':
            return True
        if check_set == 'ㄱㄴㅅㅇ':
            return True
        if check_set == 'ㄴㅁㅅㅇ':
            return True
        if check_set == 'ㄱㅁㅅㅇ':
            return True
        if check_set == 'ㄱㄴㅁㅅ':
            return True
    elif set_len == 3:
        if check_set == 'ㄱㄴㅁ':
            return True
        if check_set == 'ㄱㄴㅇ':
            return True
        if check_set == 'ㄴㅅㅇ':
            return True
        if check_set == 'ㅁㅅㅇ':
            return True
        if check_set == 'ㄱㅁㅅ':
            return True
    elif set_len == 2:
        if check_set == 'ㄱㄴ':
            return True
        if check_set == 'ㄴㅇ':
            return True
        if check_set == 'ㅅㅇ':
            return True
        if check_set == 'ㅁㅅ':
            return True
        if check_set == 'ㄱㅁ':
            return True
    elif set_len == 1:
        if check_set == 'ㄱ':
            return True
        if check_set == 'ㄴ':
            return True
        if check_set == 'ㅁ':
            return True
        if check_set == 'ㅅ':
            return True
        if check_set == 'ㅇ':
            return True

    return False


# 목 -> 화 -> 토 -> 금 -> 수 -> 목 (생)
# 토 -> 목 -> 금 -> 화 -> 수 -> 토 (흉)
def balum_oheng(s1, s2, s3):
    TYPE_DICT = {
        'ㄱ': 'ㄱ', 'ㅋ': 'ㄱ',
        'ㅁ': 'ㅁ', 'ㅂ': 'ㅁ', 'ㅍ': 'ㅁ',
        'ㅅ': 'ㅅ', 'ㅈ': 'ㅅ', 'ㅊ': 'ㅅ',
        'ㅇ': 'ㅇ', 'ㅎ': 'ㅇ',
        'ㄴ': 'ㄴ', 'ㄷ': 'ㄴ', 'ㄹ': 'ㄴ', 'ㅌ': 'ㄴ',
    }

    check_pronounce = []
    check_pronounce.append(TYPE_DICT[s1[0]])
    check_pronounce.append(TYPE_DICT[s2[0]])
    check_pronounce.append(TYPE_DICT[s3[0]])

    if len(s1) == 3:
        check_pronounce.append(TYPE_DICT[s1[2]])
    if len(s2) == 3:
        check_pronounce.append(TYPE_DICT[s2[2]])
    if len(s3) == 3:
        check_pronounce.append(TYPE_DICT[s3[2]])

    temp = sorted(array_remove_duplicates(check_pronounce))
    check_set = ''.join(temp)
    return is_good_pronounce(check_set, len(check_set))


def get_middle_name(conn, n1, n2, saju, gender, n2_rsc_type, mode):
    name_dict = {}
    s = conn.cursor()
    query = """
    SELECT hanja,reading,strokes,add_strokes,rsc_type,pronunciations
    FROM naming_hanja
    WHERE is_naming_hanja=1 AND reading
    NOT IN ('만', '병', '백', '장', '춘', '최', '충', '창', '치', '참', '천',
    '택', '탁', '태', '외', '사', '매', '읍', '소', '종', '순', '요', '자',
    '경', '옥', '해', '부', '효', '존', '난', '류', '홍', '처', '필')
    """
    for n3 in s.execute(query):
        if n1[HANJA] == n3[HANJA] or n2[HANJA] == n3[HANJA]:  # 김주김, 김소소
            continue
        elif n1[READING] == n3[READING] or n2[READING] == n3[READING]:  # 김주김, 김소소
            continue

        n2n3 = '%s%s' % (n2[READING], n3[READING])
        if check_name(n2n3) is False:
            continue

        if check_last_name_gender(n3[READING], n2n3, gender) is False:
            continue

        if saju['c1'] != n3[RSC_TYPE] and saju['c2'] != n3[RSC_TYPE]:
            continue
        if n2_rsc_type == n3[RSC_TYPE]:  # 중간이름에서 사용한 자원오행은 배제함
            continue

        if check_positive_negative(conn, n1, n2, n3) is False:
            continue

        # check positive negative hanja strokes as well
        if check_total_stroke(conn, n1, n2, n3, mode) is False:
            continue

        s1 = split_syllable_char(n1[READING])
        s2 = split_syllable_char(n2[READING])
        s3 = split_syllable_char(n3[READING])
        if balum_oheng(s1, s2, s3) is False:
            continue

        if check_all_name_hard_pronounce(s1, s2, s3) is False:
            continue

        temp_hanja = '%s%s%s' % (n1[HANJA], n2[HANJA], n3[HANJA])
        # temp_hanja = '%s %s %s [%s/ %s]' % (n1[HANJA], n2[HANJA], n3[HANJA],
        #         n2[PRONUNCIATIONS], n3[PRONUNCIATIONS])
        temp_name = '%s%s%s' % (n1[READING], n2[READING], n3[READING])
        name_dict.update({temp_hanja: temp_name})

    if len(name_dict) == 0:
        return None
    return name_dict


def get_total_strokes(n1, n2, n3=None):
    if n1[ADD_STROKES] is None:
        n1_strk = int(n1[STROKES])
    else:
        n1_strk = int(n1[STROKES]) + int(n1[ADD_STROKES])

    if n2[ADD_STROKES] is None:
        n2_strk = int(n2[STROKES])
    else:
        n2_strk = int(n2[STROKES]) + int(n2[ADD_STROKES])

    if n3 is None:
        total_strokes = n1_strk + n2_strk
        # print(n1[2], n1[3], n2[2], n2[3], '---> ', total_strokes)
    else:
        if n3[ADD_STROKES] is None:
            n3_strk = int(n3[STROKES])
        else:
            n3_strk = int(n3[STROKES]) + int(n3[ADD_STROKES])
        # 획수음양
        if n1_strk % 2 == 0 and n2_strk % 2 == 0 and n3_strk % 2 == 0:
            return 0  # 획수가 모두 짝수는 불가
        elif n1_strk % 2 == 1 and n2_strk % 2 == 1 and n3_strk % 2 == 1:
            return 0  # 획수가 모두 홀수는 불가

        total_strokes = n1_strk + n2_strk + n3_strk
        # print(n1[2], n1[3], n2[2], n2[3], n3[2], n3[3], '-> ', total_strokes)
    return total_strokes


def check_name(temp_name):
    try:
        if BLOCK_LIST[temp_name] == 1:
            return False
    except:
        try:
            if WORDS_LIST[temp_name] == 1:
                return False
        except:
            return True
    return True


def print_men_women(temp):
    MEN_LAST_NAME = [
        '기', '관',
        '욱',
        '승', '석',
        '준',
        '찬',
        '혁' '훈', '학',
    ]
    WOMEN_LAST_NAME = [
        '미',
        '희',
        '혜',
    ]

    men = []
    women = []
    both = []

    for i in range(len(temp)):
        done = 0
        for j in range(len(MEN_LAST_NAME)):
            if temp[i][2] == MEN_LAST_NAME[j]:
                men.append(temp[i])
                done = 1
                break
        for k in range(len(WOMEN_LAST_NAME)):
            if temp[i][2] == WOMEN_LAST_NAME[k]:
                women.append(temp[i])
                done = 1
                break
        if done == 0:
            both.append(temp[i])
    print("MEN  : ", men)
    print("WOMEN: ", women)
    print("BOTH : ", both)


def check_middle_name_gender(middle, name, gender):
    if gender == FEMALE:
        try:
            if MALE_MIDDLE_DICT[middle] == 1:
                return False
        except:
            try:
                if MALE_NAME_DICT[name] == 1:
                    return False
            except:
                return True
    else:  # gender == MALE
        try:
            if FEMALE_MIDDLE_DICT[middle] == 1:
                return False
        except:
            try:
                if FEMALE_NAME_DICT[name] == 1:
                    return False
            except:
                return True
        return True


def check_last_name_gender(last, name, gender):
    if gender == FEMALE:
        try:
            if MALE_LAST_DICT[last] == 1:
                return False
        except:
            try:
                if MALE_NAME_DICT[name] == 1:
                    return False
            except:
                return True
        return True
    else:  # gender == MALE
        try:
            if FEMALE_LAST_DICT[last] == 1:
                return False
        except:
            try:
                if FEMALE_NAME_DICT[name] == 1:
                    return False
            except:
                return True
        return True
    return True


def get_names(conn, n1, saju, gender, mode=NORMAL):
    name_dict = {}
    cnt = 0
    s = conn.cursor()
    query = """
    SELECT hanja,reading,strokes,add_strokes,rsc_type,pronunciations
    FROM naming_hanja
    WHERE is_naming_hanja=1
    AND reading
    NOT IN ('각', '과', '균', '니', '락', '랑', '량', '려', '련', '렬',
    '렴', '령', '료', '류', '률', '린', '면', '목', '복', '부', '빈', '안',
    '엄', '열', '옥', '왕', '욱', '읍', '집', '탁', '표', '필',
    '해', '회', '후', '흠',
    '최', '돈', '률', '간', '갈', '계', '곡', '곽', '궁',
    '당', '란', '랑', '뢰', '마', '만', '매', '제', '존',
    '겸', '난', '애')
    """

    for n2 in s.execute(query):
        if n1[READING] == n2[READING]:  # 장장호
            continue

        n1n2 = '%s%s' % (n1[READING], n2[READING])
        if check_name(n1n2) is False:
            continue

        if check_middle_name_gender(n2[READING], n1n2, gender) is False:
            continue

        if saju['c1'] != n2[RSC_TYPE] and saju['c2'] != n2[RSC_TYPE]:
            continue

        ts = get_total_strokes(n1, n2, None)
        if ts == 0 or check_81_suri(conn, ts, mode) is False:  # (홍+길) 동
            continue

        if check_two_words_hard_pronounce(n1[READING], n2[READING]) is False:
            continue

        names = get_middle_name(conn, n1, n2, saju, gender, n2[RSC_TYPE], mode)
        if names is None:
            continue
        name_dict.update(names)
        cnt += 1
    return name_dict, cnt


def get_rsc_type(conn, hanja):
    rsc_type = []
    s = conn.cursor()
    for i in range(1, len(hanja)):
        query = 'SELECT rsc_type FROM naming_hanja where hanja="%s"' % hanja[i]
        s.execute(query)
        row = s.fetchone()
        if row is None:
            print('SELECT failed, hanja=', hanja)
            return None
        rsc_type.append(row[0])

    return rsc_type


def get_suri_detail(conn, sum_suri):

    s = conn.cursor()
    query = 'SELECT level FROM naming_81 WHERE strokes=%d and reference="yxeta"' % sum_suri
    s.execute(query)
    level = s.fetchone()
    query = 'SELECT explain FROM naming_81_explanation WHERE strokes=%d' % sum_suri
    s.execute(query)
    explain = s.fetchone()

    detail = '%s %s' % (level[0], explain[0])
    return detail


def get_luck_type(conn, total_strokes):
    s = conn.cursor()
    query = 'SELECT luck_type FROM naming_81 WHERE strokes=%d AND reference="yxeta"' % total_strokes
    s.execute(query)
    row = s.fetchone()
    if row is None:
        print('SELECT luck_type failed, strokes=', total_strokes)
        return None
    luck_type = row[0]
    if luck_type == '凶':
        luck_type = '半吉'

    return luck_type


def get_suri_hanja(conn, hanja):
    suri_81 = []
    s = conn.cursor()
    for i in range(len(hanja)):
        query = 'SELECT strokes,add_strokes FROM naming_hanja where hanja="%s"' % hanja[i]
        s.execute(query)
        row = s.fetchone()
        if row is None:
            last_s = conn.cursor()
            query = 'SELECT strokes,add_strokes FROM last_name where hanja="%s"' % hanja[i]
            last_s.execute(query)
            last_row = last_s.fetchone()
            print('get_suri_hanja SELECT failed, hanja=', hanja)
            if last_row is None:
                return None
            strokes = list(last_row)
        else:
            strokes = list(row)

        if strokes[1] is None:
            total_strokes = int(strokes[0])
        else:
            total_strokes = int(strokes[0]) + int(strokes[1])
        suri_81.append(total_strokes)

    if len(suri_81) == 2:
        sum_suri = suri_81[1]
        suri_81.append(sum_suri)
        suri_81.append(get_luck_type(conn, sum_suri))
        suri_81.append(get_suri_detail(conn, sum_suri))

        # 형
        sum_suri = suri_81[0] + suri_81[1]
        suri_81.append(sum_suri)
        suri_81.append(get_luck_type(conn, sum_suri))
        suri_81.append(get_suri_detail(conn, sum_suri))

        # 이
        sum_suri = suri_81[0]
        suri_81.append(sum_suri)
        suri_81.append(get_luck_type(conn, sum_suri))
        suri_81.append(get_suri_detail(conn, sum_suri))

        # 정
        sum_suri = suri_81[0] + suri_81[1]
        suri_81.append(sum_suri)
        suri_81.append(get_luck_type(conn, sum_suri))
        suri_81.append(get_suri_detail(conn, sum_suri))

        if suri_81[0] % 2 == 0:
            suri_81[0] = '陰'
        else:
            suri_81[0] = '陽'
        if suri_81[1] % 2 == 0:
            suri_81[1] = '陰'
        else:
            suri_81[1] = '陽'
    elif len(suri_81) == 3:
        # 원
        sum_suri = suri_81[1] + suri_81[2]
        suri_81.append(sum_suri)
        suri_81.append(get_luck_type(conn, sum_suri))
        suri_81.append(get_suri_detail(conn, sum_suri))

        # 형
        sum_suri = suri_81[0] + suri_81[1]
        suri_81.append(sum_suri)
        suri_81.append(get_luck_type(conn, sum_suri))
        suri_81.append(get_suri_detail(conn, sum_suri))

        # 이
        sum_suri = suri_81[0] + suri_81[2]
        suri_81.append(sum_suri)
        suri_81.append(get_luck_type(conn, sum_suri))
        suri_81.append(get_suri_detail(conn, sum_suri))

        # 정
        sum_suri = suri_81[0] + suri_81[1] + suri_81[2]
        suri_81.append(sum_suri)
        suri_81.append(get_luck_type(conn, sum_suri))
        suri_81.append(get_suri_detail(conn, sum_suri))

        if suri_81[0] % 2 == 0:
            suri_81[0] = '陰'
        else:
            suri_81[0] = '陽'
        if suri_81[1] % 2 == 0:
            suri_81[1] = '陰'
        else:
            suri_81[1] = '陽'
        if suri_81[2] % 2 == 0:
            suri_81[2] = '陰'
        else:
            suri_81[2] = '陽'
    elif len(suri_81) == 4:
        # 원
        sum_suri = suri_81[2] + suri_81[3]
        suri_81.append(sum_suri)
        suri_81.append(get_luck_type(conn, sum_suri))
        suri_81.append(get_suri_detail(conn, sum_suri))

        # 형
        sum_suri = suri_81[0] + suri_81[1]
        suri_81.append(sum_suri)
        suri_81.append(get_luck_type(conn, sum_suri))
        suri_81.append(get_suri_detail(conn, sum_suri))

        # 이
        sum_suri = suri_81[0] + suri_81[1] + suri_81[2]
        suri_81.append(sum_suri)
        suri_81.append(get_luck_type(conn, sum_suri))
        suri_81.append(get_suri_detail(conn, sum_suri))

        # 정
        sum_suri = suri_81[0] + suri_81[1] + suri_81[2] + suri_81[3]
        suri_81.append(sum_suri)
        suri_81.append(get_luck_type(conn, sum_suri))
        suri_81.append(get_suri_detail(conn, sum_suri))

        if suri_81[0] % 2 == 0:
            suri_81[0] = '陰'
        else:
            suri_81[0] = '陽'
        if suri_81[1] % 2 == 0:
            suri_81[1] = '陰'
        else:
            suri_81[1] = '陽'
        if suri_81[2] % 2 == 0:
            suri_81[2] = '陰'
        else:
            suri_81[2] = '陽'
        if suri_81[3] % 2 == 0:
            suri_81[3] = '陰'
        else:
            suri_81[3] = '陽'

    return suri_81


def get_suri_hangul(hangul):
    suri_pn = []  # pm: positive, negative
    s = hangul_len(hangul[0])
    if s % 2 == 0:
        suri_pn.append('음')
    else:
        suri_pn.append('양')

    s = hangul_len(hangul[1])
    if s % 2 == 0:
        suri_pn.append('음')
    else:
        suri_pn.append('양')

    s = hangul_len(hangul[2])
    if s % 2 == 0:
        suri_pn.append('음')
    else:
        suri_pn.append('양')
    return suri_pn


def get_name_hanja(conn, hanja):
    hanja_info = []
    s = conn.cursor()
    for i in range(len(hanja)):
        get_hanja = ""
        query = 'SELECT pronunciations FROM naming_hanja where hanja="%s"' % hanja[i]
        s.execute(query)
        row = s.fetchone()
        if row is None:
            last_s = conn.cursor()
            query = 'SELECT pronunciations FROM last_name where hanja="%s"' % hanja[i]
            try:
                last_s.execute(query)
            except:
                print('get_suri_hanja SELECT query failed, hanja=', hanja)
                return None
            last_row = last_s.fetchone()
            if last_row is None:
                print('get_suri_hanja SELECT failed, hanja=', hanja)
                return None
            get_hanja = last_row[0].split(',')[0]
        else:
            get_hanja = row[0].split(',')[0]

        hanja_info.append(get_hanja)
    return hanja_info


def create_result_message(conn, saju, hanja, hangul):
    name_hanja = get_name_hanja(conn, hanja)
    if name_hanja is None:
        return None
    suri_hanja = get_suri_hanja(conn, hanja)
    if suri_hanja is None:
        return None
    rsc_type = get_rsc_type(conn, hanja)

    # <table class="table table-condensed" style="font-size: 15px;">
    new_name = """
    <table class="table">
    <thead>
        <th class="col-xs-2"> 성명 </th>
        <th class="col-xs-10"> <strong style="font-size: 30px;"> %s %s %s (%s %s</strong><mark>%s</mark> <strong style="font-size: 30px;"> %s</strong> <mark>%s</mark>)</th>
    </thead>
    <tbody style='height:5px;'>
        <tr>
            <td> 날짜 </td>
            <td>  %s년% 02s월 %02s일 %s시 [양력]<br> %s년% 02s월 %02s일 [음력]</td>
        </tr>
        <tr>
            <td> 사주오행 </td>
            <td> 時 日 月 年 <br>
            <strong>%s %s %s %s </strong> <br>
            <strong>%s %s %s %s </strong> <br>
             %s %s %s %s <br>
             %s %s %s %s </td>
        </tr>
        <tr>
            <td> 자원오행 </td>
            <td> 사주구성과 오행을 분석한 결과 <mark>%s</mark> 기운이 강하여 <mark>%s, %s</mark> 기운을 가진 글자가 사주구성의 부족한 부분을 보완하여 도움이 됩니다.  선택한 <u>%s(%s) %s(%s)</u>의 기운으로 도움을 줍니다.  </td>
        </tr>
        <tr>
            <td> 획수음양 </td>
            <td> <mark>%s%s%s</mark> 음양이 고루섞여서 吉합니다.</td>
        </tr>
        <tr>
            <td> 수리사격 </td>
            <td> 元<small>(초년운), %s 획 <mark>%s</mark><br> - %s </small><br>
             亨<small>(중년운), %s 획 <mark>%s</mark><br> - %s </small><br>
             利<small>(장년운), %s 획 <mark>%s</mark><br> - %s </small><br>
             貞<small>(말년운), %s 획 <mark>%s</mark><br> - %s </small></td>
        </tr>
        <tr>
            <td> 불용한자 </td>
            <td> 없음 </td>
        </tr>
    </tbody>
</table>
</div>
""" % (hangul[0], hangul[1], hangul[2],
       hanja[0],
       hanja[1],
       name_hanja[1],
       hanja[2],
       name_hanja[2],
       saju['year'], saju['month'], saju['day'], saju['siju'][1],
       saju['lun_year'], saju['lun_month'], saju['lun_day'],
       saju['siju'][0], saju['iljin'][0], saju['wolgeon'][0], saju['secha'][0],
       saju['siju'][1], saju['iljin'][1], saju['wolgeon'][1], saju['secha'][1],
       saju['siju_type'][0], saju['iljin_type'][0], saju['wolgeon_type'][0], saju['secha_type'][0],
       saju['siju_type'][1], saju['iljin_type'][1], saju['wolgeon_type'][1], saju['secha_type'][1],
       saju['strong'], saju['c1'], saju['c2'],
       hanja[1], rsc_type[0], hanja[2], rsc_type[1],
       suri_hanja[0], suri_hanja[1], suri_hanja[2],
       suri_hanja[3], suri_hanja[4], suri_hanja[5],
       suri_hanja[6], suri_hanja[7], suri_hanja[8],
       suri_hanja[9], suri_hanja[10], suri_hanja[11],
       suri_hanja[12], suri_hanja[13], suri_hanja[14],
       )

    print(hanja, hangul)
    return new_name


def get_random_new_name(name_dict):
    if len(name_dict) == 0:
        return None, None
    
    rd = randrange(len(name_dict))
    hanja, hangul = None, None
    for idx, i in enumerate(name_dict):
        if idx == rd:
            hanja = i
            hangul = name_dict[i]
            return hanja, hangul
    return None, None


def get_name(birth, ln, gender):
    conn = sqlite3.connect('naming_korean.db')

    if len(ln) != 1:  # last name
        error_message = "죄송합니다. <br>현재는 1글자 성씨만 지원합니다.<br>"
        return error_message, False

    n1 = get_last_name_info(conn, ln)
    if n1 is None:
        error_message = "죄송합니다. <br>내부 서버에 문제가 있습니다.<br>"
        return error_message, False

    # SAJU
    saju = get_saju(conn, birth)
    if saju is None:
        print('[ERR] get saju failed')
        error_message = "죄송합니다. <br>내부 서버에 문제가 있습니다.<br>"
        return error_message, False

    name_dict, cnt = get_names(conn, n1, saju, gender, NORMAL)
    if len(name_dict) < 1:
        print('Names not found')
        name_dict, cnt = get_names(conn, n1, saju, gender, IGNORE)

    hanja, hangul = get_random_new_name(name_dict)
    if hanja is None or hangul is None:
        print('[ERR] no result', ln, birth)
        error_message = "죄송합니다. <br>내부 서버에 문제가 있습니다.<br>"
        return error_message, False
    print(name_dict)
    print(hanja, hangul)

    new_name_info = create_result_message(conn, saju, hanja, hangul)
    if new_name_info is None:
        print('[ERR] create_result_message failed', ln, birth)
        error_message = "관련 한자에 대한 정보는 현재 제공하지 않습니다.<br>"
        return error_message, False

    conn.close()  # db close
    return new_name_info, True
