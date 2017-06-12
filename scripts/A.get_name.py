#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

from time import time
from random import randrange
from randomdict import RandomDict

# /usr/local/lib/python3.6/site-packages/hangul_utils
from hangul_utils import hangul_len, split_syllable_char
from block_list import BLOCK_LIST
from words_list import WORDS_LIST
from use_name_list import (MALE_MIDDLE_DICT, FEMALE_MIDDLE_DICT,
                           MALE_LAST_DICT, FEMALE_LAST_DICT,
                           MALE_NAME_DICT, FEMALE_NAME_DICT,
                           NEUTRAL_NAME_DICT)

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

# DBG
LAST_NAME_LIST = ['丁', '丕', '丘', '主', '乃', '于', '京', '仇', '付', '任', '伊', '伍', '余', '侯', '倉', '候', '傅', '元', '全', '兪', '公', '具', '初', '判', '剛', '劉', '包', '化', '千', '卓', '南', '卜', '卞', '占', '印', '叢', '史', '吉', '后', '吳', '呂', '周', '咸', '唐', '喬', '單', '嚴', '國', '堅', '增', '墨', '夏', '多', '夜', '大', '天', '太', '夫', '奇', '奈', '奉', '姚', '姜', '孔', '孟', '孫', '安', '宋', '宗', '宣', '寶', '尙', '尹', '山', '崔', '左', '平', '康', '庾', '廉', '延', '弓', '张', '張', '强', '弼', '彈', '彬', '彭', '影', '徐', '愼', '慈', '慶', '成', '戰', '房', '扈', '承', '文', '斤', '方', '施', '昇', '昌', '明', '昔', '星', '晋', '景', '智', '曲', '曺', '曾', '朱', '朴', '杉', '李', '杜', '杨', '松', '林', '柳', '柴', '桂', '梁', '梅', '森', '楊', '楔', '楚', '榮', '樊', '橋', '權', '欒', '武', '段', '殷', '毛', '水', '氷', '江', '池', '沈', '沙', '河', '洙', '洪', '浪', '海', '淳', '湯', '溫', '滕', '漢', '潘', '燕', '片', '牟', '玄', '玉', '王', '班', '琴', '甄', '甘', '田', '申', '畢', '異', '白', '皮', '盧', '眞', '睦', '石', '禹', '秋', '秦', '程', '章', '箕', '管', '簡', '米', '罗', '羅', '耿', '胡', '臧', '舍', '舜', '艾', '芮', '芸', '苑', '苗', '范', '荀', '莊', '菊', '萬', '葉', '葉', '葛', '董', '蔡', '蔣', '薛', '蘇', '衛', '表', '袁', '裵', '解', '許', '諸', '謝', '譚', '谷', '賀', '賈', '賓', '趙', '路', '車', '辛', '連', '道', '邊', '邕', '邢', '邦', '邱', '邵', '郝', '郭', '都', '鄒', '鄧', '鄭', '采', '釋', '金', '錢', '鍾', '鎬', '閔', '閻', '關', '阮', '阿', '陈', '陰', '陳', '陶', '陸', '隋', '雍', '雲', '雷', '鞠', '韋', '韓', '順', '頓', '顧', '馬', '馮', '高', '魏', '魚', '魯', '鳳', '鴌', '麻', '黃', '黎', '齊', '龍', '龐', ]


def get_last_name_info(conn, hanja):
    s = conn.cursor()
    query = 'SELECT hanja,reading,strokes,add_strokes,rsc_type FROM last_name where hanja="%s"' % hanja
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
    # print('[DBG] -----------')
    # print('[DBG] 시 일 월 년')
    # print('[DBG] -----------')
    # print('[D간]', siju[0], iljin[0], wolgeon[0], secha[0])
    # print('[D지]', siju[1], iljin[1], wolgeon[1], secha[1])
    # print('[DBG] -----------')
    # print('[DBG]', siju_type[0], iljin_type[0], wolgeon_type[0], secha_type[0])
    # print('[DBG]', siju_type[1], iljin_type[1], wolgeon_type[1], secha_type[1])
    # print('[DBG] -----------')

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


