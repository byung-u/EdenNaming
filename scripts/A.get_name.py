#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

from time import time
from random import randrange

# /usr/local/lib/python3.6/site-packages/hangul_utils
from hangul_utils import hangul_len, split_syllable_char
from block_list import BLOCK_LIST
from words_list import WORDS_LIST

SHINGANG = 1
SHINYACK = 0

HANJA = 0
READING = 1
STROKES = 2
ADD_STROKES = 3
RSC_TYPE = 4

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
    SELECT lun_secha, lun_wolgeon, lun_iljin
    FROM gregorian_calendar
    WHERE sol_year=%s and sol_month=%s and sol_day=%s
    ''' % (year, month, day)
    s.execute(query)
    row = s.fetchone()
    if row[1] == '-':
        pyoungdal = yundal_to_pyoungdal(conn, year, month, day)
        return row[0], pyoungdal, row[2]
    else:
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
def check_complementary(many):
    complementary = []
    if many == '木':
        complementary.append('火')
        complementary.append('金')
    elif many == '土':
        complementary.append('金')
        complementary.append('木')
    elif many == '火':
        complementary.append('土')
        complementary.append('水')
    elif many == '金':
        complementary.append('水')
        complementary.append('火')
    elif many == '水':
        complementary.append('木')
        complementary.append('土')
    else:
        return None

    return complementary


def get_complementary(energy):
    max_val = energy[max(energy, key=energy.get)]
    for key, value in energy.items():
        if value == max_val:
            many = key
            break
    c = check_complementary(many)
    if c is None:
        return None
    return c


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
    secha, wolgeon, iljin = get_secha_wolgeon_iljin(conn, year, month, day)
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
    print('[DBG] -----------')
    print('[DBG] 시 일 월 년')
    print('[DBG] -----------')
    print('[D간]', siju[0], iljin[0], wolgeon[0], secha[0])
    print('[D지]', siju[1], iljin[1], wolgeon[1], secha[1])
    print('[DBG] -----------')
    print('[DBG]', siju_type[0], iljin_type[0], wolgeon_type[0], secha_type[0])
    print('[DBG]', siju_type[1], iljin_type[1], wolgeon_type[1], secha_type[1])
    print('[DBG] -----------')

    energy = count_5heng(siju_type, iljin_type, wolgeon_type, secha_type)
    complementary_type = get_complementary(energy)

    saju = {
        'year': year, 'month': month,
        'c1':  complementary_type[0],
        'c2':  complementary_type[1],
        'siju': siju, 'siju_type': siju_type,
        'iljin': iljin, 'iljin_type': iljin_type,
        'wolgeon': wolgeon, 'wolgeon_type': wolgeon_type,
        'secha': secha, 'secha_type': secha_type,
    }
    return saju


def check_total_stroke(conn, n1, n2, n3):
    t1 = get_total_strokes(n1, n3, None)
    if t1 == 0:
        return False
    if check_81_suri(conn, t1) is False:  # (홍) 길 (동)
        return False

    t2 = get_total_strokes(n2, n3, None)
    if t2 == 0:
        return False
    if check_81_suri(conn, t2) is False:  # 홍 (길+동)
        return False

    t3 = get_total_strokes(n1, n2, n3)
    if t3 == 0:
        return False
    if check_81_suri(conn, t3) is False:  # (홍+길+동)
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


def get_name_list(conn, n1, n2, saju):
    name_list = []
    s = conn.cursor()
    query = """
    SELECT hanja,reading,strokes,add_strokes,rsc_type
    FROM naming_hanja
    WHERE is_naming_hanja=1 AND reading
    NOT IN ('만', '병', '백', '장', '춘', '최', '충', '창', '치', '참', '천',
    '택', '탁', '태', '외', '사', '매', '읍', '소', '종', '순', '요', '자',
    '경', '옥', '해', '부', '효', '존')
    """
    for n3 in s.execute(query):
        if n1[HANJA] == n3[HANJA] or n2[HANJA] == n3[HANJA]:  # 김주김, 김소소
            continue
        elif n1[READING] == n3[READING] or n2[READING] == n3[READING]:  # 김주김, 김소소
            continue

        n2n3 = '%s%s' % (n2[1], n3[1])
        if check_name(n2n3) is False:
            continue

        if saju['c1'] != n2[RSC_TYPE] and saju['c2'] != n3[RSC_TYPE]:
            continue

        if check_positive_negative(conn, n1, n2, n3) is False:
            continue

        # check positive negative hanja strokes as well
        if check_total_stroke(conn, n1, n2, n3) is False:
            continue

        s1 = split_syllable_char(n1[READING])
        s2 = split_syllable_char(n2[READING])
        s3 = split_syllable_char(n3[READING])
        if balum_oheng(s1, s2, s3) is False:
            continue

        if check_all_name_hard_pronounce(s1, s2, s3) is False:
            continue

        temp_name = '%s%s%s' % (n1[1], n2[1], n3[1])
        name_list.append(temp_name)

    if len(name_list) == 0:
        return None

    return name_list


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


def main():
    start_time = time()  # START
    conn = sqlite3.connect('naming_korean.db')

    # DBG TEST data
    birth = get_random_birth()  # '200103010310'  # '200203011201'
    ln = get_one_last_name()
    birth = '199410172113'
    ln = '夜'
    # LAST NAME
    n1 = get_last_name_info(conn, ln)
    if n1 is None:
        return

    # SAJU
    saju = get_saju(conn, birth)
    if saju is None:
        print('[ERR] get saju failed')
        return

    name_list = []
    cnt = 0
    s = conn.cursor()
    query = """
    SELECT hanja,reading,strokes,add_strokes,rsc_type
    FROM naming_hanja
    WHERE is_naming_hanja=1
    AND reading
    NOT IN ('각', '과', '국', '균', '니', '락', '랑', '량', '려', '련', '렬',
    '렴', '령', '료', '류', '률', '린', '면', '목', '복', '부', '빈', '안',
    '엄', '열', '오', '옥', '왕', '요', '욱', '읍', '집', '탁', '표', '필',
    '해', '회', '후', '흠')
    """
    for n2 in s.execute(query):
        if n1[READING] == n2[READING]:  # 장장호
            continue

        n1n2 = '%s%s' % (n1[READING], n2[READING])
        if check_name(n1n2) is False:
            continue

        if saju['c1'] != n2[RSC_TYPE] and saju['c2'] != n2[RSC_TYPE]:
            continue

        ts = get_total_strokes(n1, n2, None)
        if ts == 0 or check_81_suri(conn, ts) is False:  # (홍+길) 동
            continue

        if check_two_words_hard_pronounce(n1[READING], n2[READING]) is False:
            continue

        names = get_name_list(conn, n1, n2, saju)
        if names is None:
            continue
        name_list.extend(names)
        cnt += 1
    # DBG
    temp = array_remove_duplicates(name_list)
    # print_men_women(temp)
    print(temp)
    print(ln, birth)
    print("%.3f sec, Total: %d(%d) -> %d" % ((time() - start_time), len(name_list), cnt, len(temp)))

    conn.close()  # db close
    return


if __name__ == '__main__':
    main()