# DBG
def get_one_last_name():
    rd = randrange(len(LAST_NAME_LIST))
    return LAST_NAME_LIST[rd]


# DBG
def get_random_birth():
    # '200103010310'  # '200203011201'
    year = randrange(1990, 2017, 1)
    month = randrange(1, 12, 1)
    day = randrange(1, 28, 1)
    hour = randrange(1, 24, 1)
    minute = randrange(1, 60, 1)
    return '%d%02d%02d%02d%02d' % (year, month, day, hour, minute)


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
    NOT IN ('각', '과', '국', '균', '니', '락', '랑', '량', '려', '련', '렬',
    '렴', '령', '료', '류', '률', '린', '면', '목', '복', '부', '빈', '안',
    '엄', '열', '오', '옥', '왕', '요', '욱', '읍', '집', '탁', '표', '필',
    '해', '회', '후', '흠',
    '최', '환', '돈', '률', '간', '갈', '견', '계', '곡', '공', '곽', '궁',
    '노', '당', '무', '등', '란', '랑', '뢰', '마', '만', '매', '제', '존',
    '화', '위', '겸', '구', '난', '화', '후', '애')
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

        strokes = list(row)
        if strokes[1] is None:
            suri_81.append(int(strokes[0]))
        else:
            suri_81.append(int(strokes[0]) + int(strokes[1]))

    if len(suri_81) == 3:
        suri_81.append(suri_81[0] + suri_81[1])
        suri_81.append(suri_81[1] + suri_81[2])
        suri_81.append(suri_81[2] + suri_81[0])
        suri_81.append(suri_81[0] + suri_81[1] + suri_81[2])
        if suri_81[0] % 2 == 0:
            suri_81[0] = '음'
        else:
            suri_81[0] = '양'
        if suri_81[1] % 2 == 0:
            suri_81[1] = '음'
        else:
            suri_81[1] = '양'
        if suri_81[2] % 2 == 0:
            suri_81[2] = '음'
        else:
            suri_81[2] = '양'
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
        query = 'SELECT pronunciations FROM naming_hanja where hanja="%s"' % hanja[i]
        s.execute(query)
        row = s.fetchone()
        if row is None:
            last_s = conn.cursor()
            query = 'SELECT pronunciations FROM last_name where hanja="%s"' % hanja[i]
            last_s.execute(query)
            last_row = last_s.fetchone()
            print('get_suri_hanja SELECT failed, hanja=', hanja)
            if last_row is None:
                return None
        hanja_info.append(row[0])
    return hanja_info


def create_result_message(conn, saju, hanja, hangul):
    name_hanja = get_name_hanja(conn, hanja)
    suri_hangul = get_suri_hangul(hangul)
    suri_hanja = get_suri_hanja(conn, hanja)
    rsc_type = get_rsc_type(conn, hanja)

    new_name = """
<table class="table">
    <thead>
        <th>성명: </th>
        <th> %s  %s%s[%s %s<small>%s</small> %s<small>%s</small>] </th>
        <th>  </th>
    </thead>
    <tbody>
        <tr>
            <td>  </td>
            <td>  </td>
            <td>  </td>
        </tr>
        <tr>
            <td> 양력: </td>
            <td>  %s년% 02s월 %02s일 %s시 </td>
            <td> </td>
        </tr>
        <tr>
            <td> 음력: </td>
            <td> %s년% 02s월 %02s일 </td>
            <td> </td>
        </tr>
        <tr>
            <td> </td>
            <td> </td>
            <td> </td>
        </tr>
        <tr>
            <td> 四柱 </td>
            <td> 時 日 月 年 </td>
            <td> </td>
        </tr>
        <tr>
            <td> </td>
            <td> <strong>%s %s %s %s </strong> </td>
            <td> </td>
        </tr>
        <tr>
            <td> </td>
            <td> <strong>%s %s %s %s </strong> </td>
            <td> </td>
        </tr>
        <tr>
            <td> </td>
            <td> %s %s %s %s </td>
            <td> </td>
        </tr>
        <tr>
            <td> </td>
            <td> %s %s %s %s </td>
            <td> </td>
        </tr>
        <tr>
            <td> 수리음양: </td>
            <td> <mark>%s%s%s</mark> 조화를 이룬다. </td>
            <td> </td>
        </tr>
        <tr>
            <td> 발음오행: </td>
            <td> <mark>%s%s%s</mark> 조화를 이룬다.  </td>
            <td> </td>
        </tr>
        <tr>
            <td> 수리사격: </td>
            <td> 모두 좋은 작용의 吉격 수리로 구성되어있다. </td>
            <td> </td>
        </tr>
        <tr>
            <td> </td>
            <td> <mark> 元: %s  亨: %s  利: %s  貞: %s</mark> (획) </td>
            <td> </td>
        </tr>
        <tr>
            <td> 자원오행: </td>
            <td> 사주구성과 오행을 분석한 결과 </td>
            <td> </td>
        </tr>
        <tr>
            <td> </td>
            <td> <mark>%s, %s</mark> 기운을 가진 글자가 </td>
            <td> </td>
        </tr>
        <tr>
            <td> </td>
            <td> 사주구성의 부족한 부분을 보완하여 도움이 된다.  </td>
            <td> </td>
        </tr>
        <tr>
            <td> </td>
            <td> 선택한 <u>%s(%s) %s(%s)</u>의 기운으로 도움을 준다.  </td>
            <td> </td>
        </tr>
        <tr>
            <td> 불용한자: </td>
            <td> 없음 </td>
            <td> </td>
        </tr>
    </tbody>
</table>
</div>
<div class="bs-callout bs-callout-warning">
</div>
""" % (hangul[0], hangul[1], hangul[2],
       hanja[0], hanja[1], name_hanja[1], hanja[2], name_hanja[2],
       saju['year'], saju['month'], saju['day'], saju['siju'][1],
       saju['lun_year'], saju['lun_month'], saju['lun_day'],
       saju['siju'][0], saju['iljin'][0], saju['wolgeon'][0], saju['secha'][0],
       saju['siju'][1], saju['iljin'][1], saju['wolgeon'][1], saju['secha'][1],
       saju['siju_type'][0], saju['iljin_type'][0], saju['wolgeon_type'][0], saju['secha_type'][0],
       saju['siju_type'][1], saju['iljin_type'][1], saju['wolgeon_type'][1], saju['secha_type'][1],
       suri_hanja[0], suri_hanja[1], suri_hanja[2],
       suri_hangul[0], suri_hangul[1], suri_hangul[2],
       suri_hanja[3], suri_hanja[4], suri_hanja[5], suri_hanja[6],
       saju['c1'], saju['c2'],
       hanja[1], rsc_type[0], hanja[2], rsc_type[1])

    return new_name


def main():
    start_time = time()  # START
    conn = sqlite3.connect('naming_korean.db')

    # DBG TEST data
    birth = get_random_birth()  # '200103010310'  # '200203011201'
    ln = get_one_last_name()
    gender = FEMALE

    n1 = get_last_name_info(conn, ln)
    if n1 is None:
        return

    # SAJU
    saju = get_saju(conn, birth)
    if saju is None:
        print('[ERR] get saju failed')
        return

    name_dict, cnt = get_names(conn, n1, saju, gender, NORMAL)
    if len(name_dict) < 3:
        print('Names not found')
        name_dict, cnt = get_names(conn, n1, saju, gender, IGNORE)
        # names = array_remove_duplicates(name_dict)

    choose = RandomDict(name_dict)
    r_name = choose.random_item()
    new_name_info = create_result_message(conn, saju, r_name[0], r_name[1])

    print(new_name_info)
    print(ln, birth, gender)
    print("%.3f sec Total: %d(%d)" % ((time() - start_time), len(name_dict), cnt))
    conn.close()  # db close
    return


if __name__ == '__main__':
    main()
